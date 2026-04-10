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

Run this command to generate positive/negative outputs for every disaster and platform using consistent names:

```bash
python code/EmotionDynamics/code/myScripts/run_all_steps.py
```

Example output folders created:
- `code/EmotionDynamics/code/my_data/output_palisades_reddit_positive`
- `code/EmotionDynamics/code/my_data/output_palisades_reddit_negative`
- `code/EmotionDynamics/code/my_data/output_texasff_bluesky_positive`
- `code/EmotionDynamics/code/my_data/output_texasff_bluesky_negative`

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

Output images (one per dataset/platform combination):
- `code/EmotionDynamics/code/plottingOutput/palisades/daily_emotion_density_palisades_reddit_8emotions.png`
- `code/EmotionDynamics/code/plottingOutput/palisades/daily_emotion_density_palisades_bluesky_8emotions.png`
- `code/EmotionDynamics/code/plottingOutput/texasff/daily_emotion_density_texasff_reddit_8emotions.png`
- `code/EmotionDynamics/code/plottingOutput/texasff/daily_emotion_density_texasff_bluesky_8emotions.png`
- `code/EmotionDynamics/code/plottingOutput/hurricane_milton/daily_emotion_density_hurricane_milton_reddit_8emotions.png`
- `code/EmotionDynamics/code/plottingOutput/hurricane_milton/daily_emotion_density_hurricane_milton_bluesky_8emotions.png`

