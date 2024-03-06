from openai import APIStatusError, ChatCompletion, AzureOpenAI
from typing import List, Optional, Iterator
from langchain_openai import AzureOpenAIEmbeddings
from ...typings.ai import AiModel, AiModelTokenManager, AiMessageRole, AiPrompt, Vector
from ...exceptions import raise_oai_error, OaiCompletionAPINonStopFinishReasonError


class AzureAiModel(AiModel):
    def __init__(self, *, deployment: str,
                 azure_endpoint: str,
                 azure_api_key: str,
                 azure_api_version: str,
                 token_manager: Optional[AiModelTokenManager] = None,
                 tpm: int,
                 max_token: int
                 ):
        self.__azure_endpoint = azure_endpoint
        self.__api_key = azure_api_key
        self.__azure_api_version = azure_api_version
        self.__deployment = deployment
        self.__token_manager = token_manager
        self.__tpm = tpm
        self.__max_token = max_token

    @property
    def tpm(self):
        return self.__tpm

    @property
    def max_token(self):
        return self.__max_token

    @property
    def endpoint(self):
        return self.__azure_endpoint

    @property
    def api_version(self):
        return self.__azure_api_version

    @property
    def deployment(self):
        return self.__deployment

    def process(self, prompts: List[AiPrompt]) -> List[AiPrompt]:
        require_token = AiModel.messages_tokens(prompts)
        self.__wait_allow_token(require_token)
        client = self.get_autocomplete_client()
        try:
            completion = client.chat.completions.create(
                model=self.deployment,
                messages=AiPrompt.to_oai_dicts(prompts)
            )
            return prompts + self.__parse_response(completion)
        except APIStatusError as e:
            raise_oai_error(e)

    def stream(self, prompts: List[AiPrompt]) -> Iterator[List[AiPrompt]]:
        require_token = AiModel.messages_tokens(prompts)
        self.__wait_allow_token(require_token)
        client = self.get_autocomplete_client()
        streamed_response: str = ""
        try:
            # with client.chat.completions.with_streaming_response.create(
            #         messages=AiPrompt.to_oai_dicts(prompts),
            #         model=self.deployment,
            # ) as response:
            #     print("created, start to iterate")
            #     for text in response.iter_lines():
            #
            #         streamed_response += text
            #         print("streamed_response: ", streamed_response)
            #         yield prompts + [
            #             AiPrompt(
            #                 role=AiMessageRole.assistant,
            #                 content=streamed_response
            #             )
            #         ]

            response = client.chat.completions.create(messages=AiPrompt.to_oai_dicts(prompts), model=self.deployment, stream=True)
            streamed_response = ""
            for chunk in response:
                if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                    streamed_response += chunk.choices[0].delta.content
                    yield prompts + [
                        AiPrompt(
                            role=AiMessageRole.assistant,
                            content=streamed_response
                        )
                    ]
        except APIStatusError as e:
            raise_oai_error(e)

    def embed_texts(self, texts: str | List[str]) -> Vector | List[Vector]:
        require_token = AiModel.string_tokens("".join(texts) if isinstance(texts, list) else texts)
        self.__wait_allow_token(require_token)
        client = self.get_text_embedding_client()
        if isinstance(texts, list): return client.embed_documents(texts)
        return client.embed_query(texts)

    def get_autocomplete_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_version=self.__azure_api_version,
            azure_endpoint=self.__azure_endpoint,
            azure_deployment=self.__deployment,
            api_key=self.__api_key
        )

    def get_text_embedding_client(self) -> AzureOpenAIEmbeddings:
        return AzureOpenAIEmbeddings(
            openai_api_version=self.__azure_api_version,
            azure_endpoint=self.__azure_endpoint,
            azure_deployment=self.__deployment,
            openai_api_key=self.__api_key
        )

    def __parse_response(self, completion: ChatCompletion) -> List[AiPrompt]:
        if isinstance(completion, APIStatusError) or hasattr(completion, "error"): raise completion
        prompts: List[AiPrompt] = []
        for choice in completion.choices:
            if choice.finish_reason != 'stop':
                raise OaiCompletionAPINonStopFinishReasonError(choice.finish_reason)
            prompts.append(AiPrompt(role=AiMessageRole.assistant, content=choice.message.content))
        return prompts

    def __wait_allow_token(self, require_token: int):
        assert require_token <= self.tpm, f"Token requirement [{require_token}] exceeded model {self.deployment} tpm {self.tpm}"
        if self.__token_manager is not None:
            self.__token_manager.wait_for_allow(require_token=require_token, ai_model=self)
