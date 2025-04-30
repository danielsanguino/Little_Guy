import os
import shutil
import zipfile
import yaml

ZIP_FILE = 'Deep-Fish.zip'
EXTRACTED_DIR = 'deep-fish-object-detection'
TARGET_DIR = 'datasets'
YAML_FILE = 'fish.yaml'

def safe_mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def unzip_dataset(zip_path, extract_to):
    if not os.path.exists(extract_to):
        print(f"📦 Unzipping {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("✅ Unzip complete.")
    else:
        print("✅ Dataset already unzipped.")

def create_yolo_dirs(base_dir):
    for split in ['train', 'valid', 'test']:
        for sub in ['images', 'labels']:
            safe_mkdir(os.path.join(base_dir, split, sub))

def collect_files(source_dir):
    train_imgs, train_labels = [], []
    valid_imgs, valid_labels = [], []

    for root, _, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            if 'train' in root and f.endswith('.jpg'):
                train_imgs.append(full_path)
            elif 'train' in root and f.endswith('.txt'):
                train_labels.append(full_path)
            elif 'valid' in root and f.endswith('.jpg'):
                valid_imgs.append(full_path)
            elif 'valid' in root and f.endswith('.txt'):
                valid_labels.append(full_path)

    return sorted(train_imgs), sorted(train_labels), sorted(valid_imgs), sorted(valid_labels)

def copy_dataset(images, labels, split, test_limit=None):
    for i, img_path in enumerate(images):
        dest_split = 'test' if test_limit and i < test_limit else split
        dst_img = os.path.join(TARGET_DIR, dest_split, 'images', os.path.basename(img_path))
        shutil.copy(img_path, dst_img)

    for i, lbl_path in enumerate(labels):
        dest_split = 'test' if test_limit and i < test_limit else split
        dst_lbl = os.path.join(TARGET_DIR, dest_split, 'labels', os.path.basename(lbl_path))
        shutil.copy(lbl_path, dst_lbl)

def create_yaml(path, nc, class_names):
    yaml_dict = {
        'path': TARGET_DIR,
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'nc': nc,
        'names': class_names
    }
    with open(path, 'w') as f:
        yaml.dump(yaml_dict, f)

if __name__ == '__main__':
    print("🚀 Preparing YOLOv11-compatible dataset...")

    unzip_dataset(ZIP_FILE, EXTRACTED_DIR)
    create_yolo_dirs(TARGET_DIR)

    train_imgs, train_labels, valid_imgs, valid_labels = collect_files(EXTRACTED_DIR)

    print("📁 Copying training data...")
    copy_dataset(train_imgs, train_labels, split='train')

    print("📁 Copying validation/test data...")
    copy_dataset(valid_imgs, valid_labels, split='valid', test_limit=100)

    if not os.path.exists(YAML_FILE):
        create_yaml(YAML_FILE, nc=1, class_names=['fish'])
        print(f"📄 Created dataset YAML: {YAML_FILE}")

    print("✅ All done! YOLOv11 dataset is ready at:", TARGET_DIR)
