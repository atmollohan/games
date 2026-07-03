from abc import ABC, abstractmethod


class BaseGame(ABC):
    @abstractmethod
    def init_game(self) -> dict: ...

    @abstractmethod
    def state(self) -> dict: ...

    @abstractmethod
    def handle_action(self, action: dict) -> dict: ...
