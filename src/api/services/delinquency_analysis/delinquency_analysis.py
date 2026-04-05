import pandas as pd
import numpy as np
import sys
import os
import argparse
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from database import DatabaseManager

def load_comprehensive_dataset(db_path=None):
    """
    Load and merge all tables for comprehensive delinquency analysis using centralized database methods.
    
    Args:
        db_path: Optional path to the database file. If None, uses default location.
        
    Returns a DataFrame with all relevant features and target variable.
    """
    db_manager = DatabaseManager(db_path) if db_path else DatabaseManager()
    
    # Get comprehensive data using centralized method
    data = db_manager.get_delinquency_analysis_data()
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    if df.empty:
        print("Error: No data found in database")
        return pd.DataFrame()
    
    print(f"Loaded {len(df):,} records for analysis")
    print(f"Dataset shape: {df.shape}")
    print(f"Features available: {df.columns.tolist()}")
    
    return df

def engineer_features(df):
    """
    Engineer additional features for better delinquency prediction.
    """
    # Date-based features
    df['origination_date'] = pd.to_datetime(df['origination_date'])
    df['disbursement_date'] = pd.to_datetime(df['disbursement_date'])
    df['maturity_date'] = pd.to_datetime(df['maturity_date'])
    
    current_date = pd.Timestamp.now()
    
    # Time-based features
    df['loan_age_days'] = (current_date - df['origination_date']).dt.days
    df['days_since_disbursement'] = (current_date - df['disbursement_date']).dt.days
    df['days_to_maturity'] = (df['maturity_date'] - current_date).dt.days
    df['loan_progress_pct'] = df['loan_age_days'] / (df['loan_term_years'] * 365)
    
    # Financial ratios
    df['debt_to_income_ratio'] = df['loan_amount'] / np.maximum(df['annual_income_cad'], 1)
    df['payment_to_income_ratio'] = (df['monthly_payment'] * 12) / np.maximum(df['annual_income_cad'], 1)
    df['education_roi'] = df['average_starting_salary'] / np.maximum(df['typical_tuition_cad'], 1)
    df['loan_to_education_value_ratio'] = df['loan_amount'] / df['education_value']
    
    # Payment behavior features
    df['delinquency_rate'] = df['missed_payments'] / np.maximum(df['total_payments_made'], 1)
    df['payment_consistency'] = df['on_time_payments'] / np.maximum(df['total_payments_made'], 1)
    # Note: total_late_fees not available, using missed_payments as proxy for late fees
    df['avg_late_fee_per_payment'] = df['missed_payments'] / np.maximum(df['total_payments_made'], 1)
    
    # Risk category features
    df['high_ltv_risk'] = (df['ltv_ratio'] > 80).astype(int)
    df['low_income_risk'] = (df['annual_income_cad'] < 40000).astype(int)
    df['young_borrower_risk'] = (df['age'] < 26).astype(int)
    df['long_term_loan_risk'] = (df['loan_term_years'] > 15).astype(int)
    df['high_difficulty_program'] = (df['program_difficulty'] == 3).astype(int)
    
    # Employment market features
    df['low_employment_rate'] = (df['employment_rate'] < 80).astype(int)
    df['poor_job_outlook'] = (df['job_market_outlook'] == 'Challenging').astype(int)
    
    print(f"Feature engineering complete. Dataset now has {len(df.columns)} features")
    
    return df

def prepare_ml_features(df):
    """
    Prepare features for machine learning by encoding categorical variables.
    """
    # Create a copy for ML processing
    ml_df = df.copy()
    
    # Categorical features to encode
    categorical_features = [
        'employment_status', 'marital_status', 'province', 'loan_type', 
        'institution_province', 'lender', 'program_type', 'field_of_study',
        'accreditation_body', 'institution_type', 'university_name', 
        'requires_licensing', 'job_market_outlook', 'loan_status'
    ]
    
    # Label encoding for categorical features
    label_encoders = {}
    for feature in categorical_features:
        if feature in ml_df.columns:
            le = LabelEncoder()
            ml_df[feature + '_encoded'] = le.fit_transform(ml_df[feature].fillna('Unknown'))
            label_encoders[feature] = le
    
    # Select numerical and encoded features for ML
    feature_columns = [col for col in ml_df.columns if 
                      (ml_df[col].dtype in ['int64', 'float64'] and 
                       col not in ['payer_id', 'is_delinquent']) or 
                      col.endswith('_encoded')]
    
    # Handle missing values
    ml_df[feature_columns] = ml_df[feature_columns].fillna(ml_df[feature_columns].mean())
    
    # Remove infinite values
    ml_df[feature_columns] = ml_df[feature_columns].replace([np.inf, -np.inf], np.nan)
    ml_df[feature_columns] = ml_df[feature_columns].fillna(ml_df[feature_columns].mean())
    
    X = ml_df[feature_columns]
    y = ml_df['is_delinquent']
    
    print(f"ML dataset prepared with {X.shape[1]} features for {X.shape[0]} samples")
    print(f"Feature list: {X.columns.tolist()}")
    
    return X, y, feature_columns, label_encoders

