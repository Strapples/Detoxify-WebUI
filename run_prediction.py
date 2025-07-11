import argparse
import os

import pandas as pd
from detoxify import Detoxify


def load_input_text(input_obj):
    """Accepts a path to a .csv or .txt file, or a raw string.
    For CSVs, assumes there's a 'comment_text' column.
    For .txt files, returns a list of strings (one per line).
    For raw strings, returns the string as-is."""

    if isinstance(input_obj, str) and os.path.isfile(input_obj):
        if input_obj.endswith(".csv"):
            df = pd.read_csv(input_obj)
            if "comment_text" not in df.columns:
                raise ValueError("CSV file must contain a 'comment_text' column.")
            return df["comment_text"].tolist()
        elif input_obj.endswith(".txt"):
            return open(input_obj).read().splitlines()
        else:
            raise ValueError("Unsupported file type: must be .txt or .csv")
    elif isinstance(input_obj, str):
        return input_obj
    else:
        raise ValueError("Invalid input: must be a string or a valid file path.")


def run(model_name, input_obj, dest_file, from_ckpt, device="cpu"):
    """Loads model from checkpoint or from model name and runs inference on the input_obj.
    Displays results as a pandas DataFrame object.
    If a dest_file is given, it saves the results to a txt file.
    """
    text = load_input_text(input_obj)
    if model_name is not None:
        model = Detoxify(model_name, device=device)
    else:
        model = Detoxify(checkpoint=from_ckpt, device=device)
    res = model.predict(text)

    res_df = pd.DataFrame(
        res,
        index=[text] if isinstance(text, str) else text,  # pyright: ignore[reportArgumentType]
    ).round(5)
    print(res_df)
    if dest_file is not None:
        res_df.index.name = "input_text"
        res_df.to_csv(dest_file)

    return res


if __name__ == "__main__":
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        help="text, list of strings, or txt file",
    )
    parser.add_argument(
        "--model_name",
        default="unbiased",
        type=str,
        help="Name of the torch.hub model (default: unbiased)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        type=str,
        help="device to load the model on",
    )
    parser.add_argument(
        "--from_ckpt_path",
        default=None,
        type=str,
        help="Option to load from the checkpoint path (default: False)",
    )
    parser.add_argument(
        "--save_to",
        default=None,
        type=str,
        help="destination path to output model results to (default: None)",
    )

    args = parser.parse_args()

    assert args.from_ckpt_path is not None or args.model_name is not None

    if args.model_name is not None:
        assert args.model_name in [
            "original",
            "unbiased",
            "multilingual",
        ]

    if args.from_ckpt_path is not None and args.model_name is not None:
        raise ValueError(
            "Please specify only one model source, can either load model from checkpoint path or from model_name."
        )
    if args.from_ckpt_path is not None:
        assert os.path.isfile(args.from_ckpt_path)

    run(
        args.model_name,
        args.input,
        args.save_to,
        args.from_ckpt_path,
        device=args.device,
    )
