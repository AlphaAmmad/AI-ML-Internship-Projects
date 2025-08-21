# 🚀 AI-Powered Dynamic Expense Forecasting System

A sophisticated web application that uses machine learning to predict future company expenses based on historical CSV data. Built with Python, Flask, and advanced ML algorithms.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.1+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🤖 AI-Powered Forecasting**: Uses Linear Regression and Random Forest algorithms with automatic model selection
- **📊 Interactive Visualizations**: Beautiful charts powered by Plotly.js
- **🔧 Robust Data Processing**: Handles various CSV formats, missing values, and data quality issues
- **📱 Responsive Web Interface**: Modern Bootstrap-based UI that works on all devices
- **📈 Multiple Forecast Periods**: Generate forecasts for 1-24 months
- **💾 Export Capabilities**: Download forecasts as CSV files
- **🛡️ Data Validation**: Comprehensive validation and error handling

## 🏗️ System Architecture

```
📁 monthlyforcast/
├── 🌐 app.py                 # Main Flask application
├── 🔧 data_processor.py      # CSV validation and preprocessing
├── 🤖 model_trainer.py       # ML model training and forecasting
├── 📋 requirements.txt       # Python dependencies
├── 🧪 test_system.py         # Comprehensive test suite
├── 🎯 demo.py               # Simple demo without ML dependencies
├── 📖 README.md             # This file
├── 📁 templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── forecast.html
│   └── results.html
├── 📁 uploads/              # Uploaded CSV files
└── 📁 static/               # CSS, JS, images
```

## 📋 CSV Format Requirements

Your CSV file must contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Month | Date in YYYY-MM-DD format | 2020-01-01 |
| Miscellaneous | Miscellaneous expenses | 10149.01 |
| Financial | Financial expenses | 11880.21 |
| CapEx | Capital expenditures | 15395.52 |
| COGS | Cost of goods sold | 21750.27 |
| Operating | Operating expenses | 18722.62 |
| Total | Total expenses | 77897.62 |

### ✅ Supported Features
- Various date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
- Missing values (automatically filled using interpolation)
- Different number formats ($1,234.56, 1234.56, etc.)
- Minimum 12 months of data required
- Automatic total recalculation if inconsistent

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd monthlyforcast
```

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Tests (Optional)
```bash
# Basic validation (no dependencies required)
python3 simple_test.py

# Full test suite (requires dependencies)
python3 test_system.py

# Demo with sample data
python3 demo.py
```

### 4. Start the Application
```bash
python3 app.py
```

### 5. Access the Web Interface
Open your browser and go to: `http://localhost:5000`

## 🎯 How to Use

### Step 1: Upload CSV Data
1. Navigate to the home page
2. Drag and drop your CSV file or click to browse
3. The system validates your data automatically

### Step 2: Configure Forecast
1. Review the data summary and any warnings
2. Choose the number of months to forecast (1-24)
3. Click "Generate AI Forecast"

### Step 3: View Results
1. Explore interactive charts showing historical vs. forecasted data
2. Review model performance metrics
3. Download forecast data as CSV
4. Print or share results

## 🤖 AI Models

The system uses two machine learning algorithms and automatically selects the best performer:

### Linear Regression
- **Best for**: Linear trends and stable patterns
- **Advantages**: Fast, interpretable, good baseline
- **Use case**: Consistent growth patterns

### Random Forest
- **Best for**: Complex patterns and seasonality
- **Advantages**: Handles non-linear relationships, robust to outliers
- **Use case**: Variable expense patterns

### Feature Engineering
- Time-based features (month, year, trend)
- Lag features (previous 1-3 months)
- Moving averages (3 and 6 months)
- Growth rate calculations

## 📊 Model Performance Metrics

- **R² Score**: Coefficient of determination (higher is better)
- **RMSE**: Root Mean Square Error (lower is better)
- **MAE**: Mean Absolute Error (lower is better)

## 🛠️ Technical Details

### Data Processing Pipeline
1. **Validation**: Check required columns and data types
2. **Cleaning**: Handle missing values and format inconsistencies
3. **Feature Engineering**: Create time-based and lag features
4. **Scaling**: Normalize features for ML algorithms
5. **Training**: Train multiple models and select best performer
6. **Forecasting**: Generate predictions with confidence intervals

### Error Handling
- Invalid CSV formats
- Missing or corrupted data
- Insufficient historical data
- Network and file upload errors
- Model training failures

## 🧪 Testing

The system includes comprehensive testing:

```bash
# Run all tests
python3 test_system.py

# Test specific components
python3 -m unittest test_system.TestDataProcessor
python3 -m unittest test_system.TestModelTrainer
```

## 📈 Sample Output

```
📈 6-Month Expense Forecast:
Month        Misc    Financial    CapEx     COGS    Operating    Total
2025-01     11,055    15,310     28,664    20,513    25,947     101,489
2025-02     11,053    15,308     28,646    20,512    25,936     101,455
2025-03     11,051    15,307     28,630    20,512    25,925     101,424
...

📊 Model Performance:
Linear Regression: R² = 0.9234, RMSE = $2,145
Random Forest: R² = 0.9456, RMSE = $1,876 ✅ Selected
```

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=development  # For development
export FLASK_DEBUG=1          # Enable debug mode
```

### Application Settings
- Maximum file size: 16MB
- Supported file types: CSV only
- Forecast range: 1-24 months
- Session timeout: 1 hour

## 🚨 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**CSV validation fails**
- Check column names match exactly
- Ensure dates are in YYYY-MM-DD format
- Verify numeric values don't contain text

**Poor forecast accuracy**
- Ensure at least 24 months of data
- Check for data quality issues
- Consider external factors affecting expenses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Flask, scikit-learn, and Plotly
- Bootstrap for responsive UI
- Font Awesome for icons
- Pandas for data processing

---

**Made with ❤️ for accurate expense forecasting**
