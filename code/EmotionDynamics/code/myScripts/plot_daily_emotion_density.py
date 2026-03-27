import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths for cleaned output from avgEmoValues - organized by dataset and platform
DATASETS = ["palisades", "texasff", "hurricane_milton"]

def get_paths(dataset_name):
    return {
        "reddit": {
            "positive": Path(f"code/EmotionDynamics/code/my_data/output_{dataset_name}_reddit_positive/val.csv"),
            "negative": Path(f"code/EmotionDynamics/code/my_data/output_{dataset_name}_reddit_negative/val.csv"),
        },
        "bluesky": {
            "positive": Path(f"code/EmotionDynamics/code/my_data/output_{dataset_name}_bluesky_positive/val.csv"),
            "negative": Path(f"code/EmotionDynamics/code/my_data/output_{dataset_name}_bluesky_negative/val.csv"),
        },
    }


def load_and_agg(path):
    df = pd.read_csv(path)
    # Standardize date column name if available
    if "created_iso" in df.columns:
        df["date"] = pd.to_datetime(df["created_iso"]).dt.date
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    else:
        # fallback to first timestamp-like column
        for c in df.columns:
            if "time" in c.lower() or "date" in c.lower():
                df["date"] = pd.to_datetime(df[c], errors="coerce").dt.date
                break

    # if still missing date, fail
    if "date" not in df.columns:
        raise ValueError(f"No date column found in {path}")

    # use lexRatio if exists else use avgLexVal
    if "lexRatio" in df.columns:
        metric = "lexRatio"
    elif "avgLexVal" in df.columns:
        metric = "avgLexVal"
    else:
        raise ValueError(f"No lexRatio or avgLexVal column in {path}")

    agg = df.groupby("date")[metric].mean().rename("density").to_frame()
    return agg


def plot_month_daily():
    for dataset_name in DATASETS:
        paths = get_paths(dataset_name)
        for platform in ["reddit", "bluesky"]:
            pos = load_and_agg(paths[platform]["positive"])
            neg = load_and_agg(paths[platform]["negative"])

            merged = pd.DataFrame({"positive": pos["density"], "negative": neg["density"]})
            merged = merged.dropna(how="all")
            merged = merged.sort_index()

            if len(merged) > 31:
                merged = merged.iloc[-31:]

            merged_smooth = merged.rolling(3, min_periods=1, center=True).mean()

            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(merged_smooth.index, merged_smooth["negative"], label="Negative", color="red", linewidth=2)
            ax.plot(merged_smooth.index, merged_smooth["positive"], label="Positive", color="blue", linewidth=2)
            ax.scatter(merged.index, merged["negative"], color="pink", alpha=0.4, s=12)
            ax.scatter(merged.index, merged["positive"], color="skyblue", alpha=0.4, s=12)
            ax.set_title(f"{dataset_name.capitalize()} - {platform.capitalize()} daily emotion-word density")
            ax.set_ylabel("Emotion-word density")
            ax.set_xlabel("Date")
            ax.legend()
            ax.grid(alpha=0.25)
            fig.autofmt_xdate(rotation=45)
            out = Path(f"code/EmotionDynamics/code/plottingOutput/{dataset_name}/daily_emotion_density_{dataset_name}_{platform}.png")
            out.parent.mkdir(parents=True, exist_ok=True)
            plt.tight_layout()
            plt.savefig(out, dpi=150)
            plt.close(fig)
            print(f"Saved plot to {out}")


if __name__ == "__main__":
    plot_month_daily()
