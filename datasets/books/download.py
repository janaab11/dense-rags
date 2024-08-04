"""
script for downloading RAG dataset

Usage:
	download.py [--path <path>]

Options:
  --path <output-path>              filepath to save dataset [default: use-default]
"""

from docopt import docopt
import pandas as pd
import os

# Dataset: https://huggingface.co/datasets/Eitanli/goodreads
HF_DATASET_URL = "hf://datasets/Eitanli/goodreads/goodreads_data.csv"


def main(output_path):
    # download and clean dataset
    print(f"Downloading dataset from {HF_DATASET_URL}")
    df = pd.read_csv(HF_DATASET_URL)
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.assign(genre_len=lambda x: len(x['Genres']))
    df = df[df['genre_len'] > 0]
    df = df[['Book', 'Description']]

    # save to output path
    if output_path == "use-default":
        dir_path = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(dir_path, "data.csv")
    df.sample(n=1000).to_csv(output_path, index=False)
    print(f"Saved dataset to {output_path}")
    return


if __name__ == "__main__":
    args = docopt(__doc__)
    output_path = args["--path"]

    main(output_path)
