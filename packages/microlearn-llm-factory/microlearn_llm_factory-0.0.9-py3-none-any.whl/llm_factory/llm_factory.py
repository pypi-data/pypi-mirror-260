"""
Factory class for LLM objects.
"""


class LLMFactory:
    """
    Factory class for LLMs.
    """
    LLM_OPENAI_CHAT_NAME = "openai_chat"
    _SUPPORTED_LLM_TYPES = [LLM_OPENAI_CHAT_NAME]

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LLMFactory, cls).__new__(
                cls, *args, **kwargs)
        return cls.instance

    def build_llm(self, llm_type: str, **kwargs):
        if llm_type == self.LLM_OPENAI_CHAT_NAME:
            from llm_factory.llm_openai_chat import LLMOpenAIChat
            return LLMOpenAIChat().get_llm(**kwargs)
        else:
            raise ValueError(f"Invalid llm_type: {llm_type}")

    def build_llm_default(self):
        from llm_factory.llm_openai_chat import LLMOpenAIChat
        kwargs = LLMOpenAIChat.get_default_args()
        return self.build_llm(
            llm_type=self.LLM_OPENAI_CHAT_NAME,
            **kwargs,
        )