def train_delinquency_models(X, y):
    """
    Train multiple ML models and select the best performer.
    """
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=6, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVC': SVC(kernel='rbf', probability=True, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5)
    }
    
    # Train and evaluate models
    model_results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        auc_score = roc_auc_score(y_test, y_pred_proba)
        cv_scores = cross_val_score(model, X_train_scaled if name == 'Logistic Regression' else X_train, 
                                   y_train, cv=5, scoring='roc_auc')
        
        model_results[name] = {
            'model': model,
            'auc_score': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'predictions': y_pred_proba
        }
        
        print(f"AUC Score: {auc_score:.4f}")
        print(f"Cross-validation AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
    
    # Select best model
    best_model_name = max(model_results.keys(), key=lambda x: model_results[x]['auc_score'])
    best_model = model_results[best_model_name]['model']
    
    print(f"\nBest performing model: {best_model_name}")
    
    return best_model, model_results, scaler
def train_single_algorithm(X, y, algorithm):
    """
    Train only the specified ML algorithm instead of all models.
    
    Args:
        X: Feature matrix
        y: Target labels
        algorithm: The specific algorithm to train
    
    Returns:
        Tuple of (model, model_results, scaler, model_name)
    """
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Algorithm mapping
    algorithm_map = {
        'random_forest': ('Random Forest', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)),
        'gradient_boosting': ('Gradient Boosting', GradientBoostingClassifier(n_estimators=100, max_depth=6, random_state=42)),
        'logistic_regression': ('Logistic Regression', LogisticRegression(random_state=42, max_iter=1000)),
        'neural_network': ('Neural Network', MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42, max_iter=500)),
        'svm': ('SVM', SVC(kernel='rbf', probability=True, random_state=42)),
        'knn': ('KNN', KNeighborsClassifier(n_neighbors=5))
    }
    
    if algorithm not in algorithm_map:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    model_name, model = algorithm_map[algorithm]
    
    print(f"\nTraining {model_name}...")
    
    # Train the specific model
    if algorithm == 'logistic_regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    auc_score = roc_auc_score(y_test, y_pred_proba) if len(set(y_test)) > 1 else 0.0
    cv_scores = cross_val_score(model, X_train_scaled if algorithm == 'logistic_regression' else X_train, y_train, cv=5, scoring='roc_auc')
    
    print(f"AUC Score: {auc_score:.4f}")
    print(f"Cross-validation AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Store results in same format as train_delinquency_models
    model_results = {
        model_name: {
            'auc_score': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    }
    
    return model, model_results, scaler, model_name
def analyze_feature_importance(model, feature_columns, model_name):
    """
    Analyze and display feature importance from the trained model.
    """
    print(f"\n{'='*60}")
    print(f"FEATURE IMPORTANCE ANALYSIS - {model_name}")
    print(f"{'='*60}")
    
    if hasattr(model, 'feature_importances_'):
        # Tree-based models
        importance_scores = model.feature_importances_
    elif hasattr(model, 'coef_'):
        # Linear models
        importance_scores = np.abs(model.coef_[0])
    else:
        print("Model does not support feature importance analysis")
        return None
    
    # Create feature importance DataFrame
    feature_importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': importance_scores
    }).sort_values('importance', ascending=False)
    
    print("\nTop 20 Most Influential Features for Delinquency Prediction:")
    print("-" * 70)
    
    for i, (idx, row) in enumerate(feature_importance_df.head(20).iterrows()):
        print(f"{i+1:2d}. {row['feature']:<40} {row['importance']:.4f}")
    
    # Categorize features by table source
    user_features = [f for f in feature_importance_df['feature'] if any(
        prefix in f.lower() for prefix in ['age', 'income', 'employment', 'marital', 'province'])]
    loan_features = [f for f in feature_importance_df['feature'] if any(
        prefix in f.lower() for prefix in ['loan_', 'interest', 'ltv', 'balance', 'payment', 'debt_to'])]
    program_features = [f for f in feature_importance_df['feature'] if any(
        prefix in f.lower() for prefix in ['program_', 'difficulty', 'tuition', 'employment_rate', 'education'])]
    payment_features = [f for f in feature_importance_df['feature'] if any(
        prefix in f.lower() for prefix in ['missed', 'late', 'delinquency_rate', 'consistency'])]
    
    print(f"\nFeature Importance by Data Source:")
    print(f"User Profile Features: {sum(feature_importance_df[feature_importance_df['feature'].isin(user_features)]['importance']):.3f}")
    print(f"Loan Info Features: {sum(feature_importance_df[feature_importance_df['feature'].isin(loan_features)]['importance']):.3f}")
    print(f"Program Features: {sum(feature_importance_df[feature_importance_df['feature'].isin(program_features)]['importance']):.3f}")
    print(f"Payment Behavior Features: {sum(feature_importance_df[feature_importance_df['feature'].isin(payment_features)]['importance']):.3f}")
    
    return feature_importance_df

