from typing import List, Dict
import json

from langchain_community.llms.azureml_endpoint import (
    AzureMLEndpointApiType,
    
    ContentFormatterBase
)
from langchain_community.llms.azureml_endpoint import AzureMLOnlineEndpoint

from langchain_core.outputs import Generation, LLMResult


class MistralChatContentFormatter(ContentFormatterBase):
    """Content formatter for Mistral Chat"""

    @property
    def supported_api_types(self) -> List[AzureMLEndpointApiType]:
        return [AzureMLEndpointApiType.realtime, AzureMLEndpointApiType.serverless]

    def format_request_payload(
        self, prompt: str, model_kwargs: Dict, api_type: AzureMLEndpointApiType
    ) -> bytes:
        """Formats the request according to the chosen api"""
        prompt = ContentFormatterBase.escape_special_characters(prompt)

        if api_type == AzureMLEndpointApiType.realtime:
            request_payload = json.dumps(
                {
                    "input_data": {
                        "input_string": [{
                            'role':'user',
                            'content': prompt
                        }],
                        "parameters": model_kwargs,
                    }
                }
            )
        elif api_type == AzureMLEndpointApiType.serverless:
            request_payload = json.dumps({"prompt": prompt, **model_kwargs})
        else:
            raise ValueError(
                f"`api_type` {api_type} is not supported by this formatter"
            )
        return str.encode(request_payload)

    def format_response_payload(
        self, output: bytes, api_type: AzureMLEndpointApiType
    ) -> Generation:
        """Formats response"""
        if api_type == AzureMLEndpointApiType.realtime:
            try:
                choice = json.loads(output)["output"]
            except (KeyError, IndexError, TypeError) as e:
                raise ValueError(self.format_error_msg.format(api_type=api_type)) from e
            return Generation(text=choice)
        if api_type == AzureMLEndpointApiType.serverless:
            try:
                choice = json.loads(output)["choices"][0]
                if not isinstance(choice, dict):
                    raise TypeError(
                        "Endpoint response is not well formed for a chat "
                        "model. Expected `dict` but `{type(choice)}` was "
                        "received."
                    )
            except (KeyError, IndexError, TypeError) as e:
                raise ValueError(self.format_error_msg.format(api_type=api_type)) from e
            return Generation(
                text=choice["text"].strip(),
                generation_info=dict(
                    finish_reason=choice.get("finish_reason"),
                    logprobs=choice.get("logprobs"),
                ),
            )
        raise ValueError(f"`api_type` {api_type} is not supported by this formatter")
