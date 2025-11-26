# requirements.txt
"""
streamlit
pandas
numpy
matplotlib
seaborn
plotly
scipy
fpdf2
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr
from fpdf import FPDF
import io
import base64
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Automated EDA & Insights Generator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4472c4;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .insight-card {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #4472c4;
    }
    .metric-card {
        background-color: #e7f3ff;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Automated EDA Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(3)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

def main():
    st.markdown('<h1 class="main-header">📊 Automated EDA & Insights Generator</h1>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns")
            
            # Create tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Visualizations", "🔍 Correlations", "💡 Insights", "📄 Report"])
            
            with tab1:
                show_overview(df)
            
            with tab2:
                show_visualizations(df)
            
            with tab3:
                show_correlations(df)
            
            with tab4:
                show_insights(df)
            
            with tab5:
                generate_report(df)
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        st.info("Please upload a CSV file to begin analysis")

def show_overview(df):
    st.markdown('<h2 class="section-header">Dataset Overview</h2>', unsafe_allow_html=True)
    
    # Basic info
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Data types
    st.subheader("Data Types")
    dtypes_df = df.dtypes.value_counts().reset_index()
    dtypes_df.columns = ['Type', 'Count']
    st.dataframe(dtypes_df)
    
    # First few rows
    st.subheader("First 5 Rows")
    st.dataframe(df.head())
    
    # Descriptive statistics
    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include='all'))

def show_visualizations(df):
    st.markdown('<h2 class="section-header">Visualizations</h2>', unsafe_allow_html=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if numeric_cols:
        # Distribution plots
        st.subheader("Distribution of Numeric Variables")
        cols = st.columns(min(3, len(numeric_cols)))
        for i, col in enumerate(numeric_cols[:6]):  # Limit to first 6
            with cols[i % 3]:
                fig = px.histogram(df, x=col, title=f"Distribution of {col}")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    if categorical_cols:
        # Categorical distributions
        st.subheader("Categorical Variable Distributions")
        cols = st.columns(min(3, len(categorical_cols)))
        for i, col in enumerate(categorical_cols[:6]):  # Limit to first 6
            with cols[i % 3]:
                value_counts = df[col].value_counts().head(10)  # Top 10 categories
                fig = px.bar(value_counts, title=f"Distribution of {col}")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

def show_correlations(df):
    st.markdown('<h2 class="section-header">Correlation Analysis</h2>', unsafe_allow_html=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 1:
        # Correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale='RdBu'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation insights
        st.subheader("Strong Correlations")
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:  # Strong correlation threshold
                    strong_corr.append({
                        'Feature 1': corr_matrix.columns[i],
                        'Feature 2': corr_matrix.columns[j],
                        'Correlation': corr_val
                    })
        
        if strong_corr:
            strong_corr_df = pd.DataFrame(strong_corr)
            strong_corr_df = strong_corr_df.sort_values(by='Correlation', key=abs, ascending=False)
            st.dataframe(strong_corr_df)
        else:
            st.info("No strong correlations (|r| > 0.5) found")
    else:
        st.warning("No numeric columns found for correlation analysis")

def show_insights(df):
    st.markdown('<h2 class="section-header">Key Insights</h2>', unsafe_allow_html=True)
    
    insights = []
    
    # Missing values insight
    missing_count = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = (missing_count / total_cells) * 100
    
    if missing_pct > 0:
        insights.append(f"⚠️ Dataset has {missing_count} missing values ({missing_pct:.2f}% of total data)")
    
    # Data types insight
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    insights.append(f"📊 Dataset contains {len(numeric_cols)} numeric and {len(categorical_cols)} categorical features")
    
    # Unique values insight
    high_cardinality = [col for col in categorical_cols if df[col].nunique() > 50]
    if high_cardinality:
        insights.append(f"🔍 Features with high cardinality: {', '.join(high_cardinality)}")
    
    # Statistical insights
    if numeric_cols:
        for col in numeric_cols[:3]:  # Check first 3 numeric columns
            skewness = df[col].skew()
            if abs(skewness) > 1:
                direction = "right" if skewness > 0 else "left"
                insights.append(f"📈 Feature '{col}' is highly skewed to the {direction} (skewness: {skewness:.2f})")
    
    # Show insights
    for i, insight in enumerate(insights):
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)

def generate_report(df):
    st.markdown('<h2 class="section-header">Generate PDF Report</h2>', unsafe_allow_html=True)
    
    if st.button("Generate Report"):
        # Create PDF
        pdf = PDFReport()
        pdf.add_page()
        
        # Add content to PDF
        pdf.chapter_title('Dataset Overview')
        pdf.chapter_body(f'Rows: {df.shape[0]}, Columns: {df.shape[1]}')
        pdf.chapter_body(f'Missing Values: {df.isnull().sum().sum()}')
        
        # Add statistical summary
        pdf.chapter_title('Statistical Summary')
        for col in df.select_dtypes(include=[np.number]).columns[:3]:  # Limit to first 3
            pdf.chapter_body(f'{col}: Mean={df[col].mean():.2f}, Std={df[col].std():.2f}')
        
        # Save PDF to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        
        # Create download button
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"eda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