def calculate_risk_scores(model, X, scaler=None, model_name='', algorithm='random_forest'):
    """
    Calculate delinquency risk scores using ML classification algorithms: 0 (low), 1 (medium), 2 (high).
    
    Args:
        model: Trained ML model
        X: Feature matrix
        scaler: Feature scaler (for algorithms requiring scaling)
        model_name: Name of the model
        algorithm: Risk scoring algorithm ('random_forest', 'gradient_boosting', 'logistic_regression', 'svm', 'knn', 'neural_network')
    
    Returns:
        Array of risk scores (0, 1, or 2)
    """
    if model_name == 'Logistic Regression' and scaler is not None:
        X_scaled = scaler.transform(X)
        risk_probabilities = model.predict_proba(X_scaled)[:, 1]
    else:
        risk_probabilities = model.predict_proba(X)[:, 1]
    
    print(f"\nUsing '{algorithm}' classification algorithm for risk scoring...")
    
    # Create training labels from probability distribution for classification algorithms
    prob_percentiles = np.percentile(risk_probabilities, [40, 80])  # 40-40-20 split
    training_labels = np.zeros(len(risk_probabilities))
    training_labels[risk_probabilities > prob_percentiles[0]] = 1
    training_labels[risk_probabilities > prob_percentiles[1]] = 2
    
    # Prepare data for classification
    X_for_classification = X if scaler is None else scaler.transform(X)
    
    if algorithm == 'random_forest':
        # Random Forest classification approach
        print("Training Random Forest classifier for risk level prediction...")
        from sklearn.ensemble import RandomForestClassifier
        
        rf_model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=10, 
            random_state=42,
            class_weight='balanced',
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        # Train-test split with stratification
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42, 
                stratify=training_labels
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42
            )
        
        rf_model.fit(X_train, y_train)
        risk_scores = rf_model.predict(X_for_classification)
        
        print(f"Random Forest Training Accuracy: {rf_model.score(X_train, y_train):.3f}")
        print(f"Random Forest Test Accuracy: {rf_model.score(X_test, y_test):.3f}")
        
    elif algorithm == 'gradient_boosting':
        # Gradient Boosting classification approach
        print("Training Gradient Boosting classifier for risk level prediction...")
        from sklearn.ensemble import GradientBoostingClassifier
        
        gb_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42, 
                stratify=training_labels
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42
            )
        
        gb_model.fit(X_train, y_train)
        risk_scores = gb_model.predict(X_for_classification)
        
        print(f"Gradient Boosting Training Accuracy: {gb_model.score(X_train, y_train):.3f}")
        print(f"Gradient Boosting Test Accuracy: {gb_model.score(X_test, y_test):.3f}")
        
    elif algorithm == 'logistic_regression':
        # Logistic Regression classification approach
        print("Training Logistic Regression classifier for risk level prediction...")
        from sklearn.linear_model import LogisticRegression
        
        lr_model = LogisticRegression(
            random_state=42,
            class_weight='balanced',
            max_iter=1000,
            C=1.0
        )
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42, 
                stratify=training_labels
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42
            )
        
        lr_model.fit(X_train, y_train)
        risk_scores = lr_model.predict(X_for_classification)
        
        print(f"Logistic Regression Training Accuracy: {lr_model.score(X_train, y_train):.3f}")
        print(f"Logistic Regression Test Accuracy: {lr_model.score(X_test, y_test):.3f}")
        
    elif algorithm == 'neural_network':
        # Multi-layer Perceptron classification approach
        print("Training Neural Network classifier for risk level prediction...")
        from sklearn.neural_network import MLPClassifier
        
        nn_model = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            alpha=0.001,
            learning_rate='adaptive',
            max_iter=500,
            random_state=42
        )
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42, 
                stratify=training_labels
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42
            )
        
        nn_model.fit(X_train, y_train)
        risk_scores = nn_model.predict(X_for_classification)
        
        print(f"Neural Network Training Accuracy: {nn_model.score(X_train, y_train):.3f}")
        print(f"Neural Network Test Accuracy: {nn_model.score(X_test, y_test):.3f}")
        
    elif algorithm == 'kmeans':
        # K-means clustering approach (unsupervised learning fallback)
        print("Using K-means clustering for risk level prediction...")
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_for_classification)
        
        # Map clusters to risk levels based on average probability in each cluster
        cluster_probs = []
        for i in range(3):
            cluster_mask = clusters == i
            if np.sum(cluster_mask) > 0:
                avg_prob = np.mean(risk_probabilities[cluster_mask])
                cluster_probs.append((i, avg_prob))
        
        # Sort clusters by average probability
        cluster_probs.sort(key=lambda x: x[1])
        
        risk_scores = np.zeros(len(risk_probabilities))
        for rank, (cluster_idx, _) in enumerate(cluster_probs):
            risk_scores[clusters == cluster_idx] = rank
            
        print(f"K-means cluster mapping: {[(f'Cluster {cp[0]}', f'Risk {rank}', f'Avg Prob {cp[1]:.3f}') for rank, cp in enumerate(cluster_probs)]}")
    
    elif algorithm == 'svm':
        # Enhanced SVM-based risk classification
        print("Training Support Vector Machine classifier for risk level prediction...")
        
        # Verify we have all three classes in training data
        unique_labels, label_counts = np.unique(training_labels, return_counts=True)
        print(f"Training label distribution: {dict(zip(unique_labels.astype(int), label_counts))}")
        
        # Enhanced SVM with optimized hyperparameters
        svm_model = SVC(
            kernel='rbf', 
            probability=True, 
            random_state=42,
            class_weight='balanced',
            C=10.0,  # Higher regularization for better generalization
            gamma='auto',
            decision_function_shape='ovr'
        )
        
        # Ensure sufficient samples for each class
        min_samples_per_class = 5
        for label in [0, 1, 2]:
            count = np.sum(training_labels == label)
            if count < min_samples_per_class:
                print(f"Warning: Only {count} samples for class {label}. Adjusting distribution...")
                prob_percentiles = np.percentile(risk_probabilities, [50, 85])
                training_labels = np.zeros(len(risk_probabilities))
                training_labels[risk_probabilities > prob_percentiles[0]] = 1
                training_labels[risk_probabilities > prob_percentiles[1]] = 2
                break
        
        try:
            X_train_svm, X_test_svm, y_train_svm, y_test_svm = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42, 
                stratify=training_labels
            )
        except ValueError:
            X_train_svm, X_test_svm, y_train_svm, y_test_svm = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42
            )
        
        svm_model.fit(X_train_svm, y_train_svm)
        risk_scores = svm_model.predict(X_for_classification)
        
        print(f"SVM Training Accuracy: {svm_model.score(X_train_svm, y_train_svm):.3f}")
        print(f"SVM Test Accuracy: {svm_model.score(X_test_svm, y_test_svm):.3f}")
        
        # Enhanced post-processing for balanced distribution
        unique_output, output_counts = np.unique(risk_scores, return_counts=True)
        print(f"SVM Output distribution: {dict(zip(unique_output.astype(int), output_counts))}")
        
        if len(unique_output) < 3:
            print("SVM produced incomplete risk distribution. Applying intelligent post-processing...")
            # Get prediction probabilities for more nuanced classification
            svm_probs = svm_model.predict_proba(X_for_classification)
            
            # Use probability-based adjustment for missing classes
            prob_based_scores = np.argmax(svm_probs, axis=1)
            
            # Blend original predictions with probability-based ones
            final_scores = np.copy(risk_scores)
            
            # Fill missing medium risk category if needed
            if 1 not in risk_scores and len(np.where(prob_based_scores == 1)[0]) > 0:
                final_scores[prob_based_scores == 1] = 1
            
            risk_scores = final_scores
    
    elif algorithm == 'knn':
        # Enhanced KNN-based risk classification
        print("Training K-Nearest Neighbors classifier for risk level prediction...")
        
        # Verify we have all three classes
        unique_labels, label_counts = np.unique(training_labels, return_counts=True)
        print(f"Training label distribution: {dict(zip(unique_labels.astype(int), label_counts))}")
        
        # Optimize k value based on dataset size
        dataset_size = len(risk_probabilities)
        if dataset_size < 100:
            optimal_k = 3
        elif dataset_size < 500:
            optimal_k = 5
        elif dataset_size < 1000:
            optimal_k = 7
        else:
            optimal_k = min(15, max(5, int(np.sqrt(dataset_size) * 0.5)))
        
        # Enhanced KNN with better parameters
        knn_model = KNeighborsClassifier(
            n_neighbors=optimal_k, 
            weights='distance',
            algorithm='auto',
            metric='euclidean',
            p=2
        )
        
        try:
            X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42, 
                stratify=training_labels
            )
        except ValueError:
            X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
                X_for_classification, training_labels, test_size=0.3, random_state=42
            )
        
        knn_model.fit(X_train_knn, y_train_knn)
        risk_scores = knn_model.predict(X_for_classification)
        
        print(f"KNN Training Accuracy (k={optimal_k}): {knn_model.score(X_train_knn, y_train_knn):.3f}")
        print(f"KNN Test Accuracy: {knn_model.score(X_test_knn, y_test_knn):.3f}")
        
        # Enhanced distribution checking and correction
        unique_output, output_counts = np.unique(risk_scores, return_counts=True)
        print(f"KNN Output distribution: {dict(zip(unique_output.astype(int), output_counts))}")
        
        if len(unique_output) < 3:
            print("KNN produced incomplete risk distribution. Applying probability-based correction...")
            # Get prediction probabilities for more intelligent adjustment
            knn_probs = knn_model.predict_proba(X_for_classification)
            
            # Find samples with high uncertainty (close probabilities)
            max_probs = np.max(knn_probs, axis=1)
            uncertain_mask = max_probs < 0.6  # Low confidence predictions
            
            if np.sum(uncertain_mask) > 0:
                # Reassign uncertain predictions based on probability distribution
                uncertain_indices = np.where(uncertain_mask)[0]
                for idx in uncertain_indices:
                    target_prob = risk_probabilities[idx]
                    if 0.6 <= target_prob <= 0.9:  # Medium risk probability range
                        risk_scores[idx] = 1
            
    elif algorithm == 'percentile':
        # Percentile-based risk classification
        print("Using Percentile-based risk classification...")
        # Bottom 60% = Low (0), Next 30% = Medium (1), Top 10% = High (2)
        percentile_60 = np.percentile(risk_probabilities, 60)
        percentile_90 = np.percentile(risk_probabilities, 90)
        
        risk_scores = np.zeros(len(risk_probabilities))
        risk_scores[risk_probabilities > percentile_60] = 1  # Medium risk
        risk_scores[risk_probabilities > percentile_90] = 2  # High risk
        
        print(f"Percentile thresholds: P60={percentile_60:.4f}, P90={percentile_90:.4f}")
            
    elif algorithm == 'threshold':
        # Fixed probability threshold-based risk classification  
        print("Using Fixed Threshold-based risk classification...")
        # Updated thresholds: <0.6=Low, 0.6-0.9=Medium, >0.9=High
        
        risk_scores = np.zeros(len(risk_probabilities))
        risk_scores[risk_probabilities >= 0.6] = 1  # Medium risk
        risk_scores[risk_probabilities > 0.9] = 2   # High risk
        
        print(f"Fixed thresholds: Low<0.6, Medium=0.6-0.9, High>0.9")
            
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}. Choose from 'random_forest', 'gradient_boosting', 'logistic_regression', 'neural_network', 'svm', 'knn', 'kmeans', 'percentile', 'threshold'")
    
    # Convert to integers
    risk_scores = risk_scores.astype(int)
    
    # Distribution summary
    low_risk = np.sum(risk_scores == 0)
    medium_risk = np.sum(risk_scores == 1)
    high_risk = np.sum(risk_scores == 2)
    
    print(f"\nRisk Score Distribution Summary:")
    print(f"  Algorithm: {algorithm}")
    print(f"  Low Risk (0): {low_risk:,} borrowers ({low_risk/len(risk_scores)*100:.1f}%)")
    print(f"  Medium Risk (1): {medium_risk:,} borrowers ({medium_risk/len(risk_scores)*100:.1f}%)")
    print(f"  High Risk (2): {high_risk:,} borrowers ({high_risk/len(risk_scores)*100:.1f}%)")
    
    if algorithm == 'threshold':
        print(f"\nProbability Thresholds Used:")
        print(f"  Low -> Medium: 0.6")
        print(f"  Medium -> High: 0.9")
    elif algorithm == 'percentile':
        print(f"\nPercentile Thresholds Used:")
        print(f"  Low -> Medium: {np.percentile(risk_probabilities, 60):.4f}")
        print(f"  Medium -> High: {np.percentile(risk_probabilities, 90):.4f}")
    elif algorithm in ['svm', 'knn']:
        print(f"\nML Classifier Details:")
        if algorithm == 'svm':
            print(f"  Kernel: RBF (Radial Basis Function)")
            print(f"  Training method: Stratified split with probability-based labels")
        else:
            print(f"  K-value: {optimal_k} (distance-weighted)")
            print(f"  Training method: Stratified split with probability-based labels")
    
    return risk_scores

