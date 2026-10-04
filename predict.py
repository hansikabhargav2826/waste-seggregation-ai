# ================= IMPORTS =================
import tensorflow as tf
import numpy as np

# ================= LOAD MODELS =================
model = tf.keras.models.load_model("model/waste_model.h5")
condition_model = tf.keras.models.load_model("model/condition_model.h5")

# ================= LABELS =================
CATEGORY_LABELS = ["E-Waste", "Organic", "Recyclable", "Residual"]

INSTRUCTION_MAP = {
    "E-Waste": (
        "Dispose at an authorized e-waste collection center and never mix with regular household waste. "
        "Includes electronic items like mobile phones, chargers, batteries, computers, and cables."
    ),
    "Organic": (
        "Use for composting to convert waste into natural fertilizer. Includes food scraps, peels, and garden waste."
    ),
    "Recyclable": (
        "Send to recycling facility after cleaning. Includes plastic, glass, paper, and metal."
    ),
    "Residual": (
        "Dispose in general waste bin. Non-recyclable contaminated materials."
    )
}

# ================= MAIN PREDICTION FUNCTION =================
def predict_waste(img_array, filename=None):

    # ================= CATEGORY MODEL =================
    cat_pred = model.predict(img_array, verbose=0)[0]
    category_index = int(np.argmax(cat_pred))
    category = CATEGORY_LABELS[category_index]
    category_confidence = float(np.max(cat_pred))

    # Optional filename override (rule-based correction)
    if filename:
        fname = filename.lower()
        if any(x in fname for x in ["battery", "phone", "circuit"]):
            category = "E-Waste"

    # ================= CONDITION MODEL =================

    # 🚨 SPECIAL RULE FOR E-WASTE
    if category == "E-Waste":
        condition = "⚠️ Unsafe"
        condition_confidence = 1.0

    else:
        cond_pred = condition_model.predict(img_array, verbose=0)

        if cond_pred.shape[-1] == 1:
            prob = float(cond_pred[0][0])
            contaminated_prob = prob
            clean_prob = 1 - prob

            if contaminated_prob >= 0.5:
                condition = "🔴 Contaminated"
                condition_confidence = contaminated_prob
            else:
                condition = "🟢 Clean"
                condition_confidence = clean_prob

        else:
            cond_index = int(np.argmax(cond_pred, axis=1)[0])

            if cond_index == 0:
                condition = "🟢 Clean"
            else:
                condition = "🔴 Contaminated"

            condition_confidence = float(np.max(cond_pred))

    # ================= INSTRUCTION =================
    instruction = INSTRUCTION_MAP.get(category, "Follow proper disposal rules")

    # ================= RETURN =================
    return {
        "category": category,
        "category_confidence": category_confidence,
        "condition": condition,
        "condition_confidence": condition_confidence,
        "instruction": instruction
    }