import numpy as np
from sklearn.metrics import brier_score_loss

def calculate_brier_score(y_true, y_pred_proba):
    """
    Calculate Brier score for each class and overall
    """
    classes = ['H', 'D', 'A']
    brier_scores = []
    
    for i, class_label in enumerate(classes):
        y_true_binary = (y_true == class_label).astype(int)
        y_pred_class = y_pred_proba[:, i]
        brier_score = brier_score_loss(y_true_binary, y_pred_class)
        brier_scores.append(brier_score)
        print(f"Brier Score for {class_label}: {brier_score:.4f}")
    
    overall_brier = np.mean(brier_scores)*3
    print(f"Overall Brier Score: {overall_brier:.4f}")
    return overall_brier, brier_scores