def update_loan_info_table(df, risk_scores):
    """
    Add delinquency_risk column to loan_info table and update with calculated scores using centralized database methods.
    """
    db_manager = DatabaseManager()
    
    # Create a dictionary mapping payer_id to risk_score
    risk_score_dict = {}
    for payer_id, risk_score in zip(df['payer_id'], risk_scores):
        risk_score_dict[str(payer_id)] = int(risk_score)
    
    # Add the delinquency_risk column if it doesn't exist
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE loan_info ADD COLUMN delinquency_risk INTEGER")
        conn.commit()
        conn.close()
        print("Added delinquency_risk column to loan_info table")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("delinquency_risk column already exists")
        else:
            print(f"Error adding column: {e}")
    
    # Update risk scores using centralized batch update method
    try:
        rows_updated = db_manager.batch_update_delinquency_risks(risk_score_dict)
        print(f"Updated {rows_updated} risk scores in loan_info table")
        
        # Show statistics
        print(f"Risk score statistics:")
        print(f"  Low Risk (0): {np.sum(risk_scores == 0):,} borrowers")
        print(f"  Medium Risk (1): {np.sum(risk_scores == 1):,} borrowers")
        print(f"  High Risk (2): {np.sum(risk_scores == 2):,} borrowers")
        
    except Exception as e:
        print(f"Error updating risk scores: {e}")
        raise

