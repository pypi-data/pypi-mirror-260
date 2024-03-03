from __future__ import annotations

import pickle
import re
from pathlib import Path
from typing import Callable, Union

from box import Box


class IntactBox(Box):
    pass

class DataboxLoader:

    def __init__(
        self,
        builder,
        parent: Union[None, DataboxLoader] = None,
        name=None,
        base_dir="data",
        cache_dir=None,
        no_cache=False,
        no_cache_read=False,
        no_cache_write=False,
        cacheable=[],
        debug=False,
    ):
        # normalize arguments
        base_dir = Path(base_dir)
        if cache_dir is None:
            cache_dir = base_dir / "cache"

        if no_cache:
            no_cache_read = True
            no_cache_write = True

        # initialize
        self.parent = parent
        self.name = name
        if self.parent is not None and self.name is None:
            raise ValueError(f"A child DataboxLoader must have a name.")

        self.box = IntactBox(
            default_box=True,
            default_box_no_key_error=False,
            default_box_none_transform=False,
            default_box_create_on_get=False,
            default_box_attr=self.load_databox_item,
            box_intact_types=[IntactBox],
        )

        if self.parent is None:
            self.events = []
            self.root = Box()
            self.root.config = {}

            self.root.config.NO_CACHE = no_cache
            self.root.config.NO_CACHE_READ = no_cache_read
            self.root.config.NO_CACHE_WRITE = no_cache_write
            self.root.config.CACHEABLE = cacheable
            self.root.config.BASE_DIR = base_dir
            self.root.config.CACHE_DIR = cache_dir
            self.root.config.DEBUG = debug
        else:
            self.root = self.parent.root

        self.builder = builder
        self.builder_build_method = None
        self.builder_build_method_method = None
        self.builder_init_method = None

        if self.builder is not None:
            try:
                self.builder_build_method = getattr(self.builder, "BUILD")
            except:
                pass

            try:
                self.builder_init_method = getattr(self.builder, "INIT")
            except:
                pass

            try:
                self.builder_build_method_method = getattr(self.builder, "BUILD_METHOD")
            except:
                pass

        self.events = []

        if self.builder_init_method is not None:
            self._log_event(
                "Init builder {item_path}",
                type="BuilderInit",
                item_path=self.item_path(),
            )
            self.builder_init_method(self)

    @property
    def root_loader(self):
        if self.parent is None:
            return self
        else:
            return self.parent.root_loader

    @property
    def root_box(self):
        return self.root_loader.box

    def child_loader(self, builder: object, name: str) -> DataboxLoader:
        return DataboxLoader(builder, parent=self, name=name)

    def load_databox_item(self, box_instance, key):

        self.debug_msg(f"LOAD [{self.name}] {key} {self.builder}")

        item_path = self.item_path(key)
        item = None

        if self.builder is None:
            raise NameError(f"Unknown item key name {item_path}, no builder")

        if not self.root.config.NO_CACHE_READ and self.is_item_path_cacheable(
            item_path
        ):
            item = self.read_from_cache(item_path)
            if item is None:
                self._log_event(
                    "Item {item_path} not found in cache",
                    type="CacheMiss",
                    item_path=item_path,
                    item_cache_path=str(self.item_cache_path(item_path))
                )
            else:
                self._log_event(
                    "Item {item_path} loaded from cache",
                    type="CacheHit",
                    item_path=item_path,
                    item_cache_path=str(self.item_cache_path(item_path))
                )

        if item is not None:
            self.box[key] = item
            return item
        
        build_method = None
        if self.builder_build_method_method is not None:
            build_method = self.builder_build_method_method(self, key)

        if build_method is None:
            build_method_name = f"build_{key}"
            try:
                build_method = getattr(self.builder, build_method_name)
                if not isinstance(build_method, Callable):
                    raise NameError(
                        f"Unknown item key name {item_path}. {build_method_name} is not callable"
                    )
            except:
                if self.builder_build_method is None:
                    raise NameError(f"Unknown item key name {item_path}, no builder method")
                else:
                    build_method = self.builder_build_method

        item = build_method(self, key)

        if item is None:
            raise NameError(f"Unknown item key name {item_path}, unknown item.")

        if isinstance(item, DataboxLoader):
            item_loader = item
            if item_loader.name is None:
                item_loader.name = key
            item = item_loader.box
            print("Item as loader:", item_loader, item)

        self._log_event(
            "Item {item_path} built using {build_method}",
            type="ItemBuild",
            item_path=item_path,
            build_method=build_method.__name__,
        )
        if not self.root.config.NO_CACHE_WRITE and self.is_item_path_cacheable(
            item_path
        ):
            self._log_event(
                "Item {item_path} written to cache: {item_cache_path}",
                type="CacheWrite",
                item_path=item_path,
                item_cache_path=str(self.item_cache_path(item_path)),
            )
            self.write_to_cache(item_path, item)

        self.box[key] = item

        return item

    def box_path(self, path: Union[str, Path]) -> Path:
        return self.root.config.BASE_DIR / Path(path)

    def item_path(self, key=None):
        if self.parent is None:
            if key is None:
                return ""
            else:
                return key
        else:
            if key is None:
                return self.parent.item_path(self.name)
            else:
                return self.parent.item_path(self.name) + "/" + key

    def item_cache_path(self, item_path) -> Path:
        return (self.root.config.CACHE_DIR / item_path).with_suffix(".pickle")

    def is_item_path_cacheable(self, item_path):
        for c in self.root.config.CACHEABLE:
            if isinstance(c, str) and c == item_path:
                return True
            elif isinstance(c, re.Pattern) and c.match(item_path):
                return True
        return False

    def read_from_cache(self, item_path):
        pickle_path = self.item_cache_path(item_path)
        if pickle_path.exists():
            return load_from_pickle(pickle_path)
        return None

    def write_to_cache(self, item_path, item):
        pickle_path = self.item_cache_path(item_path)
        pickle_path.parent.mkdir(exist_ok=True, parents=True)
        dump_to_pickle(item, pickle_path)

    def _log_event(self, msg: str, **params):
        if self.parent is None:
            message = msg.format(**params)
            self.debug_msg(message)
            self.events.append(Box({"message": message, **params}))
        else:
            self.parent._log_event(msg, **params)

    def debug_msg(self, msg):
        if self.root.config.DEBUG:
            print(msg, flush=True)


def dump_to_pickle(data, data_path):

    with data_path.open("wb") as fh:
        pickle.dump(data, fh)


def load_from_pickle(data_path):

    with data_path.open("rb") as fh:
        data = pickle.load(fh)

    return data
