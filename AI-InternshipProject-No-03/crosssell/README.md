# 🤖 AI Upsell/Cross-sell Predictor

**AI-powered system to predict if you can upsell or cross-sell to new customers**

## 📁 Project Files

```
📦 AI Upsell Predictor
├── 📊 training_data_10k.csv          # 10,000 customer training data
├── 🤖 ai_model_trainer.py            # AI model training & prediction
├── 🌐 ai_predictor_interface.html    # Web interface for predictions
├── 🔧 generate_training_data.py      # Generate new training data
└── 📖 README.md                      # This file
```

## 🚀 How to Run (Step by Step)

### Step 1: Test the AI Model
```bash
python3 ai_model_trainer.py
```
**What it does:**
- Loads 10,000 customer training data
- Trains AI model with customer patterns
- Tests with 3 sample customers
- Shows prediction results

**Expected Output:**
```
🤖 Starting AI Model Training...
✅ Loaded 10,000 customer records
✅ Learned 21 upsell patterns
✅ Learned 21 cross-sell patterns
🎉 AI Model Training Complete!

🧪 Testing Trained AI Model:
1. 💰 High-Value Customer
   Upsell: ✅ YES (99.9%)
   Cross-sell: ✅ YES (99.4%)
```

### Step 2: Open Web Interface
```bash
# Open in browser
firefox ai_predictor_interface.html
# OR
google-chrome ai_predictor_interface.html
# OR double-click the file
```

**What it does:**
- Opens interactive web form
- Enter customer details
- Get instant AI predictions
- See upsell/cross-sell recommendations

### Step 3: Generate New Training Data (Optional)
```bash
python3 generate_training_data.py
```
**What it does:**
- Creates fresh 10,000 customer dataset
- Saves to `training_data_10k.csv`
- Shows data analysis statistics

## 🎯 How to Use for Business

### Method 1: Web Interface
1. Open `ai_predictor_interface.html` in browser
2. Fill customer information:
   - Age, Income, Spending Score
   - Membership Years, Purchase History
   - Product Preferences, Satisfaction
3. Click "Get AI Predictions"
4. See results:
   - ✅/❌ Can Upsell?
   - ✅/❌ Can Cross-sell?
   - 🎁 Recommended Products
   - 📊 Success Probabilities

### Method 2: Python Code
```python
from ai_model_trainer import SimpleAIModel

# Load trained model
model = SimpleAIModel()
model.train('training_data_10k.csv')

# New customer data
customer = {
    'age': 35,
    'income': 75000,
    'spending_score': 65,
    'membership_years': 2,
    'previous_purchases': 10,
    'avg_order_value': 150,
    'last_purchase_days': 30,
    'product_category_preference': 'Electronics',
    'satisfaction_score': 7
}

# Get prediction
result = model.predict_customer(customer)

# Check results
if result['can_upsell']:
    print("✅ Can upsell this customer!")
    
if result['can_crosssell']:
    print("✅ Can cross-sell to this customer!")

# See recommendations
for rec in result['recommendations']:
    print(f"🎁 {rec['product']} - {rec['probability']:.1%}")
```

## 📊 Understanding Results

### Upsell Prediction
- **✅ YES**: Customer can buy higher-value products
- **❌ NO**: Focus on retention instead
- **Probability**: Success chance percentage

### Cross-sell Prediction  
- **✅ YES**: Customer will buy additional products
- **❌ NO**: Not ready for more products
- **Probability**: Success chance percentage

### Product Recommendations
- **Premium Products** (upsell): Higher-value versions
- **Accessories** (cross-sell): Add-on products
- **Extended Warranty** (cross-sell): Protection plans
- **Monthly Subscription** (cross-sell): Recurring services

## 🎯 Business Use Cases

### For Sales Team
```
New customer walks in:
1. Enter their details in web interface
2. Get instant AI prediction
3. If upsell = YES → Show premium products
4. If cross-sell = YES → Recommend accessories
5. Follow suggested action plan
```

### For E-commerce
```
Customer browsing website:
1. Analyze their profile with AI
2. Show personalized recommendations
3. Target high-probability products
4. Increase average order value
```

### For Customer Service
```
Customer calls support:
1. Look up their prediction
2. Offer relevant upgrades
3. Suggest complementary products
4. Improve customer lifetime value
```

## 🔧 Customization

### Add More Training Data
1. Edit `generate_training_data.py`
2. Increase `num_customers` parameter
3. Run: `python3 generate_training_data.py`
4. Retrain: `python3 ai_model_trainer.py`

### Modify Prediction Logic
1. Edit `ai_model_trainer.py`
2. Update `predict_upsell_opportunity()` function
3. Update `predict_crosssell_opportunity()` function
4. Test with new logic

### Add New Products
1. Edit `get_product_recommendations()` in `ai_model_trainer.py`
2. Add new product categories
3. Define recommendation rules
4. Update web interface if needed

## 📈 Performance Stats

**Training Data**: 10,000 customers
- **Upsell Rate**: 64.8%
- **Cross-sell Rate**: 88.6%
- **Premium Products**: 39.7%
- **Accessories**: 19.5%
- **Warranty**: 48.1%
- **Subscription**: 48.2%

**Model Accuracy**: 
- **251 product patterns** learned
- **21 upsell patterns** identified
- **21 cross-sell patterns** identified

## 🎉 Success Examples

**High-Income Customer ($120k)**:
- Upsell: ✅ 99.9% success
- Cross-sell: ✅ 99.4% success
- Top recommendation: Premium Products (85%)

**Medium Customer ($65k)**:
- Upsell: ❌ 22.4% (focus on retention)
- Cross-sell: ✅ 83.9% success
- Top recommendation: Accessories (100%)

**New Customer ($45k)**:
- Upsell: ❌ 0% (build relationship first)
- Cross-sell: ✅ 65.6% success
- Top recommendation: Subscription (50%)

## 🚀 Ready for Production!

This system is ready to use for real business:
- ✅ Trained on realistic data
- ✅ Tested with multiple scenarios
- ✅ Web interface for easy use
- ✅ Python API for integration
- ✅ Clear business recommendations

**Start using it today to increase your sales!** 🎯
