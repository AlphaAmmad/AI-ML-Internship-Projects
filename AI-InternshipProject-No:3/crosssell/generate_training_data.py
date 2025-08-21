#!/usr/bin/env python3
"""
Generate 10,000 customer training data for upsell/cross-sell prediction
Creates realistic customer data with proper target labels
"""

import random
import csv

def generate_customer_data():
    """Generate realistic customer data"""
    
    # Customer demographics
    age = random.randint(18, 70)
    gender = random.choice(['Male', 'Female'])
    
    # Income based on age (older people generally earn more)
    if age < 25:
        income = random.randint(25000, 60000)
    elif age < 35:
        income = random.randint(35000, 90000)
    elif age < 50:
        income = random.randint(45000, 150000)
    else:
        income = random.randint(40000, 120000)
    
    # Spending score correlated with income
    if income > 100000:
        spending_score = random.randint(60, 100)
    elif income > 70000:
        spending_score = random.randint(50, 90)
    elif income > 50000:
        spending_score = random.randint(40, 80)
    else:
        spending_score = random.randint(20, 70)
    
    # Membership and purchase history
    membership_years = random.randint(0, 15)
    
    # Previous purchases based on membership and spending
    if membership_years > 5 and spending_score > 70:
        previous_purchases = random.randint(20, 80)
    elif membership_years > 2 and spending_score > 50:
        previous_purchases = random.randint(10, 40)
    elif membership_years > 0:
        previous_purchases = random.randint(1, 20)
    else:
        previous_purchases = random.randint(0, 5)
    
    # Average order value based on income and spending
    if income > 80000 and spending_score > 70:
        avg_order_value = random.randint(200, 800)
    elif income > 50000 and spending_score > 50:
        avg_order_value = random.randint(100, 400)
    else:
        avg_order_value = random.randint(30, 200)
    
    # Last purchase days
    if previous_purchases > 10:
        last_purchase_days = random.randint(1, 180)
    elif previous_purchases > 0:
        last_purchase_days = random.randint(1, 365)
    else:
        last_purchase_days = random.randint(180, 730)  # New customers
    
    # Product preferences
    product_category_preference = random.choice([
        'Electronics', 'Clothing', 'Books', 'Home', 'Sports', 
        'Beauty', 'Automotive', 'Health', 'Toys', 'Garden'
    ])
    
    # Communication channel based on age
    if age < 30:
        communication_channel = random.choice(['App', 'SMS', 'Email'])
    elif age < 50:
        communication_channel = random.choice(['Email', 'App', 'Phone'])
    else:
        communication_channel = random.choice(['Phone', 'Email', 'SMS'])
    
    # Satisfaction score based on previous experience
    if previous_purchases > 15 and membership_years > 3:
        satisfaction_score = random.randint(7, 10)
    elif previous_purchases > 5:
        satisfaction_score = random.randint(5, 9)
    else:
        satisfaction_score = random.randint(3, 8)
    
    return {
        'customer_id': None,  # Will be set later
        'age': age,
        'gender': gender,
        'income': income,
        'spending_score': spending_score,
        'membership_years': membership_years,
        'previous_purchases': previous_purchases,
        'avg_order_value': avg_order_value,
        'last_purchase_days': last_purchase_days,
        'product_category_preference': product_category_preference,
        'communication_channel': communication_channel,
        'satisfaction_score': satisfaction_score
    }

def calculate_upsell_target(customer):
    """Calculate if customer can be upsold (target variable)"""
    score = 0
    
    # High income customers
    if customer['income'] > 100000:
        score += 0.4
    elif customer['income'] > 70000:
        score += 0.25
    elif customer['income'] > 50000:
        score += 0.15
    
    # High spending score
    if customer['spending_score'] > 80:
        score += 0.3
    elif customer['spending_score'] > 60:
        score += 0.2
    
    # Loyal customers
    if customer['membership_years'] > 5:
        score += 0.2
    elif customer['membership_years'] > 2:
        score += 0.1
    
    # High satisfaction
    if customer['satisfaction_score'] > 8:
        score += 0.15
    elif customer['satisfaction_score'] > 6:
        score += 0.1
    
    # Recent activity
    if customer['last_purchase_days'] < 30:
        score += 0.1
    elif customer['last_purchase_days'] < 90:
        score += 0.05
    
    # Add some randomness for realistic data
    score += random.uniform(-0.1, 0.1)
    
    return 1 if score > 0.5 else 0

def calculate_crosssell_target(customer):
    """Calculate if customer can be cross-sold (target variable)"""
    score = 0
    
    # Purchase history
    if customer['previous_purchases'] > 15:
        score += 0.35
    elif customer['previous_purchases'] > 5:
        score += 0.25
    elif customer['previous_purchases'] > 0:
        score += 0.15
    
    # Recent activity
    if customer['last_purchase_days'] < 60:
        score += 0.25
    elif customer['last_purchase_days'] < 120:
        score += 0.15
    
    # Satisfaction
    if customer['satisfaction_score'] > 7:
        score += 0.2
    elif customer['satisfaction_score'] > 5:
        score += 0.1
    
    # Category preferences (some categories have more cross-sell opportunities)
    if customer['product_category_preference'] in ['Electronics', 'Clothing', 'Home']:
        score += 0.15
    elif customer['product_category_preference'] in ['Beauty', 'Sports']:
        score += 0.1
    
    # Communication channel (app users are more responsive)
    if customer['communication_channel'] == 'App':
        score += 0.1
    elif customer['communication_channel'] == 'Email':
        score += 0.05
    
    # Add randomness
    score += random.uniform(-0.1, 0.1)
    
    return 1 if score > 0.4 else 0

