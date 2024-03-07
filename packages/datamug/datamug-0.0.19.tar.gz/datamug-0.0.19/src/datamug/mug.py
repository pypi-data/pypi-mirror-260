import pandas as pd
from os.path import exists

from datamug.utils.models import (
    MistralChatContentFormatter,
    AnswerValidationModel,
    MugColor,
)
from datamug.utils.test import test_0
from datamug.reader.text_reader import TextReader

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.azureml_endpoint import (
    AzureMLEndpointApiType,
    AzureMLOnlineEndpoint,
)
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException


class Mug:
    def __init__(self):
        self.path_text = None

    @staticmethod
    def from_text(path: str) -> "Mug":
        __mug = Mug()
        __mug.path = path

        if not exists(path):
            raise FileNotFoundError(f"file {path} cannot be found")

        __mug.list_dict_qa = TextReader.to_dicts(path=path)

        return __mug

    def set_embeddings(
        self,
        model_name: str,
        type: str = "huggingface",
        encode_kwargs={"normalize_embeddings": True},
        model_kwargs={"device": "cpu"},
    ) -> "Mug":
        if type == "huggingface":
            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_name,  # Provide the pre-trained model's path
                model_kwargs=model_kwargs,  # Pass the model configuration options
                encode_kwargs=encode_kwargs,  # Pass the encoding options
            )
        else:
            raise NotImplementedError("This type hasn't been implemented yet.")

        return self

    def set_llm(self, kwargs: dict, type: str = "azure_ml_endpoint") -> "Mug":
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
        if type == "azure_ml_endpoint":
            self.llm = AzureMLOnlineEndpoint(
                content_formatter=MistralChatContentFormatter(),
                endpoint_api_type=AzureMLEndpointApiType.realtime,
                **kwargs,
            )
        else:
            raise NotImplementedError("This type hasn't been implemented yet.")

        return self

    def set_answer_builder_prompt(self, prompt_template: PromptTemplate) -> "Mug":
        """For usecases that u want to extend your answer with some structure based on given prompt. For example you have a small answer and you want to build explianed version of your answer

        Args:
            prompt_template (PromptTemplate): langchain prompt template

        Returns:
            Mug: _description_
        """
        __list_input_vars = prompt_template.input_variables

        self.chain_answer_builder = (
            RunnableParallel({f"{k}": RunnablePassthrough() for k in __list_input_vars})
            | prompt_template
            | self.llm
            | StrOutputParser()
        )

        return self

    def set_evaluator_prompt(self, prompt_template: PromptTemplate = None) -> "Mug":
        """After you build the new column based on the answer column (actual data in dataset) and answer_builder prompt, now u want to evaluate that if generated answer contextually is the same with actual answer.
            Keep this in mind this prompt should have 2 fields one is `actual_answer` another is `generated_answer`.

        Args:
            prompt_template (PromptTemplate): langchain prompt template

        Returns:
            Mug: _description_
        """

        if prompt_template is None:
            validation_template = """Given an actual answer and a generated answer, use a Language Model to compare these answers and return whether they match or not. The input is as below:

            Actual Answer: "{actual_answer}"

            Generated Answer: "{generated_answer}"
            """

            prompt_template = PromptTemplate.from_template(validation_template)

        __list_input_vars = prompt_template.input_variables

        if (
            "actual_answer" not in __list_input_vars
            or "generated_answer" not in __list_input_vars
        ):
            raise NotImplementedError(
                """U should have {actual_answer} and {generated_answer} in your prompt"""
            )

        prompt_template.template += (
            "Output Format Instructions: \n\n{format_instructions}\n\n"
        )

        __parser = PydanticOutputParser(pydantic_object=AnswerValidationModel)

        # Add parser to the prompt
        prompt_template.partial_variables = {
            "format_instructions": __parser.get_format_instructions()
        }

        self.chain_validaton = (
            RunnableParallel({f"{k}": RunnablePassthrough() for k in __list_input_vars})
            | prompt_template
            | self.llm
            | __parser
        )

        return self

    def grab(self, output_csv_name: str = "results", verbose=True):
        output_csv_name = output_csv_name.replace(".csv", "")
        list_new_qa = []
        for idx, qa in enumerate(self.list_dict_qa):

            dict_new_qa = {}
            dict_new_qa["question"] = qa["question"]
            dict_new_qa["actual_answer"] = qa["answer"]
            dict_new_qa["generated_answer"] = self.chain_answer_builder.invoke(
                {
                    "question": dict_new_qa["question"],
                    "answer": dict_new_qa["actual_answer"],
                }
            )
            dict_new_qa["is_valid"] = None
            dict_new_qa["exception"] = None
            try:
                dict_new_qa["is_valid"] = self.chain_validaton.invoke(
                    {
                        "generated_answer": dict_new_qa["generated_answer"],
                        "actual_answer": dict_new_qa["actual_answer"],
                    }
                ).is_correct
            except OutputParserException as e:
                dict_new_qa["exception"] = str(e)

            __msg = (
                MugColor.GREEN + f"{idx} validated"
                if dict_new_qa["is_valid"]
                else MugColor.RED + f"{idx} not validated"
            )
            print(__msg + MugColor.END)

            list_new_qa.append(dict_new_qa)

            self.df_result = pd.DataFrame(list_new_qa)
            self.df_result.to_csv(f"{output_csv_name}.csv")

        return self

    def report(self):
        __dict_result = {}
        __dict_result["instances"] = len(self.df_result)
        __dict_result["not_validated"] = self.df_result.loc[
            self.df_result["is_valid"].isna()
        ].shape[0]
        __dict_result["validated_successfully"] = (
            __dict_result["instances"] - __dict_result["not_validated"]
        )
        __dict_result["validated_as_True"] = self.df_result.loc[
            self.df_result["is_valid"] == True
        ].shape[0]
        __dict_result["validated_as_False"] = self.df_result.loc[
            self.df_result["is_valid"] == False
        ].shape[0]
        __dict_result[
            "validation_rate"
        ] = f"{round((__dict_result['validated_successfully']/__dict_result['instances'])*100,2)}%"

        __list_result = [{"metric": k, "value": v} for k, v in __dict_result.items()]

        __df_res = pd.DataFrame(__list_result)

        return __df_res
