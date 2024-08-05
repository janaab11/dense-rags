"""
script for downloading RAG dataset

Usage:
	download.py

Options:
"""

from docopt import docopt
import pandas as pd
import os

# Dataset: https://huggingface.co/datasets/enelpol/rag-mini-bioasq
TEXT_DATASET_URL = "hf://datasets/enelpol/rag-mini-bioasq/text-corpus/test-00000-of-00001.parquet"
EVAL_DATASET_URL = "hf://datasets/enelpol/rag-mini-bioasq/question-answer-passages/test-00000-of-00001.parquet"
EVAL_SIZE = 100

def get_output_paths():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return {
        "data": os.path.join(dir_path, "data.csv"),
        "eval": os.path.join(dir_path, "eval.csv"),
    }


def main():
    # download and clean dataset
    print(f'Downloading dataset from {"https://huggingface.co/datasets/enelpol/rag-mini-bioasq"}')
    data_df = pd.read_parquet(TEXT_DATASET_URL)
    eval_df = pd.read_parquet(EVAL_DATASET_URL).sample(EVAL_SIZE)

    # logic to create search space (for retrieval)
    passage_ids = eval_df["relevant_passage_ids"].to_list()
    passage_ids_list = [idx for id_list in passage_ids for idx in id_list]
    data_df["data"] = data_df["id"].apply(lambda idx: 1 if idx in passage_ids_list else 0)


    # save to output path
    paths = get_output_paths()
    data_df[data_df["data"] == 1][["passage"]].to_csv(paths["data"], index=False)
    eval_df[["question", "answer"]].to_csv(paths["eval"], index=False)
    print(f'Saved dataset to {paths["data"]}')
    return


if __name__ == "__main__":
    args = docopt(__doc__)

    main()
