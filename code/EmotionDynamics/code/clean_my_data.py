import pandas as pd
import re
from pathlib import Path

INPUTS = [
    Path("code/EmotionDynamics/code/my_data/palisades_reddit_filtered.csv"),
    Path("code/EmotionDynamics/code/my_data/palisades-fire-bluesky.csv"),
]
OUT_SUFFIX = "_cleaned.csv"

# temporarily using without twTokenizer because I couldn't find it.
# may use tweet tokenizer from nltkw

def clean_text(txt):
    txt = str(txt)
    tokens = re.findall(r"[A-Za-z']+", txt)
    toks = " ".join(tokens).lower()
    # keep rows with at least 3 alphabetic tokens
    alpha_count = sum(1 for t in toks.split() if any(c.isalpha() for c in t))
    if alpha_count < 3:
        return None
    return toks

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