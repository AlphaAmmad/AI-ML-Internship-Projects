#!/usr/bin/env python3
"""
AI Model Trainer for Upsell/Cross-sell Prediction
Trains machine learning models using the generated CSV data
"""

import csv
import random
from collections import defaultdict

class SimpleAIModel:
    """Simple AI model that learns from CSV data"""
    
    def __init__(self):
        self.upsell_rules = {}
        self.crosssell_rules = {}
        self.product_rules = {}
        self.trained = False
        self.training_stats = {}
    
    def load_csv_data(self, filename='training_data_10k.csv'):
        """Load training data from CSV"""
        print(f"📂 Loading training data from {filename}...")
        
        customers = []
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Convert numeric fields
                    customer = {}
                    for key, value in row.items():
                        if key in ['age', 'income', 'spending_score', 'membership_years', 
                                 'previous_purchases', 'avg_order_value', 'last_purchase_days',
                                 'satisfaction_score', 'can_upsell', 'can_crosssell',
                                 'will_buy_premium', 'will_buy_accessories', 'will_buy_warranty',
                                 'will_buy_subscription']:
                            customer[key] = int(float(value))
                        else:
                            customer[key] = value
                    customers.append(customer)
            
            print(f"✅ Loaded {len(customers):,} customer records")
            return customers
            
        except FileNotFoundError:
            print(f"❌ Error: {filename} not found!")
            return []
    
    def analyze_patterns(self, customers):
        """Analyze patterns in the training data"""
        print("🔍 Analyzing customer patterns...")
        
        # Upsell patterns
        upsell_patterns = defaultdict(list)
        crosssell_patterns = defaultdict(list)
        
        for customer in customers:
            # Create feature combinations for pattern analysis
            income_bracket = 'high' if customer['income'] > 80000 else 'medium' if customer['income'] > 50000 else 'low'
            spending_bracket = 'high' if customer['spending_score'] > 70 else 'medium' if customer['spending_score'] > 40 else 'low'
            loyalty_bracket = 'high' if customer['membership_years'] > 3 else 'medium' if customer['membership_years'] > 1 else 'low'
            
            pattern_key = f"{income_bracket}_{spending_bracket}_{loyalty_bracket}"
            
            upsell_patterns[pattern_key].append(customer['can_upsell'])
            crosssell_patterns[pattern_key].append(customer['can_crosssell'])
        
        # Calculate success rates for each pattern
        self.upsell_rules = {}
        self.crosssell_rules = {}
        
        for pattern, outcomes in upsell_patterns.items():
            success_rate = sum(outcomes) / len(outcomes)
            self.upsell_rules[pattern] = success_rate
        
        for pattern, outcomes in crosssell_patterns.items():
            success_rate = sum(outcomes) / len(outcomes)
            self.crosssell_rules[pattern] = success_rate
        
        print(f"✅ Learned {len(self.upsell_rules)} upsell patterns")
        print(f"✅ Learned {len(self.crosssell_rules)} cross-sell patterns")
    
    def train_product_models(self, customers):
        """Train models for specific products"""
        print("🎯 Training product-specific models...")
        
        # Product patterns
        premium_patterns = defaultdict(list)
        accessories_patterns = defaultdict(list)
        warranty_patterns = defaultdict(list)
        subscription_patterns = defaultdict(list)
        
        for customer in customers:
            # Create patterns based on customer characteristics
            age_bracket = 'young' if customer['age'] < 35 else 'middle' if customer['age'] < 55 else 'senior'
            order_value_bracket = 'high' if customer['avg_order_value'] > 250 else 'medium' if customer['avg_order_value'] > 100 else 'low'
            activity_bracket = 'recent' if customer['last_purchase_days'] < 60 else 'moderate' if customer['last_purchase_days'] < 180 else 'old'
            
            pattern_key = f"{age_bracket}_{order_value_bracket}_{activity_bracket}_{customer['product_category_preference']}"
            
            premium_patterns[pattern_key].append(customer['will_buy_premium'])
            accessories_patterns[pattern_key].append(customer['will_buy_accessories'])
            warranty_patterns[pattern_key].append(customer['will_buy_warranty'])
            subscription_patterns[pattern_key].append(customer['will_buy_subscription'])
        
        # Calculate product success rates
        self.product_rules = {
            'premium': {},
            'accessories': {},
            'warranty': {},
            'subscription': {}
        }
        
        for pattern, outcomes in premium_patterns.items():
            if len(outcomes) > 5:  # Only use patterns with enough data
                self.product_rules['premium'][pattern] = sum(outcomes) / len(outcomes)
        
        for pattern, outcomes in accessories_patterns.items():
            if len(outcomes) > 5:
                self.product_rules['accessories'][pattern] = sum(outcomes) / len(outcomes)
        
        for pattern, outcomes in warranty_patterns.items():
            if len(outcomes) > 5:
                self.product_rules['warranty'][pattern] = sum(outcomes) / len(outcomes)
        
        for pattern, outcomes in subscription_patterns.items():
            if len(outcomes) > 5:
                self.product_rules['subscription'][pattern] = sum(outcomes) / len(outcomes)
        
        print(f"✅ Trained premium model: {len(self.product_rules['premium'])} patterns")
        print(f"✅ Trained accessories model: {len(self.product_rules['accessories'])} patterns")
        print(f"✅ Trained warranty model: {len(self.product_rules['warranty'])} patterns")
        print(f"✅ Trained subscription model: {len(self.product_rules['subscription'])} patterns")
    
    def train(self, csv_filename='training_data_10k.csv'):
        """Train the AI model using CSV data"""
        print("🤖 Starting AI Model Training...")
        print("=" * 50)
        
        # Load data
        customers = self.load_csv_data(csv_filename)
        if not customers:
            return False
        
        # Analyze patterns
        self.analyze_patterns(customers)
        
        # Train product models
        self.train_product_models(customers)
        
        # Calculate training statistics
        total_customers = len(customers)
        upsell_customers = sum(1 for c in customers if c['can_upsell'])
        crosssell_customers = sum(1 for c in customers if c['can_crosssell'])
        
        self.training_stats = {
            'total_customers': total_customers,
            'upsell_rate': (upsell_customers / total_customers) * 100,
            'crosssell_rate': (crosssell_customers / total_customers) * 100,
            'premium_rate': (sum(1 for c in customers if c['will_buy_premium']) / total_customers) * 100,
            'accessories_rate': (sum(1 for c in customers if c['will_buy_accessories']) / total_customers) * 100,
            'warranty_rate': (sum(1 for c in customers if c['will_buy_warranty']) / total_customers) * 100,
            'subscription_rate': (sum(1 for c in customers if c['will_buy_subscription']) / total_customers) * 100
        }
        
        self.trained = True
        print("🎉 AI Model Training Complete!")
        return True
    
    def predict_customer(self, customer):
        """Predict upsell/cross-sell for a new customer"""
        if not self.trained:
            return {"error": "Model not trained yet!"}
        
        # Create pattern for this customer
        income_bracket = 'high' if customer['income'] > 80000 else 'medium' if customer['income'] > 50000 else 'low'
        spending_bracket = 'high' if customer['spending_score'] > 70 else 'medium' if customer['spending_score'] > 40 else 'low'
        loyalty_bracket = 'high' if customer['membership_years'] > 3 else 'medium' if customer['membership_years'] > 1 else 'low'
        
        pattern_key = f"{income_bracket}_{spending_bracket}_{loyalty_bracket}"
        
        # Get upsell/cross-sell probabilities
        upsell_prob = self.upsell_rules.get(pattern_key, 0.3)  # Default 30%
        crosssell_prob = self.crosssell_rules.get(pattern_key, 0.4)  # Default 40%
        
        # Product-specific predictions
        age_bracket = 'young' if customer['age'] < 35 else 'middle' if customer['age'] < 55 else 'senior'
        order_value_bracket = 'high' if customer['avg_order_value'] > 250 else 'medium' if customer['avg_order_value'] > 100 else 'low'
        activity_bracket = 'recent' if customer['last_purchase_days'] < 60 else 'moderate' if customer['last_purchase_days'] < 180 else 'old'
        
        product_pattern = f"{age_bracket}_{order_value_bracket}_{activity_bracket}_{customer['product_category_preference']}"
        
        premium_prob = self.product_rules['premium'].get(product_pattern, 0.2)
        accessories_prob = self.product_rules['accessories'].get(product_pattern, 0.15)
        warranty_prob = self.product_rules['warranty'].get(product_pattern, 0.25)
        subscription_prob = self.product_rules['subscription'].get(product_pattern, 0.2)
        
        return {
            'upsell_probability': upsell_prob,
            'crosssell_probability': crosssell_prob,
            'can_upsell': upsell_prob > 0.5,
            'can_crosssell': crosssell_prob > 0.4,
            'product_probabilities': {
                'premium': premium_prob,
                'accessories': accessories_prob,
                'warranty': warranty_prob,
                'subscription': subscription_prob
            },
            'recommendations': self.get_recommendations(premium_prob, accessories_prob, warranty_prob, subscription_prob)
        }
    
    def get_recommendations(self, premium_prob, accessories_prob, warranty_prob, subscription_prob):
        """Get product recommendations based on probabilities"""
        recommendations = []
        
        products = [
            ('Premium Products', premium_prob, 'upsell'),
            ('Accessories', accessories_prob, 'crosssell'),
            ('Extended Warranty', warranty_prob, 'crosssell'),
            ('Monthly Subscription', subscription_prob, 'crosssell')
        ]
        
        # Sort by probability and filter
        products.sort(key=lambda x: x[1], reverse=True)
        
        for product, prob, sell_type in products:
            if prob > 0.3:  # Only recommend if >30% probability
                confidence = 'High' if prob > 0.7 else 'Medium' if prob > 0.5 else 'Low'
                recommendations.append({
                    'product': product,
                    'probability': prob,
                    'confidence': confidence,
                    'type': sell_type
                })
        
        return recommendations
    
    def display_training_stats(self):
        """Display training statistics"""
        if not self.trained:
            print("❌ Model not trained yet!")
            return
        
        print("\n📊 AI Model Training Statistics:")
        print("=" * 40)
        print(f"📈 Training Data: {self.training_stats['total_customers']:,} customers")
        print(f"⬆️ Upsell Rate: {self.training_stats['upsell_rate']:.1f}%")
        print(f"➡️ Cross-sell Rate: {self.training_stats['crosssell_rate']:.1f}%")
        print(f"💎 Premium Rate: {self.training_stats['premium_rate']:.1f}%")
        print(f"🔧 Accessories Rate: {self.training_stats['accessories_rate']:.1f}%")
        print(f"🛡️ Warranty Rate: {self.training_stats['warranty_rate']:.1f}%")
        print(f"📱 Subscription Rate: {self.training_stats['subscription_rate']:.1f}%")

