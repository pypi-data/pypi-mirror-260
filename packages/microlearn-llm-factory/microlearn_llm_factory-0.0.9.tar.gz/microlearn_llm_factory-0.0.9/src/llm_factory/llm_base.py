from abc import ABC, abstractmethod


class LLMBase(ABC):
    @abstractmethod
    def _validate_args(self, **kwargs):
        pass

    @abstractmethod
    def _build_llm(self, **kwargs):
        pass

    def get_llm(self, **kwargs):
        """
        Returns a LLM instance.
        """
        self._validate_args(**kwargs)
        return self._build_llm(**kwargs)
