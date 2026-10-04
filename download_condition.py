from bing_image_downloader import downloader

# ---------------- CLEAN (Total = 50) ----------------
downloader.download(
    "clean plastic bottle recycling",
    limit=12,
    output_dir="dataset_condition/clean",
    force_replace=False
)

downloader.download(
    "clean cardboard box recycling",
    limit=12,
    output_dir="dataset_condition/clean",
    force_replace=False
)

downloader.download(
    "unused tissue paper clean",
    limit=12,
    output_dir="dataset_condition/clean",
    force_replace=False
)

downloader.download(
    "empty clean food container",
    limit=14,
    output_dir="dataset_condition/clean",
    force_replace=False
)


# ---------------- CONTAMINATED (Total = 50) ----------------
downloader.download(
    "greasy pizza box waste",
    limit=12,
    output_dir="dataset_condition/contaminated",
    force_replace=False
)

downloader.download(
    "used tissue garbage dirty",
    limit=12,
    output_dir="dataset_condition/contaminated",
    force_replace=False
)

downloader.download(
    "food waste leftovers dirty container",
    limit=12,
    output_dir="dataset_condition/contaminated",
    force_replace=False
)

downloader.download(
    "dirty plastic waste oily",
    limit=14,
    output_dir="dataset_condition/contaminated",
    force_replace=False
)


print("✅ 50 Clean & 50 Contaminated images downloaded!")