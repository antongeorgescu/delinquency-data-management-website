"""
Exploratory Data Analysis (EDA) with Principal Component Analysis (PCA)
for Student Loan Delinquency Risk Assessment

This script performs comprehensive exploratory data analysis including:
- PCA dimensionality reduction and visualization
- Feature correlation analysis
- Risk distribution analysis across principal components
- Interactive charts and statistical insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime
import argparse
import os
import markdown

# Import existing data processing functions
from delinquency_analysis.delinquency_analysis import load_comprehensive_dataset, engineer_features, prepare_ml_features

warnings.filterwarnings('ignore')

class ExploratoryDataAnalysis:
    """
    Comprehensive EDA class with PCA analysis and visualization capabilities.
    """
    
    def __init__(self, db_path="student_loan_data.db", output_dir="eda_outputs"):
        """
        Initialize EDA with database path and output directory.
        
        Args:
            db_path: Path to SQLite database
            output_dir: Directory to save charts and analysis results
        """
        self.db_path = db_path
        self.output_dir = output_dir
        self.create_output_directory()
        
        # Data containers
        self.raw_df = None
        self.processed_df = None
        self.X_scaled = None
        self.y = None
        self.feature_columns = None
        self.pca = None
        self.pca_components = None
        self.explained_variance = None
        
        print(f"Exploratory Data Analysis initialized")
        print(f"Output directory: {self.output_dir}")
    
    def create_output_directory(self):
        """Create output directory for charts and analysis results."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def generate_analysis_summary_html(self, chart_type, additional_stats=None):
        """
        Generate HTML summary with analysis scope, chart description, and numerical values.
        
        Args:
            chart_type: Type of chart being created
            additional_stats: Dictionary of additional statistics specific to the chart
        """
        base_stats = {
            'sample_size': f"{len(self.processed_df):,}" if self.processed_df is not None else "N/A",
            'features': len(self.feature_columns) if self.feature_columns is not None else "N/A", 
            'delinquency_rate': f"{self.y.mean():.2%}" if self.y is not None else "N/A",
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'database': os.path.basename(self.db_path)
        }
        
        if self.pca is not None and len(self.explained_variance) >= 2:
            base_stats.update({
                'pc1_variance': f"{self.explained_variance[0]:.2%}",
                'pc2_variance': f"{self.explained_variance[1]:.2%}",
                'total_components': len(self.explained_variance),
                'variance_80pct': np.argmax(np.cumsum(self.explained_variance) >= 0.8) + 1,
                'variance_95pct': np.argmax(np.cumsum(self.explained_variance) >= 0.95) + 1
            })
        
        # Merge additional stats
        if additional_stats:
            base_stats.update(additional_stats)
        
        chart_descriptions = {
            'scree_plot': {
                'title': 'PCA Scree Plot Analysis',
                'description': '''This scree plot shows the explained variance for each principal component, helping determine 
                the optimal number of components to retain. The elbow point indicates diminishing returns in variance explanation.''',
                'interpretation': '''• Left plot: Individual variance explained by each component<br>
                • Right plot: Cumulative variance with 80% and 95% reference lines<br>
                • Components before the elbow retain most meaningful information'''
            },
            'pca_scatter': {
                'title': 'PCA Scatter Plot Analysis', 
                'description': '''This scatter plot visualizes borrowers in the reduced dimensional space of the first two 
                principal components, colored by delinquency risk level and sized by loan amount.''',
                'interpretation': '''• Red points: High-risk borrowers (delinquent)<br>
                • Blue points: Low-risk borrowers (non-delinquent)<br>
                • Point size represents loan amount<br>
                • Clustering patterns indicate risk segments'''
            },
            'biplot': {
                'title': 'PCA Biplot Analysis',
                'description': '''This biplot combines the principal component scatter plot with feature loading vectors, 
                showing both borrower positions and feature contributions simultaneously.''',
                'interpretation': '''• Red dots: High-risk borrowers, Blue dots: Low-risk borrowers<br>
                • Green arrows: Feature loading vectors indicating direction of influence<br>
                • Arrow length represents feature importance<br>
                • Features pointing in similar directions are correlated'''
            },
            'feature_contributions': {
                'title': 'Feature Contributions Analysis',
                'description': '''This analysis shows which original features contribute most strongly to each principal component, 
                revealing the underlying structure of the data.''',
                'interpretation': '''• Blue bars: Positive loadings (features increase with component)<br>
                • Red bars: Negative loadings (features decrease with component)<br>
                • Bar length indicates contribution strength<br>
                • Top features define each component's meaning'''
            },
            'correlation_heatmap': {
                'title': 'Feature Correlation Analysis',
                'description': '''This heatmap shows correlations between all numerical features in the dataset, 
                identifying relationships and potential multicollinearity issues.''',
                'interpretation': '''• Red colors: Strong positive correlations (values move together)<br>
                • Blue colors: Strong negative correlations (values move oppositely)<br>
                • White/Light colors: Weak or no correlation<br>
                • Dark diagonal: Perfect self-correlation (value = 1)'''
            },
            'clustering': {
                'title': 'K-means Clustering Analysis',
                'description': '''This visualization shows K-means clustering results in the PCA space, 
                identifying natural groupings of borrowers based on their risk profiles.''',
                'interpretation': '''• Different colors: Distinct clusters identified<br>
                • Symbols indicate risk level (circle/diamond)<br>
                • Point size represents loan amount<br>
                • Cluster separation indicates distinct borrower segments'''
            }
        }
        
        chart_info = chart_descriptions.get(chart_type, {
            'title': 'Analysis Chart',
            'description': 'Interactive visualization of the analysis results.',
            'interpretation': '• Hover over data points for detailed information'
        })
        
        html_summary = f"""
        <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #007bff;">
            <h2 style="color: #0056b3; margin-bottom: 15px;">{chart_info['title']}</h2>
            
            <div style="margin-bottom: 20px;">
                <h3 style="color: #495057; font-size: 16px; margin-bottom: 10px;">📊 Analysis Scope</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 15px;">
                    <div><strong>Sample Size:</strong> {base_stats['sample_size']} borrowers</div>
                    <div><strong>Features:</strong> {base_stats['features']} engineered features</div>
                    <div><strong>Delinquency Rate:</strong> {base_stats['delinquency_rate']}</div>
                    <div><strong>Database:</strong> {base_stats['database']}</div>
                </div>
        """
        
        if 'pc1_variance' in base_stats:
            html_summary += f"""
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
                    <div><strong>PC1 Variance:</strong> {base_stats['pc1_variance']}</div>
                    <div><strong>PC2 Variance:</strong> {base_stats['pc2_variance']}</div>
                    <div><strong>Components (80%):</strong> {base_stats['variance_80pct']}</div>
                    <div><strong>Components (95%):</strong> {base_stats['variance_95pct']}</div>
                </div>
            """
        
        html_summary += f"""
            </div>
            
            <div style="margin-bottom: 20px;">
                <h3 style="color: #495057; font-size: 16px; margin-bottom: 10px;">📈 Chart Description</h3>
                <p style="line-height: 1.6; margin-bottom: 10px;">{chart_info['description']}</p>
            </div>
            
            <div>
                <h3 style="color: #495057; font-size: 16px; margin-bottom: 10px;">🔍 Key Insights</h3>
                <div style="line-height: 1.6;">{chart_info['interpretation']}</div>
            </div>
        """
        
        if additional_stats:
            html_summary += f"""
            <div style="margin-top: 20px;">
                <h3 style="color: #495057; font-size: 16px; margin-bottom: 10px;">📋 Additional Statistics</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
            """
            for key, value in additional_stats.items():
                if key not in base_stats:  # Avoid duplicating base stats
                    formatted_key = key.replace('_', ' ').title()
                    html_summary += f"<div><strong>{formatted_key}:</strong> {value}</div>"
            html_summary += "</div></div>"
        
        html_summary += f"""
            
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d;">
                <strong>Generated:</strong> {base_stats['analysis_date']} | <strong>System:</strong> Student Loan Delinquency EDA
            </div>
        </div>
        """
        
        return html_summary
    
    def write_enhanced_html(self, fig, output_path, chart_type, additional_stats=None):
        """
        Write HTML file with enhanced analysis information.
        
        Args:
            fig: Plotly figure object
            output_path: Path to save the HTML file
            chart_type: Type of chart for summary generation
            additional_stats: Additional statistics specific to the chart
        """
        # Generate the analysis summary
        analysis_html = self.generate_analysis_summary_html(chart_type, additional_stats)
        
        # Get the base HTML from figure
        base_html = fig.to_html(include_plotlyjs='cdn', div_id="chart-div")
        
        # Insert the analysis summary before the chart
        enhanced_html = base_html.replace(
            '<div id="chart-div"',
            f'{analysis_html}<div id="chart-div"'
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        
        return enhanced_html
    
    def load_and_process_data(self):
        """
        Load data from database and apply feature engineering.
        """
        print("Loading comprehensive dataset...")
        self.raw_df = load_comprehensive_dataset(self.db_path)
        
        print("Engineering features...")
        self.processed_df = engineer_features(self.raw_df)
        
        print("Preparing ML features...")
        X, self.y, self.feature_columns, self.label_encoders = prepare_ml_features(self.processed_df)
        
        # Standardize features for PCA
        print("Standardizing features...")
        scaler = StandardScaler()
        self.X_scaled = scaler.fit_transform(X)
        self.scaler = scaler
        
        print(f"Data processing complete:")
        print(f"   - Sample size: {len(self.processed_df):,} borrowers")
        print(f"   - Features: {len(self.feature_columns)} engineered features")
        print(f"   - Delinquency rate: {self.y.mean():.2%}")
        
        return self.processed_df
    
    def perform_pca_analysis(self, n_components=None):
        """
        Perform Principal Component Analysis on the standardized features.
        
        Args:
            n_components: Number of components to keep (None for all)
        """
        if self.X_scaled is None:
            raise ValueError("Data must be loaded and processed first!")
        
        print("Performing Principal Component Analysis...")
        
        # Determine optimal number of components if not specified
        if n_components is None:
            n_components = min(len(self.feature_columns), len(self.processed_df)) - 1
        
        # Fit PCA
        self.pca = PCA(n_components=n_components, random_state=42)
        self.pca_components = self.pca.fit_transform(self.X_scaled)
        
        # Calculate explained variance
        self.explained_variance = self.pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(self.explained_variance)
        
        print(f"PCA Analysis Results:")
        print(f"   - Components extracted: {len(self.explained_variance)}")
        print(f"   - Variance explained by PC1: {self.explained_variance[0]:.2%}")
        print(f"   - Variance explained by PC2: {self.explained_variance[1]:.2%}")
        print(f"   - Cumulative variance (first 5 PCs): {cumulative_variance[4]:.2%}")
        print(f"   - Components for 80% variance: {np.argmax(cumulative_variance >= 0.8) + 1}")
        print(f"   - Components for 95% variance: {np.argmax(cumulative_variance >= 0.95) + 1}")
        
        return self.pca_components
    
    def create_scree_plot(self):
        """
        Create scree plot showing explained variance by each principal component.
        """
        if self.pca is None:
            raise ValueError("PCA must be performed first!")
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Individual Explained Variance', 'Cumulative Explained Variance'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Individual variance
        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(self.explained_variance) + 1)),
                y=self.explained_variance * 100,
                mode='lines+markers',
                name='Explained Variance',
                line=dict(color='royalblue', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Cumulative variance
        cumulative_variance = np.cumsum(self.explained_variance) * 100
        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(cumulative_variance) + 1)),
                y=cumulative_variance,
                mode='lines+markers',
                name='Cumulative Variance',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ),
            row=1, col=2
        )
        
        # Add 80% and 95% reference lines
        fig.add_hline(y=80, line_dash="dash", line_color="green", row=1, col=2)
        fig.add_hline(y=95, line_dash="dash", line_color="orange", row=1, col=2)
        
        fig.update_xaxes(title_text="Principal Component", row=1, col=1)
        fig.update_xaxes(title_text="Principal Component", row=1, col=2)
        fig.update_yaxes(title_text="Explained Variance (%)", row=1, col=1)
        fig.update_yaxes(title_text="Cumulative Variance (%)", row=1, col=2)
        
        fig.update_layout(
            title="PCA Scree Plot: Explained Variance Analysis",
            height=500,
            showlegend=False
        )
        
        # Calculate additional statistics for scree plot
        cumulative_variance = np.cumsum(self.explained_variance)
        additional_stats = {
            'total_variance_captured': f"{cumulative_variance[-1]:.2%}",
            'components_80pct_detail': f"{np.argmax(cumulative_variance >= 0.8) + 1} components explain 80% variance",
            'components_95pct_detail': f"{np.argmax(cumulative_variance >= 0.95) + 1} components explain 95% variance",
            'optimal_components': f"{np.argmax(cumulative_variance >= 0.8) + 1}-{np.argmax(cumulative_variance >= 0.95) + 1} recommended range"
        }
        
        # Save plot with enhanced information
        output_path = os.path.join(self.output_dir, "pca_scree_plot.html")
        self.write_enhanced_html(fig, output_path, 'scree_plot', additional_stats)
        print(f"Enhanced scree plot saved: {output_path}")
        
        return fig
    
    def create_pca_scatter_plot(self):
        """
        Create interactive scatter plot of first two principal components colored by delinquency risk.
        """
        if self.pca_components is None:
            raise ValueError("PCA must be performed first!")
        
        # Create DataFrame for plotting
        plot_df = pd.DataFrame({
            'PC1': self.pca_components[:, 0],
            'PC2': self.pca_components[:, 1],
            'Risk_Level': ['High Risk' if x == 1 else 'Low Risk' for x in self.y],
            'Loan_Amount': self.processed_df['loan_amount'],
            'Annual_Income': self.processed_df['annual_income_cad'],
            'Age': self.processed_df['age'],
            'Delinquency_Rate': self.processed_df['delinquency_rate'].fillna(0)
        })
        
        # Create interactive scatter plot
        fig = px.scatter(
            plot_df,
            x='PC1',
            y='PC2',
            color='Risk_Level',
            size='Loan_Amount',
            hover_data=['Annual_Income', 'Age', 'Delinquency_Rate'],
            title=f"PCA Analysis: Principal Components 1 vs 2<br>PC1 explains {self.explained_variance[0]:.1%}, PC2 explains {self.explained_variance[1]:.1%}",
            labels={
                'PC1': f'First Principal Component ({self.explained_variance[0]:.1%} variance)',
                'PC2': f'Second Principal Component ({self.explained_variance[1]:.1%} variance)'
            },
            color_discrete_map={'High Risk': 'red', 'Low Risk': 'blue'}
        )
        
        fig.update_layout(
            height=600,
            width=800
        )
        
        # Calculate additional statistics for scatter plot
        high_risk_count = sum(self.y)
        low_risk_count = len(self.y) - high_risk_count
        avg_loan_high = plot_df[plot_df['Risk_Level'] == 'High Risk']['Loan_Amount'].mean()
        avg_loan_low = plot_df[plot_df['Risk_Level'] == 'Low Risk']['Loan_Amount'].mean()
        
        additional_stats = {
            'high_risk_borrowers': f"{high_risk_count:,} ({high_risk_count/len(self.y):.1%})",
            'low_risk_borrowers': f"{low_risk_count:,} ({low_risk_count/len(self.y):.1%})",
            'avg_loan_high_risk': f"${avg_loan_high:,.0f}",
            'avg_loan_low_risk': f"${avg_loan_low:,.0f}",
            'risk_loan_difference': f"${avg_loan_high - avg_loan_low:,.0f} higher for high-risk"
        }
        
        # Save plot with enhanced information
        output_path = os.path.join(self.output_dir, "pca_scatter_plot.html")
        self.write_enhanced_html(fig, output_path, 'pca_scatter', additional_stats)
        print(f"Enhanced PCA scatter plot saved: {output_path}")
        
        return fig
    
    def create_biplot(self, pc1=0, pc2=1, top_features=15):
        """
        Create PCA biplot showing both data points and feature loading vectors.
        
        Args:
            pc1: First principal component index (default 0)
            pc2: Second principal component index (default 1) 
            top_features: Number of top contributing features to show (default 15)
        """
        if self.pca is None:
            raise ValueError("PCA must be performed first!")
        
        # Get feature loadings (components)
        loadings = self.pca.components_.T * np.sqrt(self.pca.explained_variance_)
        
        # Create figure
        fig = go.Figure()
        
        # Add data points
        risk_colors = ['blue' if x == 0 else 'red' for x in self.y]
        
        fig.add_trace(go.Scatter(
            x=self.pca_components[:, pc1],
            y=self.pca_components[:, pc2],
            mode='markers',
            marker=dict(
                color=risk_colors,
                size=6,
                opacity=0.6,
                line=dict(width=0.5, color='white')
            ),
            name='Borrowers',
            hovertemplate=f'PC{pc1+1}: %{{x:.2f}}<br>PC{pc2+1}: %{{y:.2f}}<extra></extra>'
        ))
        
        # Calculate feature importance for the selected components
        feature_importance = np.abs(loadings[:, pc1]) + np.abs(loadings[:, pc2])
        top_indices = np.argsort(feature_importance)[-top_features:]
        
        # Add feature vectors for top contributing features
        scale_factor = 3  # Scale factor for visibility
        
        for i in top_indices:
            feature_name = self.feature_columns[i]
            
            # Shorten long feature names
            if len(feature_name) > 20:
                display_name = feature_name[:17] + "..."
            else:
                display_name = feature_name
            
            fig.add_trace(go.Scatter(
                x=[0, loadings[i, pc1] * scale_factor],
                y=[0, loadings[i, pc2] * scale_factor],
                mode='lines+text',
                line=dict(color='green', width=2),
                text=['', display_name],
                textposition='top center',
                textfont=dict(size=10, color='darkgreen'),
                name=display_name,
                showlegend=False,
                hovertemplate=f'{feature_name}<br>PC{pc1+1} loading: {loadings[i, pc1]:.3f}<br>PC{pc2+1} loading: {loadings[i, pc2]:.3f}<extra></extra>'
            ))
        
        fig.update_layout(
            title=f"PCA Biplot: Components {pc1+1} vs {pc2+1}<br>Top {top_features} Contributing Features",
            xaxis_title=f'PC{pc1+1} ({self.explained_variance[pc1]:.1%} variance)',
            yaxis_title=f'PC{pc2+1} ({self.explained_variance[pc2]:.1%} variance)',
            height=700,
            width=900,
            hovermode='closest'
        )
        
        # Calculate additional statistics for biplot
        high_risk_mask = (self.y == 1)
        pc1_risk_separation = np.abs(np.mean(self.pca_components[high_risk_mask, pc1]) - np.mean(self.pca_components[~high_risk_mask, pc1]))
        pc2_risk_separation = np.abs(np.mean(self.pca_components[high_risk_mask, pc2]) - np.mean(self.pca_components[~high_risk_mask, pc2]))
        
        additional_stats = {
            'features_displayed': f"{top_features} most important features",
            'pc1_risk_separation': f"{pc1_risk_separation:.2f} standard deviations",
            'pc2_risk_separation': f"{pc2_risk_separation:.2f} standard deviations",
            'total_features_analyzed': f"{len(self.feature_columns)} original features"
        }
        
        # Save plot with enhanced information 
        output_path = os.path.join(self.output_dir, f"pca_biplot_pc{pc1+1}_vs_pc{pc2+1}.html")
        self.write_enhanced_html(fig, output_path, 'biplot', additional_stats)
        print(f"Enhanced PCA biplot saved: {output_path}")
        
        return fig
    
    def analyze_feature_contributions(self, top_n=20):
        """
        Analyze and visualize which original features contribute most to each principal component.
        
        Args:
            top_n: Number of top features to display for each component
        """
        if self.pca is None:
            raise ValueError("PCA must be performed first!")
        
        # Create feature contribution analysis for first few components
        n_components_to_analyze = min(5, len(self.explained_variance))
        
        fig = make_subplots(
            rows=n_components_to_analyze, cols=1,
            subplot_titles=[f'PC{i+1} Feature Contributions ({self.explained_variance[i]:.1%} variance)' 
                          for i in range(n_components_to_analyze)],
            vertical_spacing=0.08
        )
        
        for pc in range(n_components_to_analyze):
            # Get loadings for this component
            loadings = self.pca.components_[pc]
            
            # Get top positive and negative loadings
            loading_df = pd.DataFrame({
                'Feature': self.feature_columns,
                'Loading': loadings,
                'Abs_Loading': np.abs(loadings)
            })
            
            top_features = loading_df.nlargest(top_n, 'Abs_Loading')
            
            # Create horizontal bar chart
            colors = ['red' if x < 0 else 'blue' for x in top_features['Loading']]
            
            fig.add_trace(
                go.Bar(
                    x=top_features['Loading'],
                    y=top_features['Feature'],
                    orientation='h',
                    marker_color=colors,
                    name=f'PC{pc+1}',
                    showlegend=False
                ),
                row=pc+1, col=1
            )
        
        fig.update_layout(
            title="Feature Contributions to Principal Components",
            height=300 * n_components_to_analyze,
            showlegend=False
        )
        
        # Update x-axis labels
        for i in range(n_components_to_analyze):
            fig.update_xaxes(title_text="Feature Loading", row=i+1, col=1)
        
        # Calculate additional statistics for feature contributions
        total_features_analyzed = n_components_to_analyze
        avg_contribution = np.mean([np.mean(np.abs(self.pca.components_[i])) for i in range(n_components_to_analyze)])
        
        additional_stats = {
            'components_analyzed': f"{total_features_analyzed} principal components",
            'features_per_component': f"Top {top_n} features displayed per component",
            'avg_feature_contribution': f"{avg_contribution:.3f} average absolute loading",
            'variance_accounted': f"{np.sum(self.explained_variance[:n_components_to_analyze]):.2%} total variance"
        }
        
        # Save plot with enhanced information
        output_path = os.path.join(self.output_dir, "pca_feature_contributions.html")
        self.write_enhanced_html(fig, output_path, 'feature_contributions', additional_stats)
        print(f"Enhanced feature contributions analysis saved: {output_path}")
        
        return fig
    
    def create_correlation_heatmap(self):
        """
        Create correlation heatmap of original features.
        """
        if self.processed_df is None:
            raise ValueError("Data must be loaded first!")
        
        # Select only numerical features that exist in processed_df
        available_numerical_cols = []
        for col in self.processed_df.columns:
            if self.processed_df[col].dtype in ['int64', 'float64'] and col != 'payer_id':
                available_numerical_cols.append(col)
        
        numerical_features = self.processed_df[available_numerical_cols]
        
        # Calculate correlation matrix
        correlation_matrix = numerical_features.corr()
        
        # Create interactive heatmap
        fig = px.imshow(
            correlation_matrix,
            title="Feature Correlation Heatmap",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        
        fig.update_layout(
            height=800,
            width=800
        )
        
        # Calculate additional statistics for correlation heatmap
        correlation_values = correlation_matrix.values
        # Get upper triangle (excluding diagonal) for correlation statistics
        upper_triangle = correlation_values[np.triu_indices_from(correlation_values, k=1)]
        high_correlations = np.sum(np.abs(upper_triangle) > 0.7)
        moderate_correlations = np.sum((np.abs(upper_triangle) > 0.5) & (np.abs(upper_triangle) <= 0.7))
        
        additional_stats = {
            'features_analyzed': f"{len(available_numerical_cols)} numerical features",
            'correlation_pairs': f"{len(upper_triangle):,} unique feature pairs",
            'high_correlations': f"{high_correlations} pairs with |r| > 0.7",
            'moderate_correlations': f"{moderate_correlations} pairs with 0.5 < |r| ≤ 0.7",
            'max_correlation': f"{np.max(np.abs(upper_triangle)):.2f} maximum absolute correlation"
        }
        
        # Save plot with enhanced information
        output_path = os.path.join(self.output_dir, "feature_correlation_heatmap.html")
        self.write_enhanced_html(fig, output_path, 'correlation_heatmap', additional_stats)
        print(f"Enhanced correlation heatmap saved: {output_path}")
        
        return fig
    
    def perform_clustering_analysis(self, n_clusters=3):
        """
        Perform K-means clustering on PCA components and visualize results.
        
        Args:
            n_clusters: Number of clusters for K-means
        """
        if self.pca_components is None:
            raise ValueError("PCA must be performed first!")
        
        print(f"Performing K-means clustering with {n_clusters} clusters...")
        
        # Use first few principal components for clustering
        pca_for_clustering = self.pca_components[:, :5]  # First 5 components
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(pca_for_clustering)
        
        # Create DataFrame for plotting
        plot_df = pd.DataFrame({
            'PC1': self.pca_components[:, 0],
            'PC2': self.pca_components[:, 1],
            'Cluster': [f'Cluster {i+1}' for i in cluster_labels],
            'Risk_Level': ['High Risk' if x == 1 else 'Low Risk' for x in self.y],
            'Loan_Amount': self.processed_df['loan_amount'],
            'Annual_Income': self.processed_df['annual_income_cad']
        })
        
        # Create clustering visualization
        fig = px.scatter(
            plot_df,
            x='PC1',
            y='PC2',
            color='Cluster',
            symbol='Risk_Level',
            size='Loan_Amount',
            hover_data=['Annual_Income'],
            title=f"K-means Clustering Analysis on PCA Components<br>({n_clusters} clusters identified)",
            labels={
                'PC1': f'PC1 ({self.explained_variance[0]:.1%} variance)',
                'PC2': f'PC2 ({self.explained_variance[1]:.1%} variance)'
            }
        )
        
        fig.update_layout(height=600, width=800)
        
        # Calculate additional statistics for clustering
        cluster_sizes = [np.sum(cluster_labels == i) for i in range(n_clusters)]
        cluster_risk_rates = [np.mean(self.y[cluster_labels == i]) for i in range(n_clusters)]
        silhouette_score = 0  # Could add silhouette analysis if sklearn imported
        
        additional_stats = {
            'clusters_identified': f"{n_clusters} distinct clusters",
            'largest_cluster': f"{max(cluster_sizes):,} borrowers ({max(cluster_sizes)/len(cluster_labels):.1%})", 
            'smallest_cluster': f"{min(cluster_sizes):,} borrowers ({min(cluster_sizes)/len(cluster_labels):.1%})",
            'highest_risk_cluster': f"{max(cluster_risk_rates):.1%} delinquency rate",
            'lowest_risk_cluster': f"{min(cluster_risk_rates):.1%} delinquency rate",
            'risk_range': f"{max(cluster_risk_rates) - min(cluster_risk_rates):.1%} percentage point spread"
        }
        
        # Save plot with enhanced information
        output_path = os.path.join(self.output_dir, f"pca_clustering_k{n_clusters}.html")
        self.write_enhanced_html(fig, output_path, 'clustering', additional_stats)
        print(f"Enhanced clustering analysis saved: {output_path}")
        
        # Analyze cluster characteristics
        cluster_analysis = self.analyze_cluster_characteristics(cluster_labels)
        
        return fig, cluster_labels, cluster_analysis
    
    def analyze_cluster_characteristics(self, cluster_labels):
        """
        Analyze characteristics of each cluster.
        
        Args:
            cluster_labels: Cluster assignments for each data point
        """
        cluster_df = self.processed_df.copy()
        cluster_df['Cluster'] = cluster_labels
        
        # Analysis by cluster
        cluster_stats = []
        
        for cluster_id in sorted(cluster_df['Cluster'].unique()):
            cluster_data = cluster_df[cluster_df['Cluster'] == cluster_id]
            
            stats = {
                'Cluster': f'Cluster {cluster_id + 1}',
                'Size': len(cluster_data),
                'Size_Pct': len(cluster_data) / len(cluster_df) * 100,
                'Delinquency_Rate': cluster_data['is_delinquent'].mean() * 100,
                'Avg_Age': cluster_data['age'].mean(),
                'Avg_Income': cluster_data['annual_income_cad'].mean(),
                'Avg_Loan_Amount': cluster_data['loan_amount'].mean(),
                'Avg_Payment_Ratio': cluster_data['payment_to_income_ratio'].mean()
            }
            cluster_stats.append(stats)
        
        cluster_analysis_df = pd.DataFrame(cluster_stats)
        
        print("\nCluster Analysis Summary:")
        print(cluster_analysis_df.round(2))
        
        # Save cluster analysis
        output_path = os.path.join(self.output_dir, "cluster_analysis_summary.csv")
        cluster_analysis_df.to_csv(output_path, index=False)
        print(f"Cluster analysis saved: {output_path}")
        
        return cluster_analysis_df
    
    def analyze_top_feature_loadings(self, top_n=10, n_components=5):
        """
        Analyze the most important features for each principal component based on loadings.
        
        Args:
            top_n: Number of top features to identify per component
            n_components: Number of principal components to analyze
        
        Returns:
            Dictionary containing detailed feature analysis per component
        """
        if self.pca is None:
            raise ValueError("PCA must be performed first!")
        
        print(f"Analyzing top {top_n} features for first {n_components} principal components...")
        
        # Limit analysis to available components
        n_components = min(n_components, len(self.explained_variance))
        
        feature_analysis = {}
        
        for pc in range(n_components):
            # Get loadings for this component
            loadings = self.pca.components_[pc]
            
            # Create DataFrame with feature names and loadings
            loading_df = pd.DataFrame({
                'Feature': self.feature_columns,
                'Loading': loadings,
                'Abs_Loading': np.abs(loadings)
            })
            
            # Sort by absolute loading (importance)
            loading_df = loading_df.sort_values('Abs_Loading', ascending=False)
            
            # Get top features
            top_features = loading_df.head(top_n)
            
            # Categorize features by loading direction and magnitude
            positive_features = top_features[top_features['Loading'] > 0].copy()
            negative_features = top_features[top_features['Loading'] < 0].copy()
            
            # Calculate feature importance statistics
            max_loading = top_features['Abs_Loading'].max()
            avg_loading = top_features['Abs_Loading'].mean()
            loading_std = top_features['Abs_Loading'].std()
            
            # Store analysis for this component
            feature_analysis[f'PC{pc+1}'] = {
                'explained_variance': self.explained_variance[pc],
                'top_features': top_features,
                'positive_features': positive_features,
                'negative_features': negative_features,
                'max_loading': max_loading,
                'avg_loading': avg_loading,
                'loading_std': loading_std,
                'feature_count': len(top_features)
            }
        
        return feature_analysis
    
    def generate_feature_importance_markdown(self, feature_analysis):
        """
        Generate markdown section for feature importance analysis.
        
        Args:
            feature_analysis: Dictionary from analyze_top_feature_loadings method
        
        Returns:
            Formatted markdown string
        """
        markdown = "\n## 🔍 Feature Importance Analysis\n\n"
        markdown += "This section identifies the most important features for each principal component based on their loadings. "
        markdown += "Features with higher absolute loadings have more influence on the component.\n\n"
        
        for pc_name, analysis in feature_analysis.items():
            variance_pct = analysis['explained_variance'] * 100
            
            # Component header
            markdown += f"### {pc_name} ({variance_pct:.2f}% variance explained)\n\n"
            
            # Top features table
            markdown += "#### Most Influential Features:\n\n"
            markdown += "| Rank | Feature | Loading | Impact | Description |\n"
            markdown += "|------|---------|---------|--------|-------------|\n"
            
            for idx, (_, feature_row) in enumerate(analysis['top_features'].iterrows(), 1):
                feature_name = feature_row['Feature']
                loading = feature_row['Loading']
                abs_loading = feature_row['Abs_Loading']
                
                # Determine impact direction and magnitude
                if loading > 0:
                    impact = "📈 Positive"
                    description = "Higher values increase component score"
                else:
                    impact = "📉 Negative" 
                    description = "Higher values decrease component score"
                
                # Add magnitude descriptor
                if abs_loading > analysis['avg_loading'] + analysis['loading_std']:
                    magnitude = " (High)"
                elif abs_loading > analysis['avg_loading']:
                    magnitude = " (Medium)"
                else:
                    magnitude = " (Low)"
                
                impact += magnitude
                
                markdown += f"| {idx} | `{feature_name}` | {loading:.4f} | {impact} | {description} |\n"
            
            # Feature interpretation
            markdown += f"\n#### {pc_name} Interpretation:\n\n"
            
            # Positive drivers
            if len(analysis['positive_features']) > 0:
                markdown += "**Positive Drivers:** Features that increase this component:\n"
                for _, row in analysis['positive_features'].head(3).iterrows():
                    markdown += f"- `{row['Feature']}` (loading: {row['Loading']:.3f})\n"
                markdown += "\n"
            
            # Negative drivers  
            if len(analysis['negative_features']) > 0:
                markdown += "**Negative Drivers:** Features that decrease this component:\n"
                for _, row in analysis['negative_features'].head(3).iterrows():
                    markdown += f"- `{row['Feature']}` (loading: {row['Loading']:.3f})\n"
                markdown += "\n"
            
            # Component statistics
            markdown += "**Component Statistics:**\n"
            markdown += f"- Maximum loading magnitude: {analysis['max_loading']:.4f}\n"
            markdown += f"- Average loading magnitude: {analysis['avg_loading']:.4f}\n"
            markdown += f"- Loading standard deviation: {analysis['loading_std']:.4f}\n\n"
            
            markdown += "---\n\n"
        
        return markdown
    
    def generate_comprehensive_report(self):
        """
        Generate a comprehensive EDA report with all analyses and insights.
        """
        print("Generating comprehensive EDA report...")
        
        # First, generate the feature importance analysis
        feature_analysis = self.analyze_top_feature_loadings(top_n=10, n_components=5)
        feature_importance_section = self.generate_feature_importance_markdown(feature_analysis)
        
        report = f"""
# Exploratory Data Analysis Report
## Student Loan Delinquency Risk Assessment

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Database:** {self.db_path}

## Dataset Overview

- **Total Borrowers:** {len(self.processed_df):,}
- **Total Features:** {len(self.feature_columns)} (engineered)
- **Delinquency Rate:** {self.y.mean():.2%}
- **Data Quality:** Complete records after feature engineering

## Principal Component Analysis Results

### Variance Explanation
- **PC1:** {self.explained_variance[0]:.2%} of total variance
- **PC2:** {self.explained_variance[1]:.2%} of total variance
- **PC3:** {self.explained_variance[2]:.2%} of total variance
- **First 5 PCs:** {np.sum(self.explained_variance[:5]):.2%} of total variance
- **Components for 80% variance:** {np.argmax(np.cumsum(self.explained_variance) >= 0.8) + 1}
- **Components for 95% variance:** {np.argmax(np.cumsum(self.explained_variance) >= 0.95) + 1}

### Key Insights from PCA

1. **Dimensionality Reduction:** The dataset's {len(self.feature_columns)} features can be effectively 
   reduced to a smaller number of components while retaining most variance.

2. **Feature Relationships:** PCA reveals underlying relationships between different risk factors
   and borrower characteristics.

3. **Risk Patterns:** The principal components help identify natural groupings of borrowers
   based on their risk profiles.

{feature_importance_section}

## 📈 Generated Visualizations

All interactive charts and reports have been saved to the `{self.output_dir}` directory:

### 📊 Interactive Visualizations
1. **pca_scree_plot.html** - Variance explained by each component
2. **pca_scatter_plot.html** - PC1 vs PC2 scatter plot colored by risk
3. **pca_biplot_pc1_vs_pc2.html** - Biplot showing feature loading vectors
4. **pca_feature_contributions.html** - Feature contributions to each PC
5. **feature_correlation_heatmap.html** - Correlation matrix of original features
6. **pca_clustering_k3.html** - K-means clustering on PCA components

### 📄 Analysis Reports
7. **eda_comprehensive_report.md** - Markdown version of this report
8. **eda_comprehensive_report.html** - HTML version with enhanced styling

## Business Implications

### Risk Segmentation
The PCA analysis reveals natural risk segments that can be used for:
- Targeted intervention strategies
- Customized loan products
- Proactive risk management

### Feature Importance
The principal components identify the most important combinations of features
for delinquency prediction, enabling more efficient risk assessment.

### Portfolio Management
Understanding the principal components helps in:
- Diversification strategies
- Risk concentration analysis
- Performance monitoring

---
*This report was generated automatically by the Exploratory Data Analysis system.*
"""
        
        # Save report
        output_path = os.path.join(self.output_dir, "eda_comprehensive_report.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Comprehensive report saved: {output_path}")
        return report
    
    def convert_markdown_to_html(self, markdown_content, output_filename="eda_comprehensive_report.html"):
        """
        Convert markdown content to HTML with proper styling.
        
        Args:
            markdown_content: The markdown content to convert
            output_filename: Name of the HTML output file
        """
        print("Converting comprehensive report to HTML...")
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['markdown.extensions.tables', 'markdown.extensions.toc']
        )
        
        # Create styled HTML document
        styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDA Comprehensive Report - Student Loan Delinquency Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 25px;
        }}
        h4 {{
            color: #95a5a6;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background-color: white;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        code {{
            background-color: #f1f2f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        strong {{
            color: #2c3e50;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
        }}
        .generated-info {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""
        
        # Save HTML file
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(styled_html)
        
        print(f"HTML report saved: {output_path}")
        return output_path
    
    def convert_markdown_to_html(self, markdown_content, output_filename="eda_comprehensive_report.html"):
        """
        Convert markdown content to HTML with proper styling.
        
        Args:
            markdown_content: The markdown content to convert
            output_filename: Name of the HTML output file
        """
        print("Converting comprehensive report to HTML...")
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['markdown.extensions.tables', 'markdown.extensions.toc']
        )
        
        # Create styled HTML document
        styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDA Comprehensive Report - Student Loan Delinquency Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 25px;
        }}
        h4 {{
            color: #95a5a6;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background-color: white;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        code {{
            background-color: #f1f2f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        strong {{
            color: #2c3e50;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
        }}
        .generated-info {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""
        
        # Save HTML file
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(styled_html)
        
        print(f"HTML report saved: {output_path}")
        return output_path

def main():
    """
    Main function to run the complete exploratory data analysis.
    """
    parser = argparse.ArgumentParser(description='Exploratory Data Analysis with PCA')
    parser.add_argument('--db_path', default='student_loan_data.db', 
                       help='Path to SQLite database')
    parser.add_argument('--output_dir', default='eda_outputs', 
                       help='Output directory for charts and reports')
    parser.add_argument('--n_components', type=int, default=None,
                       help='Number of PCA components (default: auto)')
    parser.add_argument('--n_clusters', type=int, default=3,
                       help='Number of clusters for K-means analysis')
    
    args = parser.parse_args()
    
    print("Starting Exploratory Data Analysis with PCA...")
    print(f"Database: {args.db_path}")
    print(f"Output directory: {args.output_dir}")
    
    # Initialize EDA
    eda = ExploratoryDataAnalysis(args.db_path, args.output_dir)
    
    try:
        # Step 1: Load and process data
        print("\\n" + "="*60)
        print("STEP 1: DATA LOADING AND PROCESSING")
        print("="*60)
        eda.load_and_process_data()
        
        # Step 2: Perform PCA analysis
        print("\\n" + "="*60)
        print("STEP 2: PRINCIPAL COMPONENT ANALYSIS")
        print("="*60)
        eda.perform_pca_analysis(args.n_components)
        
        # Step 3: Create visualizations
        print("\\n" + "="*60)
        print("STEP 3: CREATING VISUALIZATIONS")
        print("="*60)
        
        # Scree plot
        print("Creating scree plot...")
        eda.create_scree_plot()
        
        # PCA scatter plot
        print("Creating PCA scatter plot...")
        eda.create_pca_scatter_plot()
        
        # Biplot
        print("Creating PCA biplot...")
        eda.create_biplot()
        
        # Feature contributions
        print("Analyzing feature contributions...")
        eda.analyze_feature_contributions()
        
        # Correlation heatmap
        print("Creating correlation heatmap...")
        eda.create_correlation_heatmap()
        
        # Step 4: Clustering analysis
        print("\\n" + "="*60)
        print("STEP 4: CLUSTERING ANALYSIS")
        print("="*60)
        eda.perform_clustering_analysis(args.n_clusters)
        
        # Step 5: Generate comprehensive report
        print("\\n" + "="*60)
        print("STEP 5: GENERATING REPORTS")
        print("="*60)
        markdown_report = eda.generate_comprehensive_report()
        
        # Convert to HTML
        eda.convert_markdown_to_html(markdown_report)
        
        print("\\n" + "="*60)
        print("ANALYSIS COMPLETE!")
        print("="*60)
        print(f"All visualizations and reports saved to: {args.output_dir}")
        print("\\n📊 Generated Files:")
        print("  • 6 Interactive HTML charts")
        print("  • 1 Comprehensive markdown report (eda_comprehensive_report.md)")
        print("  • 1 Styled HTML report (eda_comprehensive_report.html)")
        print("\\n💡 Open the HTML files in your browser to explore the interactive charts and reports.")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main()