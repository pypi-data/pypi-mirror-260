import time
from collections import OrderedDict
from typing import Callable


class CacheSystem:
    def __init__(
            self, default_fetch_function: Callable = None, default_expiry_time: int = 300, max_size: int | None = None
    ) -> None:
        self.cache: OrderedDict[str, dict[str, any]] = OrderedDict()
        self.default_fetch_function: Callable = default_fetch_function
        self.default_expiry_time: int = default_expiry_time
        self.max_size: int | None = max_size
        self.hits: int = 0
        self.misses: int = 0

    def get(
            self,
            *args,
            cache_key_name: str,
            specialized_fetch_function: Callable = None,
            specialized_expiry_time: int = None,
            force_new: bool = False,
            **kwargs
    ) -> any:
        self.cleanup()
        current_time: int = int(time.time())
        if not force_new and cache_key_name in self.cache:
            entry = self.cache[cache_key_name]
            if entry['expiry_time'] > current_time:
                self.hits += 1
                self.cache.move_to_end(cache_key_name)
                return entry['data']

        self.misses += 1
        func: Callable = specialized_fetch_function or self.default_fetch_function
        data: any = func(*args, **kwargs)
        self.cache[cache_key_name] = {
            'data': data, 'expiry_time': current_time + (specialized_expiry_time or self.default_expiry_time)
        }
        self.cache.move_to_end(cache_key_name)
        self.ensure_max_size()
        return data

    def remove(self, cache_key_name: str) -> None:
        if cache_key_name in self.cache:
            del self.cache[cache_key_name]

    def cleanup(self) -> None:
        current_time: int = int(time.time())
        keys_to_delete: list[str] = [key for key, value in self.cache.items() if value['expiry_time'] <= current_time]
        if keys_to_delete:
            for key in keys_to_delete:
                del self.cache[key]

    def ensure_max_size(self) -> None:
        if self.max_size is not None and len(self.cache) > self.max_size:
            oldest_key: str = next(iter(self.cache))
            del self.cache[oldest_key]

    def get_stats(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses, "size": len(self.cache)}
