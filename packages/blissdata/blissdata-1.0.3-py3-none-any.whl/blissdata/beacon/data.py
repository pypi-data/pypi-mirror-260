"""Get Bliss data information from Beacon."""

import struct
from ._base import BeaconClient
from ._base import IncompleteBeaconMessage


class BeaconData(BeaconClient):
    """Provides the API to read the redis databases urls."""

    REDIS_QUERY = 30
    REDIS_QUERY_ANSWER = 31

    REDIS_DATA_SERVER_QUERY = 32
    REDIS_DATA_SERVER_FAILED = 33
    REDIS_DATA_SERVER_OK = 34

    def get_redis_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss settings.
        For example 'redis://foobar:25001' or 'unix:///tmp/redis.sock'."""
        msg = b"%s%s" % (struct.pack("<ii", self.REDIS_QUERY, 0), b"")
        self._connection.sendall(msg)
        data = b""
        while True:
            raw_data = self._connection.recv(16 * 1024)
            if not raw_data:
                break
            data = b"%s%s" % (data, raw_data)
            try:
                message_type, message, data = self._unpack_message(data)
            except IncompleteBeaconMessage:
                continue
            break
        if message_type != self.REDIS_QUERY_ANSWER:
            raise RuntimeError(f"Unexpected message type '{message_type}'")
        host, port = message.decode().split(":")
        if host == "localhost":
            return f"unix://{port}"
        else:
            return f"redis://{host}:{port}"

    def get_redis_data_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss scan data.
        For example 'redis://foobar:25002' or 'unix:///tmp/redis_data.sock'."""
        response = self._request(self.REDIS_DATA_SERVER_QUERY, "")
        response_type, data = response.read()
        if response_type == self.REDIS_DATA_SERVER_OK:
            host, port = data.decode().split("|")[:2]
            if host == "localhost":
                return f"unix://{port}"
            else:
                return f"redis://{host}:{port}"
        elif response_type == self.REDIS_DATA_SERVER_FAILED:
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response_type}")
