import abc
from threading import Thread
from typing import Tuple, Any


class BaseServer(abc.ABC):
    @abc.abstractmethod
    def _main_loop(self):
        """
        Use this function instead of creating your own loop. It is
        called every loop iteration like this:
        ```
        while server_running:
            _main_loop(*args)
        ```
        """
        pass

    def _thread_local(self) -> Tuple[Any]:
        """
        Return value of this function should be a tuple. It will be
        doconstructed and passed in as arguments to _main_loop every
        loop iteration. Values returned are not shared between threads.
        """
        pass

    def _run(self):
        args = self._thread_local()
        while self._running:
            if args:
                self._main_loop(*args)
            else:
                self._main_loop()

    def wait_for_join(self):
        """Blocks execution until thread is finished"""
        self._server_thread.join()

    def start(self):
        """Will start running _main_loop on separate thread."""
        self._running = True
        self._server_thread = Thread(target=self._run)
        self._server_thread.start()

    def stop(self):
        """
        Will try to stop _main_loop. This will finish current loop
        iteration so it may take a while. Function blocks execution
        until then.
        """
        self._running = False
        self._server_thread.join()
