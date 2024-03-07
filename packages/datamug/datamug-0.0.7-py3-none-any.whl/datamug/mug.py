from utils.test import test_0
from datamug.utils.models import (
    MistralChatContentFormatter
)
from datamug.reader.text_reader import TextReader
from os.path import exists
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.azureml_endpoint import AzureMLOnlineEndpoint
from langchain_community.llms.azureml_endpoint import (
    AzureMLEndpointApiType,
)
class Mug:



    def __init__(self):
        self.path_text = None
        

    @staticmethod
    def from_text(path:str) -> "Mug":
        __mug = Mug()
        __mug.path = path

        
        # if not exists(path):
            # raise FileNotFoundError(f'file {path} cannot be found')
        
        # __mug.list_dict_qa = TextReader.to_dicts(path=path)
        test_0()

        return __mug

    def set_embeddings(self, model_name:str,type:str='huggingface',encode_kwargs={'normalize_embeddings': True},model_kwargs={'device':'cpu'}) -> "Mug":
        if type == 'huggingface':
            self.embeddings = HuggingFaceEmbeddings(
                model_name='BAAI/bge-large-en-v1.5',     # Provide the pre-trained model's path
                model_kwargs={'device':'cpu'}, # Pass the model configuration options
                encode_kwargs={'normalize_embeddings': True} # Pass the encoding options
            )
        else:
            raise NotImplementedError('This type hasn\'t been implemented yet.')


    def set_llm(self, kwargs:dict ,type:str='azure_ml_endpoint') -> "Mug":
        """_summary_

        Args:
            kwargs (dict): _description_. for example for azureMLEndpoin:
            {
                endpoint_url="https://xxx.region.inference.ml.azure.com/score",
                endpoint_api_key="yyy",
                model_kwargs={"temperature": 0, "max_new_tokens": 1024},
            }

            type (str, optional): _description_. Defaults to 'azure_ml_endpoint'.
        """
        if type=='azure_ml_endpoint':
            self.llm = AzureMLOnlineEndpoint(
                content_formatter=MistralChatContentFormatter(),
                **kwargs
            )
        else:
            raise NotImplementedError('This type hasn\'t been implemented yet.')
        
