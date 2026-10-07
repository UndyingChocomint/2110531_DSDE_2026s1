"""
RT-DETR training script with all fixes applied:

Fix 1: Augmentation (mosaic=0.5, close_mosaic=0, scale=0.5)
Fix 2: Dataset cleaned - only annotated images used
Fix 3: Higher resolution (imgsz=640 → 768)
Fix 4: Class imbalance addressed via cls_pw
Fix 5: Explicit AdamW optimizer with correct LR
Fix 6: More epochs + higher patience
"""

from ultralytics import RTDETR
import yaml, os

# ─── Config ────────────────────────────────────────────────────────────────
MODEL_NAME = "rtdetr-l.pt"
DATA_YAML  = "dataset/data.yaml"

# RT-DETR at 768px uses ~6-7 GB VRAM with AMP; RTX 4060 8GB should fit batch=2.
# If you get OOM, reduce to imgsz=640 and raise batch to 4.
IMGSZ = 768
BATCH = 2

# ─── Step 3 fix: resolution ─────────────────────────────────────────────────
# Original used imgsz=640. The source images are 352×288.
# At 640px, median car box = ~24×45px — tiny for DETR.
# At 768px, same car = ~29×54px, giving the feature pyramid more signal.
# Trade-off: slower per-epoch, smaller batch.

# ─── Step 4 fix: class imbalance via cls_pw ─────────────────────────────────
# cls_pw is a per-class weight vector passed directly to the BCE loss.
# Ultralytics RT-DETR does NOT support cls_pw the same way YOLO does.
# The correct approach for RT-DETR is to oversample rare-class images
# at the dataset level (done below) or use fl_gamma (focal loss gamma).
#
# RT-DETR uses focal loss internally. Raising fl_gamma (default 0.0 in
# Ultralytics RT-DETR) to 2.0 focuses training on hard/rare examples.
# This is the correct substitute for cls_pw on a transformer detector.

# Distribution from diagnose.py (train split):
#   Car: 64.8%, Motorcycle: 24.0%, Bus: 1.8%, Truck: 4.9%,
#   Tuktuk: 1.0%, Van: 1.3%, Pickup: 1.8%, Songthaew: 0.4%
#
# Oversampling: duplicate images that contain only rare classes.
# The function below copies those images/labels before training.

CLASS_NAMES = ["Car", "Motorcycle", "Bus", "Truck", "Tuktuk", "Van", "Pickup", "Songthaew"]
RARE_CLASSES = {2, 4, 5, 6, 7}   # Bus, Tuktuk, Van, Pickup, Songthaew
OVERSAMPLE_FACTOR = 3             # repeat rare-class images this many extra times


def oversample_rare_classes(img_dir, lbl_dir, factor=3):
    """
    Duplicate images whose labels contain ONLY rare-class boxes.
    Creates copies named <original>_dup1.jpg / _dup1.txt, etc.
    Idempotent: skips if duplicates already exist.
    """
    import glob, shutil
    from pathlib import Path

    img_dir = Path(img_dir)
    lbl_dir = Path(lbl_dir)
    added = 0

    for lbl_path in lbl_dir.glob("*.txt"):
        if "_dup" in lbl_path.stem:
            continue   # already a duplicate

        lines = lbl_path.read_text(encoding="utf-8").strip().splitlines()
        if not lines:
            continue   # background image, skip

        classes_in_image = {int(l.split()[0]) for l in lines if l.strip()}
        if not classes_in_image.issubset(RARE_CLASSES):
            continue   # image contains common classes too — don't oversample

        # Find matching image
        img_candidates = list(img_dir.glob(lbl_path.stem + ".*"))
        img_candidates = [p for p in img_candidates if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
        if not img_candidates:
            continue
        img_path = img_candidates[0]

        for i in range(1, factor + 1):
            new_stem = f"{lbl_path.stem}_dup{i}"
            new_img  = img_dir / (new_stem + img_path.suffix)
            new_lbl  = lbl_dir / (new_stem + ".txt")
            if not new_img.exists():
                shutil.copy2(img_path, new_img)
                shutil.copy2(lbl_path, new_lbl)
                added += 1

    print(f"[oversample] Added {added} duplicate images for rare classes.")


# ─── Run oversampling before training ───────────────────────────────────────
oversample_rare_classes(
    img_dir="dataset/images/train",
    lbl_dir="dataset/labels/train",
    factor=OVERSAMPLE_FACTOR,
)

# ─── Model ──────────────────────────────────────────────────────────────────
model = RTDETR(MODEL_NAME)

# ─── Train ──────────────────────────────────────────────────────────────────
results = model.train(
    data=DATA_YAML,

    # Fix 5: epochs + patience
    epochs=100,          # was 30 — transformers need more updates
    patience=25,         # was 10 — RT-DETR plateaus mid-training then climbs

    # Fix 3: resolution
    imgsz=IMGSZ,         # was 640
    batch=BATCH,         # was 4 — reduced to fit 8 GB VRAM at 768px

    device=0,
    workers=2,
    pretrained=True,
    plots=True,
    amp=True,
    seed=0,
    cache="disk",

    # Fix 5: optimizer
    # RT-DETR benefits from AdamW over the auto-selected SGD.
    optimizer="AdamW",
    lr0=1e-4,            # lower LR suits fine-tuning a transformer
    lrf=0.1,             # final LR = lr0 * lrf = 1e-5
    weight_decay=1e-4,
    warmup_epochs=3,

    # accumulate to a nominal batch of 16 for more frequent gradient steps
    # (nbs=16 means: step optimizer every 16/batch = 8 mini-batches)
    nbs=16,

    # Fix 1: augmentation tuned for small-object fixed-camera traffic
    mosaic=0.5,          # was 1.0 — halved to avoid shrinking tiny cars further
    close_mosaic=0,      # disable mosaic for the entire run (0 = never close)
    scale=0.5,           # was 0.3 — allow objects to scale up as well as down
    fliplr=0.5,
    flipud=0.0,
    degrees=3.0,         # was 0.0 — small rotation helps cross-camera generalization
    translate=0.1,       # adds a little spatial jitter
    perspective=0.0003,  # mimics slight camera angle differences
    mixup=0.0,
    hsv_h=0.015,
    hsv_s=0.5,
    hsv_v=0.5,

    # Fix 4: class imbalance weight
    # fl_gamma is NOT in this Ultralytics version (8.4.171).
    # cls_pw upweights the classification loss — positive class weight.
    # Values > 1.0 penalise false negatives more, helping rare classes.
    # Default is 0.0 (no reweighting). 2.0 is a mild but effective bump.
    cls_pw=1.0,          # max allowed (0.0–1.0); 1.0 = full positive-class upweight

    project="runs/detect",
    name="rtdetr-l_fix",
    exist_ok=True,
)

print("\n=== Training complete ===")
print(f"Best weights: runs/detect/rtdetr-l_fix/weights/best.pt")
print(f"Best mAP50  : {results.results_dict.get('metrics/mAP50(B)', 'N/A'):.4f}")
