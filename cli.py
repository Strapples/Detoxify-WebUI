import argparse
import pandas as pd
from detoxify import Detoxify

def parse_txt_file(txt_path, delimiter="&brk"):
    with open(txt_path, "r", encoding="utf-8") as f:
        raw = f.read()
    return [x.strip() for x in raw.split(delimiter) if x.strip()]

def parse_csv_file(csv_path):
    df = pd.read_csv(csv_path)
    if "comment_text" not in df.columns:
        raise ValueError("CSV must contain a 'comment_text' column.")
    return df["comment_text"].tolist(), df

def main():
    parser = argparse.ArgumentParser(description="Score toxic content using Detoxify CLI")
    parser.add_argument("--input", required=True, help="Path to input .csv or .txt file")
    parser.add_argument("--output", default="results.csv", help="Output CSV file path")
    parser.add_argument("--model", default="original", help="Model type: original, unbiased, multilingual")
    parser.add_argument("--delimiter", default="&brk", help="Delimiter for TXT input (default: &brk)")
    args = parser.parse_args()

    try:
        print(f"Loading model: {args.model}")
        model = Detoxify(args.model)

        if args.input.endswith(".csv"):
            texts, df = parse_csv_file(args.input)
        elif args.input.endswith(".txt"):
            texts = parse_txt_file(args.input, args.delimiter)
            df = pd.DataFrame({"comment_text": texts})
        else:
            raise ValueError("Unsupported file type. Use .csv or .txt.")

        print(f"Scoring {len(texts)} entries...")
        results = model.predict(texts)

        for label in results:
            df[label] = results[label]

        df.to_csv(args.output, index=False)
        print(f"Saved results to {args.output}")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()