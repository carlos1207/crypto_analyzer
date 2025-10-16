"""
Simple in-memory caching system with TTL
"""

from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib
import json


class Cache:
    """
    Simple in-memory cache with time-to-live (TTL) support
    """

    def __init__(self):
        self._cache = {}

    def _generate_key(self, prefix: str, **kwargs) -> str:
        """Generate a cache key from prefix and parameters"""
        # Sort kwargs for consistent key generation
        params_str = json.dumps(kwargs, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f"{prefix}:{params_hash}"

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if it exists and hasn't expired

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if datetime.now() > entry['expires_at']:
            # Expired, remove it
            del self._cache[key]
            return None

        return entry['value']

    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """
        Set a value in the cache with TTL

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (default: 5 minutes)
        """
        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = {
            'value': value,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }

    def delete(self, key: str):
        """Delete a key from cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()

    def get_stats(self) -> dict:
        """Get cache statistics"""
        now = datetime.now()
        active_keys = sum(1 for entry in self._cache.values() if now <= entry['expires_at'])

        return {
            'total_keys': len(self._cache),
            'active_keys': active_keys,
            'expired_keys': len(self._cache) - active_keys
        }

    def cleanup_expired(self):
        """Remove all expired entries"""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self._cache.items()
            if now > entry['expires_at']
        ]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)


# Global cache instance
_global_cache = Cache()


def get_cache() -> Cache:
    """Get the global cache instance"""
    return _global_cache


# Decorator for caching function results
def cached(ttl_seconds: int = 300, key_prefix: str = None):
    """
    Decorator to cache function results

    Args:
        ttl_seconds: Time to live in seconds
        key_prefix: Prefix for cache key (defaults to function name)

    Example:
        @cached(ttl_seconds=600, key_prefix='historical_data')
        def get_historical_data(symbol, days):
            # expensive operation
            return data
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_cache()

            # Generate cache key
            prefix = key_prefix or func.__name__
            key_params = {
                'args': args,
                'kwargs': kwargs
            }
            cache_key = cache._generate_key(prefix, **key_params)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Not in cache, call function
            result = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl_seconds)

            return result

        return wrapper
    return decorator


if __name__ == "__main__":
    # Test the cache
    cache = Cache()

    # Test basic set/get
    cache.set('test_key', 'test_value', ttl_seconds=2)
    print(f"Get test_key: {cache.get('test_key')}")  # Should return 'test_value'

    # Test expiration
    import time
    time.sleep(3)
    print(f"Get test_key after expiry: {cache.get('test_key')}")  # Should return None

    # Test stats
    cache.set('key1', 'value1', ttl_seconds=100)
    cache.set('key2', 'value2', ttl_seconds=100)
    cache.set('key3', 'value3', ttl_seconds=1)
    time.sleep(2)

    print(f"Stats: {cache.get_stats()}")
    print(f"Cleaned up {cache.cleanup_expired()} expired keys")
    print(f"Stats after cleanup: {cache.get_stats()}")