def generate_analysis_report(df, feature_importance_df, model_results, risk_scores):
    """
    Generate comprehensive delinquency analysis report.
    """
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE DELINQUENCY ANALYSIS REPORT")
    print(f"{'='*80}")
    
    print(f"\nDataset Overview:")
    print(f"- Total borrowers analyzed: {len(df):,}")
    print(f"- Delinquent borrowers: {df['is_delinquent'].sum():,}")
    print(f"- Overall delinquency rate: {df['is_delinquent'].mean():.2%}")
    
    print(f"\nModel Performance Summary:")
    for name, results in model_results.items():
        print(f"- {name}: AUC = {results['auc_score']:.4f}")
    
    print(f"\nTop 10 Risk Factors for Delinquency:")
    for i, (_, row) in enumerate(feature_importance_df.head(10).iterrows()):
        print(f"{i+1:2d}. {row['feature']}")
    
    # Risk score distribution with discrete levels
    risk_labels = {0: 'Low Risk', 1: 'Medium Risk', 2: 'High Risk'}
    
    # Create risk categories based on the actual risk scores
    df_with_risk = df.copy()
    df_with_risk['calculated_risk'] = risk_scores
    df_with_risk['risk_category'] = df_with_risk['calculated_risk'].map(risk_labels)
    
    print(f"\nRisk Score Distribution:")
    for risk_level in [0, 1, 2]:
        count = np.sum(risk_scores == risk_level)
        pct = count / len(risk_scores) * 100
        print(f"- {risk_labels[risk_level]} ({risk_level}): {count:,} borrowers ({pct:.1f}%)")
    
    # Correlation with actual delinquency - improved analysis
    print(f"\nRisk Score Validation (Actual Delinquency Rates by Risk Level):")
    for risk_level in [0, 1, 2]:
        level_data = df_with_risk[df_with_risk['calculated_risk'] == risk_level]
        if len(level_data) > 0:
            actual_delinq_rate = level_data['is_delinquent'].mean()
            print(f"- {risk_labels[risk_level]} ({risk_level}):")
            print(f"    Actual Delinquency Rate: {actual_delinq_rate:.1%}")
            print(f"    Borrowers in Level: {len(level_data):,}")
    
    # Show examples by risk level
    for risk_level in [2, 1, 0]:  # Start with highest risk
        level_data = df_with_risk[df_with_risk['calculated_risk'] == risk_level]
        if len(level_data) > 0:
            sample_size = min(5, len(level_data))
            samples = level_data.sample(n=sample_size, random_state=42)[['payer_id', 'calculated_risk', 'is_delinquent']]
            print(f"\n{sample_size} Sample {risk_labels[risk_level]} Borrowers:")
            for _, row in samples.iterrows():
                status = "DELINQUENT" if row['is_delinquent'] else "Current"
                print(f"  Payer {row['payer_id']}: Risk Level {int(row['calculated_risk'])} - {status}")

