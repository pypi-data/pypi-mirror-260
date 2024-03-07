import os
import subprocess
from redis import Redis
from socket import socket
from pytest import fixture
from pytest_redis import factories

from blissdata.redis_engine.store import DataStore


def _find_available_port():
    with socket() as sock:
        sock.bind(("", 0))
        return sock.getsockname()[1]


redis_port = _find_available_port()
redis_db = factories.redis_noproc(host="localhost", port=redis_port, startup_timeout=1)


def pytest_configure(config):
    redis_args = [
        "redis-server",
        "--port",
        str(redis_port),
        "--loadmodule",
        os.path.join(os.getenv("CONDA_PREFIX", "/usr"), "lib", "librejson.so"),
        "--loadmodule",
        os.path.join(os.getenv("CONDA_PREFIX", "/usr"), "lib", "redisearch.so"),
        "--save ''",
    ]

    config._redis_proc = subprocess.Popen(
        redis_args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def pytest_unconfigure(config):
    config._redis_proc.kill()


@fixture
def redis_url(redis_db):
    url = f"redis://{redis_db.host}:{redis_db.port}"
    Redis.from_url(url).flushall()
    _ = DataStore(url, init_db=True)
    yield url


@fixture
def data_store(redis_url):
    data_store = DataStore(redis_url)
    try:
        yield data_store
    finally:
        data_store._redis.connection_pool.disconnect()
        data_store._redis = None
