"""
EduAI - Sistema de Cache
Sistema de cache em memória para melhorar performance
"""

import time
import threading
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass
from ..config import config

@dataclass
class CacheItem:
    """Item do cache"""
    value: Any
    timestamp: float
    ttl: int  # Time to live em segundos
    
    def is_expired(self) -> bool:
        """Verifica se o item expirou"""
        return time.time() - self.timestamp > self.ttl

class MemoryCache:
    """Cache em memória thread-safe"""
    
    def __init__(self, default_ttl: int = None):
        self._cache: Dict[str, CacheItem] = {}
        self._lock = threading.RLock()
        self.default_ttl = default_ttl or config.app.cache_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache"""
        with self._lock:
            if key not in self._cache:
                return None
            
            item = self._cache[key]
            if item.is_expired():
                del self._cache[key]
                return None
            
            return item.value
    
    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Define um valor no cache"""
        with self._lock:
            ttl = ttl or self.default_ttl
            self._cache[key] = CacheItem(
                value=value,
                timestamp=time.time(),
                ttl=ttl
            )
    
    def delete(self, key: str) -> bool:
        """Remove um valor do cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove itens expirados e retorna a quantidade removida"""
        with self._lock:
            expired_keys = [
                key for key, item in self._cache.items()
                if item.is_expired()
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)
    
    def size(self) -> int:
        """Retorna o tamanho do cache"""
        with self._lock:
            return len(self._cache)
    
    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: int = None) -> Any:
        """Obtém um valor do cache ou o cria usando a factory"""
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value

class CacheManager:
    """Gerenciador de cache com diferentes tipos de cache"""
    
    def __init__(self):
        self._caches: Dict[str, MemoryCache] = {}
        self._lock = threading.RLock()
        
        # Criar caches específicos
        self._create_default_caches()
    
    def _create_default_caches(self):
        """Cria caches padrão"""
        # Cache para usuários (TTL de 5 minutos)
        self._caches['users'] = MemoryCache(default_ttl=300)
        
        # Cache para aulas (TTL de 10 minutos)
        self._caches['aulas'] = MemoryCache(default_ttl=600)
        
        # Cache para histórico (TTL de 2 minutos)
        self._caches['historico'] = MemoryCache(default_ttl=120)
        
        # Cache para configurações (TTL de 1 hora)
        self._caches['config'] = MemoryCache(default_ttl=3600)
    
    def get_cache(self, name: str) -> MemoryCache:
        """Obtém um cache específico"""
        with self._lock:
            if name not in self._caches:
                self._caches[name] = MemoryCache()
            return self._caches[name]
    
    def clear_all(self) -> None:
        """Limpa todos os caches"""
        with self._lock:
            for cache in self._caches.values():
                cache.clear()
    
    def cleanup_all(self) -> Dict[str, int]:
        """Limpa itens expirados de todos os caches"""
        with self._lock:
            results = {}
            for name, cache in self._caches.items():
                results[name] = cache.cleanup_expired()
            return results
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Retorna estatísticas de todos os caches"""
        with self._lock:
            stats = {}
            for name, cache in self._caches.items():
                stats[name] = {
                    'size': cache.size(),
                    'default_ttl': cache.default_ttl
                }
            return stats

# Decorator para cache automático
def cached(cache_name: str = 'default', ttl: int = None, key_func: Callable = None):
    """Decorator para cache automático de funções"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Gerar chave do cache
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Obter cache
            cache = cache_manager.get_cache(cache_name)
            
            # Tentar obter do cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Executar função e cachear resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Instância global do gerenciador de cache
cache_manager = CacheManager()

# Funções de conveniência
def get_user_cache() -> MemoryCache:
    """Obtém o cache de usuários"""
    return cache_manager.get_cache('users')

def get_aula_cache() -> MemoryCache:
    """Obtém o cache de aulas"""
    return cache_manager.get_cache('aulas')

def get_historico_cache() -> MemoryCache:
    """Obtém o cache de histórico"""
    return cache_manager.get_cache('historico')

def get_config_cache() -> MemoryCache:
    """Obtém o cache de configurações"""
    return cache_manager.get_cache('config')

# Função para limpeza periódica (pode ser chamada em background)
def periodic_cleanup():
    """Limpeza periódica dos caches"""
    if config.app.cache_enabled:
        results = cache_manager.cleanup_all()
        total_cleaned = sum(results.values())
        if total_cleaned > 0:
            from utils.logger import get_logger
            logger = get_logger('cache')
            logger.info(f"Cache cleanup: removed {total_cleaned} expired items")
