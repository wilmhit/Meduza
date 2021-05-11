import abc
from threading import Thread
from typing import Tuple, Any

class BaseServer(abc.ABC):

    @abc.abstractmethod
    def _main_loop(self):
        pass

    @abc.abstractmethod
    def _thread_local(self) -> Tuple[Any]:
        pass

    def _run(self):
        args = self._thread_local()
        while self._running:
            self._main_loop(*args)

    def start(self):
        self._running = True
        self._server_thread = Thread(target=self._run)
        self._server_thread.start()
    
    def stop(self):
        self._running = False
        self._server_thread.join()
