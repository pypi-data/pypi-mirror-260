import time
from typing import Any, List, Dict, Optional, Union, Iterator

from langchain_core.messages import BaseMessageChunk, BaseMessage
from litellm import token_counter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from notdiamond import settings
from notdiamond.exceptions import ApiError
from notdiamond.llms.provider import NDLLMProvider
from notdiamond.prompts.prompt import NDPromptTemplate, NDChatPromptTemplate
from notdiamond.metrics.metric import NDMetric
from notdiamond.llms.request import model_select, report_latency
from notdiamond.types import NDApiKeyValidator


class NDLLM(LLM):
    """
    Custom implementation of NDLLM
    Starting reference is from here: https://python.langchain.com/docs/modules/model_io/llms/custom_llm
    """
    llm_providers: List[NDLLMProvider]
    api_key: str
    latency_tracking: bool = True
    default: int = 0

    def __init__(self, **kwargs):
        kwargs['api_key'] = kwargs['api_key'] if kwargs.get('api_key') else settings.NOTDIAMOND_API_KEY
        NDApiKeyValidator(api_key=kwargs.get('api_key'))
        kwargs['llm_providers'] = self._parse_llm_providers_data(kwargs.get('llm_providers'))

        super(NDLLM, self).__init__(**kwargs)

    @property
    def default_llm_provider(self):
        return self.llm_providers[self.default]

    @staticmethod
    def _parse_llm_providers_data(llm_providers: list) -> List[NDLLMProvider]:
        providers = []
        for llm_provider in llm_providers:
            if isinstance(llm_provider, NDLLMProvider):
                providers.append(llm_provider)
                continue
            split_items = llm_provider.split('/')
            provider = split_items[0]
            model = split_items[1]
            providers.append(NDLLMProvider(provider=provider, model=model))
        return providers

    @property
    def _llm_type(self) -> str:
        return "NotDiamond LLM"

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any, ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return "This function is deprecated for the latest LangChain version, use invoke instead"

    def invoke(self,
               prompt_template: Optional[Union[NDPromptTemplate, PromptTemplate,
                                               NDChatPromptTemplate, ChatPromptTemplate]] | str,
               input: Optional[Dict[str, Any]] = {},
               metric: NDMetric = NDMetric("accuracy"), **kwargs: Any) -> Any:
        if type(prompt_template) is not NDPromptTemplate or type(prompt_template) is not NDChatPromptTemplate:
            prompt_template = self._prepare_prompt_template(prompt_template)
        
        prompt_template.partial_variables = {**prompt_template.partial_variables, **input}
        
        best_llm, pipeline_id = model_select(prompt_template=prompt_template,
                                             llm_providers=self.llm_providers,
                                             metric=metric,
                                             notdiamond_api_key=self.api_key)
        if not best_llm:
            best_llm = self.default_llm_provider

        llm = self._llm_from_provider(best_llm)
        chain = prompt_template | llm

        if self.latency_tracking:
            result = self._invoke_with_latency_tracking(pipeline_id=pipeline_id, chain=chain,
                                                        model=best_llm.model, input=input)
        else:
            result = chain.invoke(input)

        return result, pipeline_id, best_llm

    def stream(self, input=None, **kwargs) -> Iterator[BaseMessageChunk]:
        """
        Stream the response from the LLM. A generator is returned. The generator yields chunks of the response.
        This is a wrapper around the `stream` method of an llm that returns a generator instead of the full response.
        """
        prompt_template = self._prepare_prompt_template(prompt_template=input)
        best_llm, pipeline_id = model_select(prompt_template=prompt_template,
                                             llm_providers=self.llm_providers,
                                             metric=NDMetric("accuracy"),
                                             notdiamond_api_key=self.api_key)
        if not best_llm:
            best_llm = self.default_llm_provider

        llm = self._llm_from_provider(best_llm)
        for chunk in llm.stream(input, **kwargs):
            yield chunk
    
    def openai_model_select(self,
                            prompt_template: Optional[Union[NDPromptTemplate, NDChatPromptTemplate]],
                            metric: NDMetric = NDMetric("accuracy")):
        if type(prompt_template) is not NDPromptTemplate or type(prompt_template) is not NDChatPromptTemplate:
            prompt_template = self._prepare_prompt_template(prompt_template)
        
        best_llm, _ = model_select(prompt_template=prompt_template,
                                   llm_providers=self.llm_providers,
                                   metric=metric,
                                   notdiamond_api_key=self.api_key)
        if not best_llm:
            best_llm = self.default_llm_provider

        return best_llm.model
    
    def model_select(self,
                     prompt_template: Optional[Union[NDPromptTemplate, PromptTemplate,
                                                     NDChatPromptTemplate, ChatPromptTemplate]] | str,
                     input: Optional[Dict[str, Any]] = {},
                     metric: NDMetric = NDMetric("accuracy"), **kwargs: Any) -> Any:
        if type(prompt_template) is not NDPromptTemplate or type(prompt_template) is not NDChatPromptTemplate:
            prompt_template = self._prepare_prompt_template(prompt_template)
        
        prompt_template.partial_variables = {**prompt_template.partial_variables, **input}
        
        best_llm, pipeline_id = model_select(prompt_template=prompt_template,
                                             llm_providers=self.llm_providers,
                                             metric=metric,
                                             notdiamond_api_key=self.api_key)
        
        return pipeline_id, best_llm

    def _invoke_with_latency_tracking(self, pipeline_id: str, chain, model: str,
                                      input: Optional[Dict[str, Any]] = {}):
        if pipeline_id == "NO-PIPELINE-ID" or pipeline_id == "":
            raise ApiError("ND pipeline id is not valid for latency tracking. Please check the API response.")

        start_time = time.time()
        result = chain.invoke(input)
        end_time = time.time()

        tokens_completed = token_counter(model=model, messages=[{"role": "assistant", "content": result.content}])
        tokens_per_second = tokens_completed / (end_time - start_time)

        report_latency(pipeline_id=pipeline_id, tokens_per_second=tokens_per_second, notdiamond_api_key=self.api_key)

        return result

    @staticmethod
    def _llm_from_provider(provider: NDLLMProvider) -> Any:
        if provider.provider == 'openai':
            return ChatOpenAI(openai_api_key=provider.api_key, model_name=provider.model)
        elif provider.provider == 'anthropic':
            return ChatAnthropic(anthropic_api_key=provider.api_key, model=provider.model)
        elif provider.provider == 'google':
            return ChatGoogleGenerativeAI(google_api_key=provider.api_key, model=provider.model)
        else:
            raise ValueError(f"Unsupported provider: {provider.provider}")

    @staticmethod
    def _prepare_prompt_template(prompt_template) -> NDPromptTemplate | NDChatPromptTemplate:
        if type(prompt_template) is str:
            return NDPromptTemplate(template=prompt_template)
        elif type(prompt_template) is PromptTemplate:
            return NDPromptTemplate.from_langchain_prompt_template(prompt_template)
        elif type(prompt_template) is NDPromptTemplate:
            return prompt_template
        elif type(prompt_template) is NDChatPromptTemplate:
            return prompt_template
        elif type(prompt_template) is ChatPromptTemplate:
            return NDChatPromptTemplate.from_langchain_chat_prompt_template(prompt_template)
        elif type(prompt_template) is list:
            if all(isinstance(pt, BaseMessage) for pt in prompt_template):
                return NDChatPromptTemplate.from_messages(prompt_template)
            else:
                raise ValueError(f"Unsupported prompt_template type {type(prompt_template)}")
        else:
            raise ValueError(f"Unsupported prompt_template type {type(prompt_template)}")
