# User-added EmotionDynamics workflow

This folder contains custom scripts and generated plots.

## Step 1: Preprocess raw data

Run the cleaning script (uses regex tokenization and filters short tweets):

```bash
python code/EmotionDynamics/code/myScripts/clean_my_data.py
```

This generates:
- `code/EmotionDynamics/code/my_data/palisades_reddit_filtered_cleaned.csv`
- `code/EmotionDynamics/code/my_data/palisades-fire-bluesky_cleaned.csv`

## Step 2: Compute emotion metrics (avgEmoValues)

Run these commands for positive and negative lexicons:

```bash
python code/EmotionDynamics/code/avgEmoValues.py --dataPath code/EmotionDynamics/code/my_data/palisades_reddit_filtered_cleaned.csv --lexPath code/EmotionDynamics/lexicons/NRC_EmoLex_positive.csv --lexNames val --savePath code/EmotionDynamics/code/my_data/output_reddit_positive
python code/EmotionDynamics/code/avgEmoValues.py --dataPath code/EmotionDynamics/code/my_data/palisades_reddit_filtered_cleaned.csv --lexPath code/EmotionDynamics/lexicons/NRC_EmoLex_negative.csv --lexNames val --savePath code/EmotionDynamics/code/my_data/output_reddit_negative

python code/EmotionDynamics/code/avgEmoValues.py --dataPath code/EmotionDynamics/code/my_data/palisades-fire-bluesky_cleaned.csv --lexPath code/EmotionDynamics/lexicons/NRC_EmoLex_positive.csv --lexNames val --savePath code/EmotionDynamics/code/my_data/output_positive_bluesky
python code/EmotionDynamics/code/avgEmoValues.py --dataPath code/EmotionDynamics/code/my_data/palisades-fire-bluesky_cleaned.csv --lexPath code/EmotionDynamics/lexicons/NRC_EmoLex_negative.csv --lexNames val --savePath code/EmotionDynamics/code/my_data/output_negative_bluesky
```

## Step 3: Plot daily emotion-word density

Run:

```bash
python code/EmotionDynamics/code/myScripts/plot_daily_emotion_density.py
```

Output images:
- `code/EmotionDynamics/code/plottingOutput/daily_emotion_density_reddit.png`
- `code/EmotionDynamics/code/plottingOutput/daily_emotion_density_bluesky.png`

## Step 4: Run all eight emotion lexicons and plot

Run this one command to compute all eight EmoLex categories and plot both datasets:

```bash
python code/EmotionDynamics/code/myScripts/run_emotion_lexicons_and_plot.py
```

Output images:
- `code/EmotionDynamics/code/plottingOutput/daily_emotion_density_reddit_8emotions.png`
- `code/EmotionDynamics/code/plottingOutput/daily_emotion_density_bluesky_8emotions.png`

