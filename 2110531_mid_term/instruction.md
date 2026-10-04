# Mid-term Project — Vehicle Detection (Kaggle: `2110531-dsde-2026-1`)

## ⚠️ Access note
`https://www.kaggle.com/competitions/2110531-dsde-2026-1` (and its `/overview`, `/data`, `/evaluation` tabs)
returned **HTTP 404** on every attempt made while writing this file. That almost always means the
competition is restricted to logged-in, enrolled participants (or isn't public yet) — it is not something
I can read without your Kaggle session. **Log in and open the page yourself** to confirm the official rules,
deadline, and scoring metric. Everything below is reverse-engineered from the files already in this folder
(`data.yaml`, `train.csv`, `sample_submission.csv`, `train/`, `test/`) and should be treated as a working
hypothesis, not the official spec.

## Task type (inferred)
Object detection on traffic-camera images, 8 vehicle classes (from `data.yaml`):

```
0 Car  1 Motorcycle  2 Bus  3 Truck  4 Tuktuk  5 Van  6 Pickup  7 Songthaew
```

This lines up with the YOLO setup already started in `yolo_model.ipynb`.

## Data inventory (verified by direct inspection)

| File / folder | Contents |
|---|---|
| `train/train/` | 2,991 images from **15** camera locations: `12,172,180,182,214,222,229,231,232,244,1066,1407,1426,1427,1437` |
| `test/test/` | 1,013 images from **5** camera locations: `227,1068,1072,1192,1439` — **none overlap with the train cameras.** The task is generalizing to unseen camera locations, not just unseen images. |
| `train.csv` | 27,396 ground-truth boxes. Columns: `id, image_id, class_id, x1, y1, x2, y2` (pixel coordinates, no confidence). |
| `sample_submission.csv` | 997 rows. Columns: `id, image_id, class_id, confidence, x1, y1, x2, y2`, all filled with placeholder values (`class_id=0`, `confidence=0.01`, box `[0,0,1,1]`). |
| `data.yaml` | YOLO dataset config (classes + expected `images/train`, `images/val` layout — note this doesn't match the current `train/train`, `test/test` layout, so you'll need to reorganize or symlink). |

Class imbalance in `train.csv` (box count by class):

```
0 Car         17,762
1 Motorcycle   6,563
3 Truck        1,356
6 Pickup         497
2 Bus            482
5 Van            354
4 Tuktuk         265
7 Songthaew      117
```

Cars and motorcycles dominate; Songthaew/Tuktuk/Van/Bus are rare — plan for class-imbalance handling
(class weighting, focal loss, oversampling rare-class images, or augmentation) rather than ignoring it.

### ⚠️ Data discrepancy to confirm with the instructor/TA
`sample_submission.csv` lists only **997** unique `image_id`s, but `test/test/` contains **1,013** image
files — **16 test images have no row in the sample submission**. Before building your submission script
around `sample_submission.csv`'s image list, confirm whether:
- those 16 images are intentionally excluded from scoring, or
- the sample file is simply incomplete and the real test set to predict is all 1,013 images.

If in doubt, generate predictions for all 1,013 test images, but build your final `submission.csv` to match
exactly the `image_id`s Kaggle expects (download the *official* `sample_submission.csv` from the Kaggle
"Data" tab once you can access it, and diff it against this local copy — they may differ).

## Suggested subtasks, in the order you'd actually complete and submit them

1. **EDA (mostly done)** — `data_exploration.py` already covers class distribution and boxes-per-image
   stats. Extend it to: box size/aspect-ratio distribution per class, and a visual check of a few images
   per camera to see lighting/angle differences between train and test cameras.

2. **Convert `train.csv` → YOLO label format**
   - YOLO needs one `.txt` per image with `class_id x_center y_center width height`, all normalized
     [0,1] by image width/height.
   - Reorganize into the layout `data.yaml` expects: `dataset/images/train`, `dataset/images/val`,
     `dataset/labels/train`, `dataset/labels/val`.
   - Since test cameras don't overlap train cameras, **split train/val by camera id** (e.g. hold out
     2-3 of the 15 cameras for validation), not by random image — this gives a validation score that
     actually estimates cross-camera generalization, matching what the real test set measures.

3. **Baseline model training**
   - Continue from `yolo_model.ipynb` (Ultralytics YOLOv8 already installed/verified there).
   - Start with a small pretrained checkpoint (e.g. `yolov8n`/`yolov8s`) fine-tuned on this dataset
     for a quick baseline before scaling up.

4. **Handle class imbalance**
   - Try class-weighted loss, or oversample images containing rare classes (Tuktuk, Songthaew, Van, Bus)
     during training.

5. **Local validation**
   - Evaluate mAP (and per-class AP) on your held-out cameras. Compare qualitatively on a handful of
     images from each of the 5 real test cameras to sanity-check the domain gap.

6. **Inference on `test/test/`**
   - Run the trained model on every test image, collect `(class_id, confidence, x1, y1, x2, y2)` per
     detected box.

7. **Build `submission.csv`**
   - One row per predicted box (not one row per image) with columns `id, image_id, class_id, confidence,
     x1, y1, x2, y2`, exactly matching `sample_submission.csv`'s schema and column order.
   - `id` is just a running row index.
   - Resolve the 997-vs-1013 discrepancy from the step above before finalizing.

8. **Submit to Kaggle & iterate**
   - Upload `submission.csv` on the competition's "Submit Predictions" page, check the leaderboard score,
     then iterate on steps 3-6 (bigger model, more augmentation, better confidence threshold / NMS tuning,
     per-class threshold tuning for rare classes).

## What `sample_submission.csv` is for

`sample_submission.csv` is a **template**, not data to analyze or train on. Its job is to tell you exactly
how Kaggle expects your prediction file to be structured, so the grading script can read it automatically:

- **Which rows/images to cover** — it lists the `image_id`s Kaggle will score you on (here, nominally the
  test-set images, modulo the 997-vs-1013 discrepancy noted above).
- **Exact column names and order** — `id, image_id, class_id, confidence, x1, y1, x2, y2`. If your
  submission is missing a column, has extra columns, or uses different column names, Kaggle's scorer will
  likely reject the file or score it incorrectly.
- **Row granularity** — because it has a `confidence` column and multiple rows can share the same
  `image_id`, each row represents **one predicted bounding box**, not one row per image. An image with
  3 detected vehicles should produce 3 rows.
- **Value types/format** — e.g. `class_id` as an integer matching `data.yaml`'s class indices, `confidence`
  as a float probability, and `x1,y1,x2,y2` as a bounding box in the same coordinate convention as
  `train.csv` (pixel coordinates, top-left/bottom-right corners).
- **A valid, submittable placeholder** — because every row already has *some* value (even if dummy), you
  could technically submit `sample_submission.csv` unmodified right now just to confirm your submission
  pipeline and file format are accepted, before you've trained any model. It will naturally score very
  poorly (confidence 0.01, degenerate 1×1 box), but it's a quick way to validate the submission *process*
  itself.

In short: never submit `sample_submission.csv`'s *values* as your answer — only follow its *shape* when
building your real `submission.csv`.