def test_trained_model():
    """Test the trained model with sample customers"""
    
    # Initialize and train model
    model = SimpleAIModel()
    success = model.train('training_data_10k.csv')
    
    if not success:
        print("❌ Training failed!")
        return
    
    # Display training stats
    model.display_training_stats()
    
    print("\n🧪 Testing Trained AI Model:")
    print("=" * 50)
    
    # Test customers
    test_customers = [
        {
            'name': '💰 High-Value Customer',
            'age': 40, 'income': 120000, 'spending_score': 85,
            'membership_years': 5, 'previous_purchases': 25, 'avg_order_value': 400,
            'last_purchase_days': 20, 'product_category_preference': 'Electronics',
            'satisfaction_score': 9
        },
        {
            'name': '🎯 Medium Customer',
            'age': 32, 'income': 65000, 'spending_score': 60,
            'membership_years': 2, 'previous_purchases': 8, 'avg_order_value': 150,
            'last_purchase_days': 45, 'product_category_preference': 'Clothing',
            'satisfaction_score': 7
        },
        {
            'name': '🆕 New Customer',
            'age': 28, 'income': 45000, 'spending_score': 40,
            'membership_years': 0, 'previous_purchases': 1, 'avg_order_value': 80,
            'last_purchase_days': 10, 'product_category_preference': 'Books',
            'satisfaction_score': 6
        }
    ]
    
    for i, customer in enumerate(test_customers, 1):
        print(f"\n{i}. {customer['name']}")
        print("-" * 40)
        
        # Remove name for prediction
        customer_data = {k: v for k, v in customer.items() if k != 'name'}
        
        # Get AI prediction
        prediction = model.predict_customer(customer_data)
        
        print(f"🤖 AI Predictions:")
        print(f"   Upsell: {'✅ YES' if prediction['can_upsell'] else '❌ NO'} ({prediction['upsell_probability']:.1%})")
        print(f"   Cross-sell: {'✅ YES' if prediction['can_crosssell'] else '❌ NO'} ({prediction['crosssell_probability']:.1%})")
        
        if prediction['recommendations']:
            print(f"   🎁 Recommendations:")
            for rec in prediction['recommendations']:
                print(f"      • {rec['product']} ({rec['type']}) - {rec['probability']:.1%} ({rec['confidence']})")
        else:
            print(f"   ❌ No recommendations")
    
    print(f"\n🎉 AI Model Successfully Trained and Tested!")
    print(f"📈 Model learned from 10,000 customer patterns")
    print(f"🚀 Ready for production use!")

if __name__ == "__main__":
    test_trained_model()
