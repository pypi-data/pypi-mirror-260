from typing import List
import pandas as pd


class TextReader:
    def __init__(self) -> None:
        pass

    @staticmethod
    def to_dicts(path: str) -> List[dict]:
        qa_list = []
        with open(path, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                question = lines[i].strip()
                answer = lines[i + 1].strip()
                qa_list.append({"question": question, "answer": answer})
        return qa_list

    @staticmethod
    def to_pandas(path: str) -> pd.DataFrame:
        return pd.DataFrame(TextReader.to_dicts(path=path))
