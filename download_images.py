# download_images.py
from bing_image_downloader import downloader

# Organic Waste
downloader.download("banana peel compost", limit=30, output_dir="dataset/organic", force_replace=False)
downloader.download("apple core waste", limit=30, output_dir="dataset/organic", force_replace=False)
downloader.download("vegetable scraps onion potato", limit=30, output_dir="dataset/organic", force_replace=False)

# Recyclable Waste
downloader.download("plastic bottle recycling clean", limit=30, output_dir="dataset/recyclable", force_replace=False)
downloader.download("cardboard box recycling", limit=30, output_dir="dataset/recyclable", force_replace=False)
downloader.download("glass bottle recycling", limit=30, output_dir="dataset/recyclable", force_replace=False)

# Residual Waste
downloader.download("used tissue garbage", limit=30, output_dir="dataset/residual", force_replace=False)
downloader.download("dirty plastic wrapper chips", limit=30, output_dir="dataset/residual", force_replace=False)
downloader.download("greasy pizza box waste", limit=30, output_dir="dataset/residual", force_replace=False)

print("✅ Organic, Recyclable, Residual images downloaded!")
