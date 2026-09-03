from abc import ABC, abstractmethod


class LanguageAdapter(ABC):

    @abstractmethod
    def can_handle(self, filename):
        pass

    @abstractmethod
    def analyze(self, filename):
        pass