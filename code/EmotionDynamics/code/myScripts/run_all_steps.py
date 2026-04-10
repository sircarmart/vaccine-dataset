#!/usr/bin/env python
"""
Run steps 2-4 for all datasets with organized output folders.
"""
import subprocess
import os
from pathlib import Path

# Base paths
MY_DATA = Path("code/EmotionDynamics/code/my_data")
LEX_PATH = Path("code/EmotionDynamics/lexicons")

# Dataset configurations
DATASETS = [
    {
        "name": "palisades",
        "reddit": MY_DATA / "palisades_reddit_cleaned.csv",
        "bluesky": MY_DATA / "palisades_bluesky_cleaned.csv",
    },
    {
        "name": "texasff",
        "reddit": MY_DATA / "texasff_reddit_cleaned.csv",
        "bluesky": MY_DATA / "texasff_bluesky_cleaned.csv",
    },
    {
        "name": "hurricane_milton",
        "reddit": MY_DATA / "hurricane_milton_reddit_cleaned.csv",
        "bluesky": MY_DATA / "hurricane_milton_bluesky_cleaned.csv",
    },
]

def run_step2():
    """Run Step 2: Compute emotion metrics for positive/negative lexicons."""
    print("\n" + "="*80)
    print("STEP 2: Computing emotion metrics (positive/negative lexicons)")
    print("="*80)
    
    for dataset in DATASETS:
        name = dataset["name"]
        print(f"\n--- Processing {name} ---")
        
        # Reddit - Positive
        cmd = [
            "python", "code/EmotionDynamics/code/avgEmoValues.py",
            "--dataPath", str(dataset["reddit"]),
            "--lexPath", str(LEX_PATH / "NRC_EmoLex_positive.csv"),
            "--lexNames", "val",
            "--savePath", str(MY_DATA / f"output_{name}_reddit_positive")
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        # Reddit - Negative
        cmd = [
            "python", "code/EmotionDynamics/code/avgEmoValues.py",
            "--dataPath", str(dataset["reddit"]),
            "--lexPath", str(LEX_PATH / "NRC_EmoLex_negative.csv"),
            "--lexNames", "val",
            "--savePath", str(MY_DATA / f"output_{name}_reddit_negative")
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        # Bluesky - Positive
        cmd = [
            "python", "code/EmotionDynamics/code/avgEmoValues.py",
            "--dataPath", str(dataset["bluesky"]),
            "--lexPath", str(LEX_PATH / "NRC_EmoLex_positive.csv"),
            "--lexNames", "val",
            "--savePath", str(MY_DATA / f"output_{name}_bluesky_positive")
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        # Bluesky - Negative
        cmd = [
            "python", "code/EmotionDynamics/code/avgEmoValues.py",
            "--dataPath", str(dataset["bluesky"]),
            "--lexPath", str(LEX_PATH / "NRC_EmoLex_negative.csv"),
            "--lexNames", "val",
            "--savePath", str(MY_DATA / f"output_{name}_bluesky_negative")
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    
    print("\n✓ Step 2 complete!")

if __name__ == "__main__":
    run_step2()
