import pandas as pd
from pathlib import Path
from twokenize import tokenize

INPUTS = [
    Path("code/EmotionDynamics/code/my_data/palisades_reddit.csv"),
    Path("code/EmotionDynamics/code/my_data/palisades_bluesky.csv"),
    Path("code/EmotionDynamics/code/my_data/texasff_reddit.csv"),
    Path("code/EmotionDynamics/code/my_data/texasff_bluesky.csv"),
    Path("code/EmotionDynamics/code/my_data/hurricane_milton_reddit.csv"),
    Path("code/EmotionDynamics/code/my_data/hurricane_milton_bluesky.csv"),
]
OUT_SUFFIX = "_cleaned.csv"

def clean_text(txt):
    txt = str(txt)
    tokens = tokenize(txt)
    # lowercase and filter tokens to only include those with alphabetic characters
    # filtered_tokens = [t.lower() for t in tokens if any(c.isalpha() for c in t)]
    # keep rows with at least 3 alphabetic tokens
    if len(tokens) < 3:
        return None
    return " ".join(tokens)

def run():
    for inp in INPUTS:
        df = pd.read_csv(inp)
        if "text" not in df.columns:
            raise ValueError(f"'text' column not found in {inp}")
        df["text"] = df["text"].apply(clean_text)
        out = inp.parent / (inp.stem + OUT_SUFFIX)
        out_df = df[df["text"].notna()]
        out_df.to_csv(out, index=False)
        print(f"Wrote {out} ({len(out_df)} rows)")

if __name__ == "__main__":
    run()