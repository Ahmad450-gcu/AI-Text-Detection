MAX_LENGTH = 256

ID2LABEL = {
    0: "Human",
    1: "AI",
}

LABEL2ID = {label: idx for idx, label in ID2LABEL.items()}

DEFAULT_DECISION_THRESHOLD = 0.5
