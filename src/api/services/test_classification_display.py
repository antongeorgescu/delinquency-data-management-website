#!/usr/bin/env python3
"""
Simple test script to verify classification report accuracy display
"""

import sys
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.datasets import make_classification

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

def test_classification_report():
    """Test classification report display with sample data"""
    print("=" * 60)
    print("CLASSIFICATION REPORT ACCURACY TEST")
    print("=" * 60)
    
    # Create sample binary classification data
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, 
                               n_informative=5, random_state=42)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=42, stratify=y)
    
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics manually
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted') 
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print("\nMANUAL ACCURACY CALCULATIONS:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    
    print("\nSKLEARN CLASSIFICATION REPORT:")
    print(classification_report(y_test, y_pred))
    
    print("\nTEST CONCLUSIONS:")
    print(f"✓ Manual accuracy: {accuracy:.4f}")
    print(f"✓ Classification report should show same accuracy")
    print(f"✓ If you don't see 'accuracy' in the classification report above,")
    print(f"  there might be a display or capture issue")
    
    return accuracy, precision, recall, f1

if __name__ == "__main__":
    test_classification_report()