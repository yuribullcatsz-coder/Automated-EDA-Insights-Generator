import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime

import streamlit as st

from eda_analysis import (
    build_insights,
    dtypes_summary,
    memory_usage_mb,
    missing_summary,
    pdf_numeric_summary_lines,
    strong_correlations,
)

def _inject_styles():
    st.markdown(
        """
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
""",
        unsafe_allow_html=True,
    )


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Automated EDA Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(3)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, body)
        self.ln()


def main():
    st.markdown(
        '<h1 class="main-header">📊 Automated EDA & Insights Generator</h1>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if df.empty:
                st.warning("The CSV has no rows. Add data or choose another file.")
                return
            st.success(
                f"Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns"
            )

            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["📊 Overview", "📈 Visualizations", "🔍 Correlations", "💡 Insights", "📄 Report"]
            )

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
    st.markdown(
        '<h2 class="section-header">Dataset Overview</h2>',
        unsafe_allow_html=True,
    )

    missing_total, _ = missing_summary(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", missing_total)
    col4.metric("Memory Usage", f"{memory_usage_mb(df):.2f} MB")

    st.subheader("Data Types")
    st.dataframe(dtypes_summary(df))

    st.subheader("First 5 Rows")
    st.dataframe(df.head())

    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include="all"))


def show_visualizations(df):
    st.markdown(
        '<h2 class="section-header">Visualizations</h2>',
        unsafe_allow_html=True,
    )

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if numeric_cols:
        st.subheader("Distribution of Numeric Variables")
        cols = st.columns(min(3, len(numeric_cols)))
        for i, col in enumerate(numeric_cols[:6]):
            with cols[i % 3]:
                sub = df[[col]].dropna()
                if sub.empty:
                    st.caption(f"{col}: no values to plot")
                    continue
                fig = px.histogram(sub, x=col, title=f"Distribution of {col}")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

    if categorical_cols:
        st.subheader("Categorical Variable Distributions")
        cols = st.columns(min(3, len(categorical_cols)))
        for i, col in enumerate(categorical_cols[:6]):
            with cols[i % 3]:
                vc = df[col].value_counts().head(10)
                if vc.empty:
                    st.caption(f"{col}: no values to plot")
                    continue
                fig = px.bar(
                    x=vc.index.astype(str),
                    y=vc.values,
                    labels={"x": col, "y": "Count"},
                    title=f"Top categories: {col}",
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)


def show_correlations(df):
    st.markdown(
        '<h2 class="section-header">Correlation Analysis</h2>',
        unsafe_allow_html=True,
    )

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) > 1:
        corr_subset = df[numeric_cols].dropna(axis=1, how="all")
        if corr_subset.shape[1] < 2:
            st.warning("Not enough numeric columns with data for correlation analysis.")
            return
        corr_matrix = corr_subset.corr(numeric_only=True)

        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Strong Correlations")
        strong_df = strong_correlations(corr_matrix, threshold=0.5)
        if not strong_df.empty:
            st.dataframe(strong_df)
        else:
            st.info("No strong correlations (|r| > 0.5) found")
    else:
        st.warning("Need at least two numeric columns for correlation analysis")


def show_insights(df):
    st.markdown(
        '<h2 class="section-header">Key Insights</h2>',
        unsafe_allow_html=True,
    )
    for insight in build_insights(df):
        st.markdown(
            f'<div class="insight-card">{insight}</div>',
            unsafe_allow_html=True,
        )


def generate_report(df):
    st.markdown(
        '<h2 class="section-header">Generate PDF Report</h2>',
        unsafe_allow_html=True,
    )

    if st.button("Generate Report"):
        pdf = PDFReport()
        pdf.add_page()

        missing_total, _ = missing_summary(df)
        pdf.chapter_title("Dataset Overview")
        pdf.chapter_body(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        pdf.chapter_body(f"Missing Values: {missing_total}")

        pdf.chapter_title("Statistical Summary")
        for line in pdf_numeric_summary_lines(df, max_cols=3):
            pdf.chapter_body(line)

        raw = pdf.output(dest="S")
        if isinstance(raw, str):
            pdf_bytes = raw.encode("latin-1")
        else:
            # fpdf2 often returns bytearray; Streamlit download_button requires bytes
            pdf_bytes = bytes(raw)

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"eda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Automated EDA & Insights Generator",
        page_icon="📊",
        layout="wide",
    )
    _inject_styles()
    main()
