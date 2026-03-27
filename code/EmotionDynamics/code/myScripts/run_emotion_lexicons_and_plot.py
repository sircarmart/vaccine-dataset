import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path("code/EmotionDynamics")

# Define all datasets with their file paths
DATASETS = {
    "palisades": {
        "reddit": BASE / "code/my_data/palisades_reddit_filtered_cleaned.csv",
        "bluesky": BASE / "code/my_data/palisades-fire-bluesky_cleaned.csv",
    },
    "texasff": {
        "reddit": BASE / "code/my_data/texasff_reddit_cleaned.csv",
        "bluesky": BASE / "code/my_data/texasff_bluesky_cleaned.csv",
    },
    "hurricane_milton": {
        "reddit": BASE / "code/my_data/hurricane_milton_reddit_cleaned.csv",
        "bluesky": BASE / "code/my_data/hurricane_milton_bluesky_cleaned.csv",
    },
}

# Generate these lexicons for each dataset/platform.
# We keep positive/negative outputs available for the daily pos/neg workflow.
EMOTIONS_TO_RUN = [
    ("positive", "lexicons/NRC_EmoLex_positive.csv"),
    ("negative", "lexicons/NRC_EmoLex_negative.csv"),
    ("fear", "lexicons/NRC_EmoLex_fear.csv"),
    ("trust", "lexicons/NRC_EmoLex_trust.csv"),
    ("sadness", "lexicons/NRC_EmoLex_sadness.csv"),
    ("anticipation", "lexicons/NRC_EmoLex_anticipation.csv"),
    ("anger", "lexicons/NRC_EmoLex_anger.csv"),
    ("disgust", "lexicons/NRC_EmoLex_disgust.csv"),
    ("joy", "lexicons/NRC_EmoLex_joy.csv"),
    ("surprise", "lexicons/NRC_EmoLex_surprise.csv"),
]

# Only these emotions are shown in the 8-emotions plot.
PLOT_EMOTIONS = [
    "fear",
    "trust",
    "sadness",
    "anticipation",
    "anger",
    "disgust",
    "joy",
    "surprise",
]

OUTPUT_ROOT = BASE / "code/my_data"


def run_avg_emo_values(data_path, lex_path, save_path):
    save_path.mkdir(parents=True, exist_ok=True)
    cmd = [
        "python",
        str(BASE / "code/avgEmoValues.py"),
        "--dataPath",
        str(data_path),
        "--lexPath",
        str(lex_path),
        "--lexNames",
        "val",
        "--savePath",
        str(save_path),
    ]
    print("Running", " ".join(cmd))
    subprocess.run(cmd, check=True)


def process_for_dataset(dataset_name, platform):
    data_path = DATASETS[dataset_name][platform]
    emotion_outputs = {}
    for emotion, lex_file in EMOTIONS_TO_RUN:
        lex_path = BASE / lex_file
        out_dir = OUTPUT_ROOT / f"output_{dataset_name}_{platform}_{emotion}"
        run_avg_emo_values(data_path, lex_path, out_dir)
        emotion_outputs[emotion] = out_dir / "val.csv"
    return emotion_outputs


def load_daily_density(path):
    df = pd.read_csv(path)
    if "created_iso" in df.columns:
        df["date"] = pd.to_datetime(df["created_iso"]).dt.date
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    else:
        raise ValueError("No date column found")
    if "lexRatio" in df.columns:
        metric = "lexRatio"
    elif "avgLexVal" in df.columns:
        metric = "avgLexVal"
    else:
        raise ValueError("No lexRatio or avgLexVal column")
    agg = df.groupby("date")[metric].mean().rename("density")
    return agg


def plot_density(dataset_name, platform, emotion_outputs):
    df = pd.DataFrame()
    for emotion in PLOT_EMOTIONS:
        p = emotion_outputs.get(emotion)
        if p is None:
            print("Missing output path for", emotion)
            continue
        if not p.exists():
            print("Missing file", p)
            continue
        df[emotion] = load_daily_density(p)

    df = df.sort_index()
    if len(df) > 31:
        df = df.iloc[-31:]
    df_smooth = df.rolling(3, min_periods=1, center=True).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = {
        "fear": "red",
        "trust": "blue",
        "sadness": "orange",
        "anticipation": "green",
        "anger": "brown",
        "disgust": "magenta",
        "joy": "olive",
        "surprise": "cyan",
    }
    for emotion in df.columns:
        ax.plot(df_smooth.index, df_smooth[emotion], label=emotion, color=colors.get(emotion, None), linewidth=2)

    ax.set_title(f"{dataset_name.capitalize()} - {platform.capitalize()} daily emotion-word density")
    ax.set_xlabel("Date")
    ax.set_ylabel("Emotion-word density")
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    fig.autofmt_xdate(rotation=45)
    out = BASE / f"code/plottingOutput/{dataset_name}/daily_emotion_density_{dataset_name}_{platform}_8emotions.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print("Saved plot:", out)


def main():
    # run metrics for each dataset and platform
    for dataset_name in DATASETS.keys():
        for platform in ["reddit", "bluesky"]:
            print(f"Processing {dataset_name} - {platform}")
            emotion_outputs = process_for_dataset(dataset_name, platform)
            plot_density(dataset_name, platform, emotion_outputs)


if __name__ == "__main__":
    main()
