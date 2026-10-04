def get_disposal_instruction(category: str, condition: str) -> str:
    instructions = {
        "Organic": {
            "Clean": "🌱 Compost in green bin",
            "Contaminated": "⚠️ Dispose in residual waste"
        },
        "Recyclable": {
            "Clean": "♻️ Place in blue recycling bin",
            "Contaminated": "🧹 Rinse or dispose in residual waste"
        },
        "E-waste": {
            "Clean": "🔌 Take to e-waste collection center",
            "Contaminated": "☢️ Handle carefully, take to hazardous facility"
        },
        "Residual": {
            "Clean": "🗑️ Place in general waste bin",
            "Contaminated": "🚮 Double-bag and dispose safely"
        }
    }
    return instructions.get(category, {}).get(condition, "Check local guidelines.")

def calculate_eco_points(category: str, condition: str, confidence: float) -> int:
    base_points = {"Organic":10,"Recyclable":15,"E-waste":20,"Residual":5}.get(category,5)
    condition_multiplier = 1.2 if condition=="Clean" else 1.0
    confidence_multiplier = 0.5 + (confidence * 0.5)
    return int(base_points * condition_multiplier * confidence_multiplier)

def get_eco_level(score: int):
    levels = [
        (0,"Beginner","🌱",50),
        (50,"Eco Aware","🌿",150),
        (150,"Green Guardian","🌳",300),
        (300,"Earth Protector","🌍",500),
        (500,"Eco Champion","🏆",1000),
        (1000,"Planet Hero","⭐",float('inf'))
    ]
    for i,(threshold,name,badge,next_threshold) in enumerate(levels):
        if i==len(levels)-1 or score < levels[i+1][0]:
            return name,badge,next_threshold
    return levels[-1][1],levels[-1][2],levels[-1][3]

def format_confidence(confidence: float) -> str:
    return f"{confidence*100:.1f}%"

def get_confidence_color(confidence: float) -> str:
    if confidence >= 0.8:
        return "#4CAF50"
    elif confidence >= 0.6:
        return "#FFC107"
    else:
        return "#F44336"
    











    
