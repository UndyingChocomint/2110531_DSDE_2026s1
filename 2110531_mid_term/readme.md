# How to reproduce (RT-DETR-L vehicle detection)

## 1. Environment

| Tool | Version / setting |
|---|---|
| Python | 3.11 |
| PyTorch | 2.6.0 + CUDA 12.4 |
| Ultralytics | 8.4.171 |
| Other packages | pandas, pillow, tqdm, jupyter |
| GPU | NVIDIA RTX 4060 Laptop, 8 GB (training uses `device=0`) |
| Seeds | split `RANDOM_SEED = 42`, training `seed = 0` |

```bash
pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
pip install ultralytics==8.4.171 pandas pillow tqdm jupyter
```

The first training run downloads the COCO-pretrained `rtdetr-l.pt` automatically (internet needed).

## 2. Folder layout (run the notebook from this folder)

```text
yolo_model.ipynb
train.csv
train/train/      # training images
test/test/        # test images (1,013)
```

## 3. What to run

Open `yolo_model.ipynb` and run these cells **in this order**
(cells 3–11 are not needed; they are an older 10% split that cell 12 replaces):

| Order | Cell | What it does | Output |
|---|---|---|---|
| 1 | 12 | Convert `train.csv` to YOLO format, stratified 85/15 split (seed 42) | `dataset/` (2,542 train / 449 val) |
| 2 | 13 | Balance the training set (`DROP_THRESHOLD = 0.90`) | `dataset_balanced/` |
| 3 | 14 | Consistency check of `dataset_balanced/` (also defines variables used by cell 15) | printed report |
| 4 | 15 | Train RT-DETR-L (`imgsz=800`, `epochs=50`, `patience=15`, `batch=4`, `scale=0.5`, `seed=0`) | `runs/detect/rtdetr-l_balanced/weights/best.pt` |
| 5 | 18 | Inference on `test/test/` (`imgsz=800`, IoU 0.45, conf 0.20, Songthaew 0.30) | `submission.csv` |

Upload `submission.csv` to Kaggle 
## 4. Reproduce the result without retraining

Put the submitted `best.pt` at `runs/detect/rtdetr-l_balanced/weights/best.pt` and run only **cell 18**.
 the best.pt is not able to put it in git so I upload to google drive instead : https://drive.google.com/file/d/14W_G4McqjF0Kx39hbVtCVe1-FNcOoM16/view?usp=sharing.
## 5. Optional: validation metrics, per-class table and confusion matrices

```python
from ultralytics import RTDETR
m = RTDETR("runs/detect/rtdetr-l_balanced/weights/best.pt")
m.val(data="dataset_balanced/data.yaml", imgsz=800, plots=True)
```

## Notes

- Training uses `exist_ok=True`, so a new run overwrites `runs/detect/rtdetr-l_balanced/`. Back up the folder first.
- If the GPU runs out of memory, lower `imgsz` to 640 in cell 15 (and in cell 18).
