# ewaste.py
from bing_image_downloader import downloader

# E-Waste
downloader.download("broken mobile phone e-waste", limit=30, output_dir="dataset/e-waste", force_replace=False)
downloader.download("circuit board electronic waste", limit=30, output_dir="dataset/e-waste", force_replace=False)
downloader.download("dead battery disposal", limit=30, output_dir="dataset/e-waste", force_replace=False)
downloader.download("old laptop e-waste", limit=30, output_dir="dataset/e-waste", force_replace=False)

print("✅ E-waste images downloaded!")
