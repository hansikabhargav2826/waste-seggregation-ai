# ================= CONDITION MODEL TRAINING =================
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

# Path to dataset
train_dir = "dataset_condition/"

# Image settings
img_size = (224, 224)
batch_size = 16

# Data Generator (with validation split)
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Training data
train_gen = datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    subset="training"
)

# Validation data
val_gen = datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)

print("Class labels:", train_gen.class_indices)

# ================= MODEL =================
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(64, activation="relu"),
    layers.Dropout(0.3),

    layers.Dense(2, activation="softmax")  # clean vs contaminated
])

# Compile model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ================= TRAIN =================
model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=5
)

# ================= SAVE =================
model.save("model/condition_model.h5")

print("✅ condition_model.h5 created successfully!")