def generate_training_dataset(num_customers=10000):
    """Generate complete training dataset"""
    
    print(f"🚀 Generating {num_customers:,} customer records for training...")
    
    customers = []
    
    for i in range(num_customers):
        if (i + 1) % 1000 == 0:
            print(f"   Generated {i + 1:,} customers...")
        
        # Generate customer data
        customer = generate_customer_data()
        customer['customer_id'] = f"CUST_{i+1:06d}"
        
        # Calculate target variables
        customer['can_upsell'] = calculate_upsell_target(customer)
        customer['can_crosssell'] = calculate_crosssell_target(customer)
        
        # Calculate specific product probabilities
        customer['will_buy_premium'] = 1 if (customer['can_upsell'] and customer['income'] > 80000) else 0
        customer['will_buy_accessories'] = 1 if (customer['can_crosssell'] and customer['product_category_preference'] in ['Electronics', 'Clothing']) else 0
        customer['will_buy_warranty'] = 1 if (customer['avg_order_value'] > 200 and customer['satisfaction_score'] > 6) else 0
        customer['will_buy_subscription'] = 1 if (customer['can_crosssell'] and customer['communication_channel'] in ['App', 'Email']) else 0
        
        customers.append(customer)
    
    return customers

def save_to_csv(customers, filename='training_data_10k.csv'):
    """Save customer data to CSV file"""
    
    print(f"💾 Saving data to {filename}...")
    
    # Define column order
    columns = [
        'customer_id', 'age', 'gender', 'income', 'spending_score',
        'membership_years', 'previous_purchases', 'avg_order_value',
        'last_purchase_days', 'product_category_preference',
        'communication_channel', 'satisfaction_score',
        'can_upsell', 'can_crosssell', 'will_buy_premium',
        'will_buy_accessories', 'will_buy_warranty', 'will_buy_subscription'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(customers)
    
    print(f"✅ Successfully saved {len(customers):,} customer records!")
    return filename

def analyze_dataset(customers):
    """Analyze the generated dataset"""
    
    print(f"\n📊 Dataset Analysis:")
    print(f"   Total Customers: {len(customers):,}")
    
    # Upsell analysis
    upsell_count = sum(1 for c in customers if c['can_upsell'])
    upsell_percentage = (upsell_count / len(customers)) * 100
    print(f"   Can Upsell: {upsell_count:,} ({upsell_percentage:.1f}%)")
    
    # Cross-sell analysis
    crosssell_count = sum(1 for c in customers if c['can_crosssell'])
    crosssell_percentage = (crosssell_count / len(customers)) * 100
    print(f"   Can Cross-sell: {crosssell_count:,} ({crosssell_percentage:.1f}%)")
    
    # Product analysis
    premium_count = sum(1 for c in customers if c['will_buy_premium'])
    accessories_count = sum(1 for c in customers if c['will_buy_accessories'])
    warranty_count = sum(1 for c in customers if c['will_buy_warranty'])
    subscription_count = sum(1 for c in customers if c['will_buy_subscription'])
    
    print(f"   Will Buy Premium: {premium_count:,} ({(premium_count/len(customers)*100):.1f}%)")
    print(f"   Will Buy Accessories: {accessories_count:,} ({(accessories_count/len(customers)*100):.1f}%)")
    print(f"   Will Buy Warranty: {warranty_count:,} ({(warranty_count/len(customers)*100):.1f}%)")
    print(f"   Will Buy Subscription: {subscription_count:,} ({(subscription_count/len(customers)*100):.1f}%)")
    
    # Income distribution
    high_income = sum(1 for c in customers if c['income'] > 100000)
    medium_income = sum(1 for c in customers if 50000 <= c['income'] <= 100000)
    low_income = sum(1 for c in customers if c['income'] < 50000)
    
    print(f"\n💰 Income Distribution:")
    print(f"   High Income (>$100k): {high_income:,} ({(high_income/len(customers)*100):.1f}%)")
    print(f"   Medium Income ($50k-$100k): {medium_income:,} ({(medium_income/len(customers)*100):.1f}%)")
    print(f"   Low Income (<$50k): {low_income:,} ({(low_income/len(customers)*100):.1f}%)")

def main():
    """Main function to generate training data"""
    
    print("🤖 AI Training Data Generator")
    print("=" * 50)
    print("📈 Creating realistic customer data for upsell/cross-sell prediction")
    
    # Set random seed for reproducible results
    random.seed(42)
    
    # Generate dataset
    customers = generate_training_dataset(10000)
    
    # Analyze dataset
    analyze_dataset(customers)
    
    # Save to CSV
    filename = save_to_csv(customers)
    
    print(f"\n🎉 Training data ready!")
    print(f"📁 File: {filename}")
    print(f"🚀 Use this CSV to train your AI model!")
    
    return filename

if __name__ == "__main__":
    main()
