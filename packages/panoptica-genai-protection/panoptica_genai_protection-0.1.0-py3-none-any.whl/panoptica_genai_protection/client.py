import httpx
import os
from logging import getLogger
from typing import Optional, Union

from panoptica_genai_protection.models import CheckPrompt, CheckPromptAnswer, CheckPromptResponse, UnknownErrorResponse
from panoptica_genai_protection.auth import GenAIProtectionAuth
from panoptica_genai_protection.settings import DEFAULT_BASE_URL

logger = getLogger("gen_ai_protection_client")


class GenAIProtectionClient:
    sync_methods = ["check_llm_prompt", "check_llm_response"]

    def __init__(self, access_key=None, secret_key=None, base_url=None, auth_host=None, as_async=False):
        self.base_url = base_url if base_url else os.getenv("GENAI_PROTECTION_BASE_URL", DEFAULT_BASE_URL)
        if self.base_url is None:
            raise ValueError("GENAI_PROTECTION_BASE_URL env var is None while a value is required")
        self.authorizer = GenAIProtectionAuth.get_instance(access_key, secret_key, auth_host)
        self.__async_replacements_set = False
        if as_async:
            self._set_async_implementations()

    @property
    def is_async(self):
        return self.__async_replacements_set

    def check_llm_prompt(self, prompt: str, api_name: str, api_endpoint_name: str, actor: Optional[str] = None,
                         actor_type: Optional[str] = None, role: Optional[str] = None,
                         sequence_id: Optional[str] = None) -> Union[CheckPromptResponse, UnknownErrorResponse]:
        request_body = CheckPrompt(prompt=prompt, apiName=api_name, apiEndpoint=api_endpoint_name,
                                   actor=actor, actorType=actor_type, role=role, seqId=sequence_id)
        response = self._post(f"{self.base_url}/checkLLMAgentPrompt", json=request_body.model_dump(mode='json'))

        result_model_class = CheckPromptResponse if response.is_success else UnknownErrorResponse
        result = result_model_class.model_validate(response.json())
        return result

    def check_llm_response(self, prompt: str, response: str, api_name: str, api_endpoint_name: str, req_id: str,
                           sequence_id: Optional[str] = None, actor: Optional[str] = None,
                           actor_type: Optional[str] = None, role: Optional[str] = None) -> CheckPromptResponse:
        request_body = CheckPromptAnswer(prompt=prompt, response=response, apiName=api_name,
                                         apiEndpoint=api_endpoint_name, seqId=sequence_id, actor=actor, reqId=req_id,
                                         actorType=actor_type, role=role)
        response = self._post(f"{self.base_url}/checkLLMAgentPromptResponse", json=request_body.model_dump(mode='json'))
        result_model_class = CheckPromptResponse if response.is_success else UnknownErrorResponse
        result = result_model_class.model_validate(response.json())
        return result

    async def check_llm_prompt_async(self, prompt: str, api_name: str, api_endpoint_name: str,
                                     actor: Optional[str] = None, actor_type: Optional[str] = None,
                                     role: Optional[str] = None, sequence_id: Optional[str] = None
                                     ) -> Union[CheckPromptResponse, UnknownErrorResponse]:
        request_body = CheckPrompt(prompt=prompt, apiName=api_name, apiEndpoint=api_endpoint_name,
                                   actor=actor, actorType=actor_type, role=role, seqId=sequence_id)
        response = await self._apost(f"{self.base_url}/checkLLMAgentPrompt", json=request_body.model_dump(mode='json'))
        result_model_class = CheckPromptResponse if response.is_success else UnknownErrorResponse
        result = result_model_class.model_validate(response.json())
        return result

    async def check_llm_response_async(self, prompt: str, response: str, api_name: str, api_endpoint_name: str,
                                       req_id: str, sequence_id: Optional[str] = None, actor: Optional[str] = None,
                                       actor_type: Optional[str] = None, role: Optional[str] = None
                                       ) -> CheckPromptResponse:
        request_body = CheckPromptAnswer(prompt=prompt, response=response, apiName=api_name,
                                         apiEndpoint=api_endpoint_name, seqId=sequence_id, actor=actor, reqId=req_id,
                                         actorType=actor_type, role=role)
        response = await self._apost(f"{self.base_url}/checkLLMAgentPromptResponse", json=request_body.model_dump(mode='json'))
        result_model_class = CheckPromptResponse if response.is_success else UnknownErrorResponse
        result = result_model_class.model_validate(response.json())
        return result

    def _get_and_prep_headers(self, kwargs):
        headers = kwargs.pop("headers", {})
        headers["jwt"] = self.authorizer.get_token()
        return headers

    def _post(self, url, *args, **kwargs):
        headers = self._get_and_prep_headers(kwargs)
        return httpx.post(url, *args, **kwargs, headers=headers)

    async def _apost(self, url, *args, **kwargs):
        headers = self._get_and_prep_headers(kwargs)
        async with httpx.AsyncClient() as http_client:
            result = await http_client.post(url, *args, **kwargs, headers=headers)
        return result

    async def __aenter__(self):
        self._set_async_implementations()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._unset_async_implementations()

    def _unset_async_implementations(self):
        for sync_method_name in self.sync_methods:
            sync_method_backup_name = f"{sync_method_name}_sync"
            sync_method = getattr(self, sync_method_backup_name, None)
            if sync_method:
                setattr(self, sync_method_name, sync_method)
        self.__async_replacements_set = False

    def _set_async_implementations(self):
        for sync_method_name in self.sync_methods:
            async_method_name = f"{sync_method_name}_async"
            async_method = getattr(self, async_method_name, None)
            if async_method:
                setattr(self, f"{sync_method_name}_sync", getattr(self, sync_method_name))
                setattr(self, sync_method_name, async_method)
        self.__async_replacements_set = True
