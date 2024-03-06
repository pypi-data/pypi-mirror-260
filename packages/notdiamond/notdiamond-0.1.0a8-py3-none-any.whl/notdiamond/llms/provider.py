from typing import Optional

from notdiamond import settings
from notdiamond.exceptions import UnsupportedLLMProvider

POSSIBLE_PROVIDERS = list(settings.PROVIDERS.keys())
POSSIBLE_MODELS = list(model for provider_values in settings.PROVIDERS.values() for values in provider_values.values()
                       if isinstance(values, list) for model in values)


class NDLLMProvider:

    def __init__(self, provider: str, model: str, api_key: Optional[str] = None):
        if provider not in POSSIBLE_PROVIDERS:
            raise UnsupportedLLMProvider(f"Given LLM provider {provider} is not in the list of supported providers.")
        if model not in POSSIBLE_MODELS:
            raise UnsupportedLLMProvider(f"Given LLM model {model} is not in the list of supported models.")

        self.provider = provider
        self.model = model
        self.api_key = api_key if api_key is not None else settings.PROVIDERS[provider]["api_key"]

    def prepare_for_request(self):
        return {"provider": self.provider, "model": self.model}
