<img width="1896" height="921" alt="image" src="https://github.com/user-attachments/assets/53d45d22-7b90-47ae-ab45-e9e7a0dd8df2" />Automated EDA & Insights Generator
A web application that automates exploratory data analysis (EDA) for CSV datasets, providing comprehensive visualizations, correlation analysis, insights, and downloadable reports.

Features
CSV Upload: Upload any CSV dataset for analysis
Automated EDA: Comprehensive statistical analysis of your data
Interactive Visualizations: Distribution plots and correlation matrices
Correlation Analysis: Identify strong correlations between variables
Insight Generation: Automatically detect patterns and anomalies
PDF Export: Generate and download professional reports
Prerequisites
Python 3.7+
pip package manager
Installation
Clone or download this repository
Install required packages:
pip install streamlit pandas numpy matplotlib seaborn plotly scipy fpdf2

Usage
Save the code as eda_app.py
Run the application:
streamlit run eda_app.py

The app will open in your default browser at http://localhost:8501
How to Use
Upload Data:
Click "Browse files" to upload a CSV file
The app will automatically load and display basic dataset information
Explore Analysis:
Overview Tab: View dataset shape, data types, and statistical summaries
Visualizations Tab: See distributions of numeric and categorical variables
Correlations Tab: Examine correlation matrices and strong relationships
Insights Tab: Discover automatically generated insights about your data
Report Tab: Generate and download a PDF summary
Download Report:
Click "Generate Report" in the Report tab
Download the PDF with key metrics and summaries

Expected Insights for Sample Data
Correlation: Sales and Quantity will show strong positive correlation
Distribution: Price will show distinct value clusters
Cardinality: Product column will have high uniqueness
Missing Values: None in this clean dataset
Technical Details
Frontend: Streamlit web interface
Visualization: Plotly for interactive charts, Matplotlib/Seaborn for static plots
Analysis: Pandas for data manipulation, SciPy for statistical tests
Reporting: FPDF2 for PDF generation
Layout: Responsive design with tabbed interface
Customization
To modify the application:

Adjust correlation thresholds in show_correlations()
Modify insight generation logic in show_insights()
Add new visualization types in show_visualizations()
Customize PDF report content in the PDFReport class
Limitations
Large datasets (>100MB) may experience performance issues
All analysis is performed in-memory
For optimal performance, datasets should have <100,000 rows

<img width="1896" height="921" alt="image" src="https://github.com/user-attachments/assets/271f5515-80cb-4b29-af30-d386bf8d9abe" />

<img width="1682" height="850" alt="image" src="https://github.com/user-attachments/assets/90d4d502-8953-4b47-9106-078c7758de6a" />

<img width="1699" height="747" alt="image" src="https://github.com/user-attachments/assets/64787789-005d-4aa1-839f-efd0993ae4e7" />

<img width="1707" height="563" alt="image" src="https://github.com/user-attachments/assets/0e71412e-5a6e-4393-be2a-cef17a32d370" />

<img width="1159" height="406" alt="image" src="https://github.com/user-attachments/assets/77f8e346-e9f0-4cfc-ab50-4111ef54d776" />

<img width="1709" height="315" alt="image" src="https://github.com/user-attachments/assets/7d840787-7fa8-460b-bb10-cbbd25852f68" />






