# train_model.py

from ultralytics.utils import SETTINGS

SETTINGS['mlflow'] = False
SETTINGS['wandb'] = True

from ultralytics import YOLO
import wandb
import os
import shutil

# === CONFIGURATION ===
MODEL = 'yolo11n.pt'  # Make sure this is available locally
DATA = 'fish.yaml'
EPOCHS = 50
IMG_SIZE = 416
BATCH = 16
RUN_NAME = 'fish_yolov11'

# === Output filenames in working directory
BEST_PT = 'best.pt'
RESULTS_PNG = 'results.png'
CONF_MATRIX = 'confusion_matrix.png'
NCNN_EXPORT_DIR = 'best_ncnn_model'

# === Step 1: Skip training if best.pt already exists
if os.path.exists(BEST_PT):
    print(f"✅ Found trained model: {BEST_PT}. Skipping training.")
    model = YOLO(BEST_PT)
else:
    # === Step 2: Log in to W&B
    wandb.login(key="0ac0f8409bed2d8ccd7cf5425e777e68bad1e598")
    print("🚀 Starting YOLOv11 training...")
    model = YOLO(MODEL)
    results = model.train(
        data=DATA,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        name="yolov11n_fish",
        project="YOLOv11_Fish"
    )

    # === Step 3: Copy key output files to current directory
    train_dir = os.path.join('runs', 'train', RUN_NAME)
    weights_path = os.path.join(train_dir, 'weights', 'best.pt')
    results_img_path = os.path.join(train_dir, 'results.png')
    conf_matrix_path = os.path.join(train_dir, 'confusion_matrix.png')

    if os.path.exists(weights_path):
        shutil.copy(weights_path, BEST_PT)
        print(f"✅ Copied best.pt to working directory.")
    else:
        print(f"❌ best.pt not found at {weights_path}")
        exit(1)

    if os.path.exists(results_img_path):
        shutil.copy(results_img_path, RESULTS_PNG)
        print("✅ Copied results.png to working directory.")
    else:
        print("⚠️ results.png not found.")

    if os.path.exists(conf_matrix_path):
        shutil.copy(conf_matrix_path, CONF_MATRIX)
        print("✅ Copied confusion_matrix.png to working directory.")
    else:
        print("⚠️ confusion_matrix.png not found.")

# === Step 4: Export to NCNN format if not already exported
if not os.path.exists(NCNN_EXPORT_DIR):
    print("📦 Exporting best.pt to NCNN format...")
    model = YOLO(BEST_PT)
    model.export(format='ncnn')
    print(f"✅ Exported NCNN model to: {NCNN_EXPORT_DIR}")
else:
    print(f"✅ NCNN model already exists: {NCNN_EXPORT_DIR}")
