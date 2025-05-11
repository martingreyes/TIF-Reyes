from redis import Redis
import redis_lock # type: ignore
import os

class ResourceLockManager:
    def __init__(self):
        # Configuración del cliente Redis con los valores de host y puerto desde las variables de entorno
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))

        # Crear la conexión Redis
        self.redis_client = Redis(host=redis_host, port=redis_port, db=0)
        
        # Crear el objeto Lock usando la nueva API
        self.lock = redis_lock.Lock(self.redis_client, "bd_lock", expire=600, auto_renewal=True)

    def acquire(self):
        # Intentar obtener el lock, bloqueando hasta que sea adquirido
        return self.lock.acquire(blocking=True)

    def release(self):
        # Liberar el lock solo si está bloqueado
        if self.lock.locked():
            self.lock.release()

    def is_locked(self):
        # Verificar si el lock está actualmente adquirido
        return self.lock.locked()