def parse_arguments():
    """
    Parse command line arguments for delinquency analysis.
    """
    parser = argparse.ArgumentParser(
        description="Comprehensive Delinquency Risk Analysis with Discrete Risk Scores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Risk Scoring Algorithms:
  percentile  - Bottom 60% = Low(0), Next 30% = Medium(1), Top 10% = High(2)
  threshold   - Fixed probability thresholds: <0.6=Low, 0.6-0.9=Medium, >0.9=High
  kmeans      - K-means clustering of probabilities into 3 risk groups
  svm         - Support Vector Machine classifier trained on probability-based risk labels
  knn         - K-Nearest Neighbors classifier with optimal k and distance weighting

Examples:
  python delinquency_analysis.py --algorithm percentile
  python delinquency_analysis.py --algorithm svm
  python delinquency_analysis.py --algorithm knn
  
Database connection is handled automatically through the centralized DatabaseManager.
        """
    )
    
    parser.add_argument(
        "--algorithm",
        choices=['random_forest', 'gradient_boosting', 'logistic_regression', 'neural_network', 'svm', 'knn', 'kmeans'],
        default='random_forest',
        help="Risk scoring algorithm to use (default: random_forest)"
    )
    
    return parser.parse_args()

def main():
    """
    Main execution function for delinquency analysis.
    """
    args = parse_arguments()
    
    print("Starting Comprehensive Delinquency Risk Analysis...")
    print("=" * 60)
    print(f"Algorithm: {args.algorithm}")
    print(f"Risk Levels: 0 (Low), 1 (Medium), 2 (High)")
    print("=" * 60)
    
    # Load and prepare data using centralized database methods
    df = load_comprehensive_dataset()
    df = engineer_features(df)
    X, y, feature_columns, label_encoders = prepare_ml_features(df)
    
    # Train models
    best_model, model_results, scaler = train_delinquency_models(X, y)
    
    # Analyze feature importance
    best_model_name = max(model_results.keys(), key=lambda x: model_results[x]['auc_score'])
    feature_importance_df = analyze_feature_importance(best_model, feature_columns, best_model_name)
    
    # Calculate risk scores using specified algorithm
    risk_scores = calculate_risk_scores(best_model, X, scaler, best_model_name, args.algorithm)
    
    # Update database using centralized methods  
    update_loan_info_table(df, risk_scores)
    
    # Generate report
    generate_analysis_report(df, feature_importance_df, model_results, risk_scores)
    
    print(f"\nDelinquency analysis complete!")
    print(f"The loan_info table has been updated with delinquency_risk scores.")
    print(f"Risk scores: 0 (Low Risk), 1 (Medium Risk), 2 (High Risk)")
    print(f"Algorithm used: {args.algorithm}")

if __name__ == "__main__":
    main()