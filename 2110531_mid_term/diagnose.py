import os, glob, statistics
import pandas as pd

# ─── 1. Original vs augmented ───────────────────────────────────────────────
orig_train = [f for f in glob.glob('./dataset/images/train/*') if '_os2_' not in os.path.basename(f)]
aug_train  = [f for f in glob.glob('./dataset/images/train/*') if '_os2_' in os.path.basename(f)]
print("=== TRAIN SET COMPOSITION ===")
print(f"Original train images  : {len(orig_train)}")
print(f"Augmented train images : {len(aug_train)}")
print(f"Total train images     : {len(orig_train)+len(aug_train)}")
print(f"Val images             : 604")

# ─── 2. CSV stats ────────────────────────────────────────────────────────────
df = pd.read_csv('./train.csv')
print(f"\n=== CSV ANNOTATIONS ===")
print(f"train.csv unique images      : {df['image_id'].nunique()}")
print(f"train.csv total annotations  : {len(df)}")
class_names = ['Car','Motorcycle','Bus','Truck','Tuktuk','Van','Pickup','Songthaew']
for c in sorted(df['class_id'].unique()):
    n = (df['class_id']==c).sum()
    print(f"  class {c} ({class_names[c]:12s}): {n:5d}  ({100*n/len(df):.1f}%)")

# ─── 3. Box size in pixels ────────────────────────────────────────────────────
from PIL import Image
sample = glob.glob('./dataset/images/train/*')
img_w, img_h = 640, 640  # fallback
for p in sample[:5]:
    try:
        with Image.open(p) as im:
            img_w, img_h = im.size
            print(f"\nSample image size: {img_w}x{img_h}  ({os.path.basename(p)})")
            break
    except:
        pass

# box pixel sizes from label files
train_labels = glob.glob('./dataset/labels/train/*.txt')
box_w_px, box_h_px = [], []
for f in train_labels:
    with open(f) as fh:
        for line in fh:
            parts = line.strip().split()
            if len(parts) == 5:
                w_px = float(parts[3]) * img_w
                h_px = float(parts[4]) * img_h
                box_w_px.append(w_px)
                box_h_px.append(h_px)

areas = [w*h for w,h in zip(box_w_px, box_h_px)]
tiny   = sum(1 for a in areas if a < 32*32)
small  = sum(1 for a in areas if 32*32 <= a < 96*96)
medium = sum(1 for a in areas if 96*96 <= a < 192*192)
large  = sum(1 for a in areas if a >= 192*192)
total  = len(areas)

print(f"\n=== BOX SIZE DISTRIBUTION (at {img_w}x{img_h}) ===")
print(f"Tiny  (<32px sq)    : {tiny:6d}  ({100*tiny/total:.1f}%)")
print(f"Small (32-96px sq)  : {small:6d}  ({100*small/total:.1f}%)")
print(f"Medium(96-192px sq) : {medium:6d}  ({100*medium/total:.1f}%)")
print(f"Large (>192px sq)   : {large:6d}  ({100*large/total:.1f}%)")
print(f"Median box WxH px : {statistics.median(box_w_px):.1f} x {statistics.median(box_h_px):.1f}")
print(f"Mean   box WxH px : {statistics.mean(box_w_px):.1f} x {statistics.mean(box_h_px):.1f}")

# ─── 4. CSV box sizes (pixel coords given directly) ──────────────────────────
print(f"\n=== CSV BOX PIXEL SIZES ===")
df['box_w'] = df['x2'] - df['x1']
df['box_h'] = df['y2'] - df['y1']
df['area']  = df['box_w'] * df['box_h']
print(df[['box_w','box_h','area']].describe().round(1))
small_csv = (df['area'] < 32*32).sum()
print(f"Tiny boxes (area<{32*32}): {small_csv} / {len(df)} = {100*small_csv/len(df):.1f}%")

# Per-class box size
print("\nMean box area per class:")
for c in sorted(df['class_id'].unique()):
    sub = df[df['class_id']==c]
    print(f"  {c} {class_names[c]:12s}: mean area={sub['area'].mean():.0f}  median={sub['area'].median():.0f}")
