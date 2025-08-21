#!/usr/bin/env python3
"""
AI Upsell/Cross-sell Predictor for New Customers
Predicts if you can upsell or cross-sell to a new customer
"""

def analyze_customer_for_upsell_crosssell(customer):
    """
    Main function to predict upsell and cross-sell opportunities
    Returns: upsell_possible, crosssell_possible, recommended_products
    """
    
    # Calculate customer value score
    value_score = calculate_customer_value(customer)
    
    # Predict upsell possibility
    upsell_possible, upsell_confidence = predict_upsell_opportunity(customer, value_score)
    
    # Predict cross-sell possibility  
    crosssell_possible, crosssell_confidence = predict_crosssell_opportunity(customer, value_score)
    
    # Get specific product recommendations
    recommended_products = get_product_recommendations(customer, value_score)
    
    return {
        'customer_profile': customer,
        'customer_value_score': value_score,
        'upsell': {
            'possible': upsell_possible,
            'confidence': upsell_confidence,
            'reason': get_upsell_reason(customer, value_score)
        },
        'crosssell': {
            'possible': crosssell_possible,
            'confidence': crosssell_confidence,
            'reason': get_crosssell_reason(customer, value_score)
        },
        'recommended_products': recommended_products,
        'action_plan': generate_action_plan(upsell_possible, crosssell_possible, recommended_products)
    }

def calculate_customer_value(customer):
    """Calculate overall customer value score (0-100)"""
    score = 0
    
    # Income factor (30% weight)
    if customer['income'] > 100000:
        score += 30
    elif customer['income'] > 70000:
        score += 20
    elif customer['income'] > 50000:
        score += 15
    elif customer['income'] > 30000:
        score += 10
    
    # Spending behavior (25% weight)
    if customer['spending_score'] > 80:
        score += 25
    elif customer['spending_score'] > 60:
        score += 20
    elif customer['spending_score'] > 40:
        score += 15
    elif customer['spending_score'] > 20:
        score += 10
    
    # Purchase history (20% weight)
    if customer['previous_purchases'] > 20:
        score += 20
    elif customer['previous_purchases'] > 10:
        score += 15
    elif customer['previous_purchases'] > 5:
        score += 10
    elif customer['previous_purchases'] > 0:
        score += 5
    
    # Order value (15% weight)
    if customer['avg_order_value'] > 300:
        score += 15
    elif customer['avg_order_value'] > 200:
        score += 12
    elif customer['avg_order_value'] > 100:
        score += 8
    elif customer['avg_order_value'] > 50:
        score += 5
    
    # Loyalty and satisfaction (10% weight)
    if customer['membership_years'] > 3 and customer['satisfaction_score'] > 8:
        score += 10
    elif customer['membership_years'] > 1 and customer['satisfaction_score'] > 6:
        score += 7
    elif customer['satisfaction_score'] > 5:
        score += 3
    
    return min(score, 100)

def predict_upsell_opportunity(customer, value_score):
    """Predict if customer can be upsold to higher value products"""
    
    upsell_score = 0
    
    # High value customers are good upsell targets
    if value_score > 70:
        upsell_score += 40
    elif value_score > 50:
        upsell_score += 25
    elif value_score > 30:
        upsell_score += 15
    
    # Recent activity indicates engagement
    if customer['last_purchase_days'] < 30:
        upsell_score += 20
    elif customer['last_purchase_days'] < 90:
        upsell_score += 10
    
    # High satisfaction means trust in brand
    if customer['satisfaction_score'] > 8:
        upsell_score += 15
    elif customer['satisfaction_score'] > 6:
        upsell_score += 10
    
    # Premium categories are easier to upsell
    if customer['product_category_preference'] in ['Electronics', 'Home']:
        upsell_score += 15
    
    # App/Email users are more responsive
    if customer['communication_channel'] in ['App', 'Email']:
        upsell_score += 10
    
    upsell_possible = upsell_score > 50
    confidence = 'High' if upsell_score > 70 else 'Medium' if upsell_score > 50 else 'Low'
    
    return upsell_possible, confidence

def predict_crosssell_opportunity(customer, value_score):
    """Predict if customer can be cross-sold additional products"""
    
    crosssell_score = 0
    
    # Customers with purchase history buy more
    if customer['previous_purchases'] > 15:
        crosssell_score += 30
    elif customer['previous_purchases'] > 5:
        crosssell_score += 20
    elif customer['previous_purchases'] > 0:
        crosssell_score += 10
    
    # Recent buyers are active
    if customer['last_purchase_days'] < 60:
        crosssell_score += 25
    elif customer['last_purchase_days'] < 120:
        crosssell_score += 15
    
    # Satisfied customers trust recommendations
    if customer['satisfaction_score'] > 7:
        crosssell_score += 20
    elif customer['satisfaction_score'] > 5:
        crosssell_score += 10
    
    # Certain categories have more cross-sell opportunities
    if customer['product_category_preference'] in ['Electronics', 'Clothing']:
        crosssell_score += 15
    
    # Younger customers are more open to new products
    if customer['age'] < 40:
        crosssell_score += 10
    
    crosssell_possible = crosssell_score > 40
    confidence = 'High' if crosssell_score > 70 else 'Medium' if crosssell_score > 40 else 'Low'
    
    return crosssell_possible, confidence

def get_product_recommendations(customer, value_score):
    """Get specific product recommendations based on customer profile"""
    
    recommendations = []
    
    # Premium products for high-value customers
    if value_score > 60 and customer['income'] > 70000:
        recommendations.append({
            'type': 'upsell',
            'product': 'Premium Version',
            'reason': 'High income and value score',
            'probability': 85
        })
    
    # Accessories for electronics customers
    if customer['product_category_preference'] == 'Electronics':
        recommendations.append({
            'type': 'crosssell',
            'product': 'Accessories & Add-ons',
            'reason': 'Electronics customers often need accessories',
            'probability': 75
        })
    
    # Warranty for high-value orders
    if customer['avg_order_value'] > 200:
        recommendations.append({
            'type': 'crosssell',
            'product': 'Extended Warranty',
            'reason': 'High order value indicates investment protection need',
            'probability': 70
        })
    
    # Subscription for active users
    if customer['last_purchase_days'] < 60 and customer['communication_channel'] == 'App':
        recommendations.append({
            'type': 'crosssell',
            'product': 'Monthly Subscription',
            'reason': 'Active app users benefit from subscriptions',
            'probability': 65
        })
    
    # Clothing accessories
    if customer['product_category_preference'] == 'Clothing':
        recommendations.append({
            'type': 'crosssell',
            'product': 'Fashion Accessories',
            'reason': 'Clothing customers often buy matching accessories',
            'probability': 60
        })
    
    return recommendations

def get_upsell_reason(customer, value_score):
    """Get reason why upsell is possible or not"""
    if value_score > 70:
        return f"High-value customer (score: {value_score}) with strong purchasing power"
    elif value_score > 50:
        return f"Medium-value customer (score: {value_score}) with upsell potential"
    else:
        return f"Low-value customer (score: {value_score}) - focus on retention first"

def get_crosssell_reason(customer, value_score):
    """Get reason why cross-sell is possible or not"""
    if customer['previous_purchases'] > 10:
        return f"Active buyer with {customer['previous_purchases']} previous purchases"
    elif customer['last_purchase_days'] < 60:
        return f"Recent activity ({customer['last_purchase_days']} days ago) indicates engagement"
    else:
        return f"Limited purchase history - need to build relationship first"

def generate_action_plan(upsell_possible, crosssell_possible, recommendations):
    """Generate actionable plan for sales team"""
    
    plan = []
    
    if upsell_possible and crosssell_possible:
        plan.append("🎯 PRIORITY: Both upsell and cross-sell opportunities available")
        plan.append("📈 Strategy: Start with cross-sell to build trust, then upsell")
    elif upsell_possible:
        plan.append("⬆️ FOCUS: Upsell opportunity identified")
        plan.append("💎 Strategy: Present premium options with clear value proposition")
    elif crosssell_possible:
        plan.append("➡️ FOCUS: Cross-sell opportunity identified") 
        plan.append("🛒 Strategy: Recommend complementary products")
    else:
        plan.append("⚠️ CAUTION: Low upsell/cross-sell potential")
        plan.append("🤝 Strategy: Focus on relationship building and satisfaction")
    
    if recommendations:
        plan.append(f"🎁 TOP RECOMMENDATION: {recommendations[0]['product']}")
        plan.append(f"📊 Success Probability: {recommendations[0]['probability']}%")
    
    return plan

def test_new_customers():
    """Test the system with new customer profiles"""
    
    print("🚀 AI Upsell/Cross-sell Predictor for New Customers")
    print("=" * 60)
    print("🎯 Predicts if you can upsell or cross-sell to new customers")
    
    # Test customers
    test_customers = [
        {
            'name': '💰 High-Income New Customer',
            'age': 35, 'gender': 'Male', 'income': 120000, 'spending_score': 80,
            'membership_years': 1, 'previous_purchases': 3, 'avg_order_value': 350,
            'last_purchase_days': 15, 'product_category_preference': 'Electronics',
            'communication_channel': 'App', 'satisfaction_score': 8
        },
        {
            'name': '🛒 Active Shopper',
            'age': 28, 'gender': 'Female', 'income': 65000, 'spending_score': 75,
            'membership_years': 2, 'previous_purchases': 12, 'avg_order_value': 180,
            'last_purchase_days': 25, 'product_category_preference': 'Clothing',
            'communication_channel': 'Email', 'satisfaction_score': 9
        },
        {
            'name': '🆕 Brand New Customer',
            'age': 42, 'gender': 'Male', 'income': 55000, 'spending_score': 45,
            'membership_years': 0, 'previous_purchases': 1, 'avg_order_value': 95,
            'last_purchase_days': 5, 'product_category_preference': 'Books',
            'communication_channel': 'Email', 'satisfaction_score': 7
        },
        {
            'name': '💸 Budget Customer',
            'age': 24, 'gender': 'Female', 'income': 35000, 'spending_score': 30,
            'membership_years': 0, 'previous_purchases': 2, 'avg_order_value': 45,
            'last_purchase_days': 90, 'product_category_preference': 'Books',
            'communication_channel': 'SMS', 'satisfaction_score': 6
        }
    ]
    
    for i, customer in enumerate(test_customers, 1):
        print(f"\n{i}. {customer['name']}")
        print("-" * 50)
        
        # Remove name for analysis
        customer_data = {k: v for k, v in customer.items() if k != 'name'}
        
        # Analyze customer
        result = analyze_customer_for_upsell_crosssell(customer_data)
        
        # Display results
        print(f"👤 Customer Value Score: {result['customer_value_score']}/100")
        
        print(f"\n⬆️ UPSELL Analysis:")
        print(f"   Possible: {'✅ YES' if result['upsell']['possible'] else '❌ NO'}")
        print(f"   Confidence: {result['upsell']['confidence']}")
        print(f"   Reason: {result['upsell']['reason']}")
        
        print(f"\n➡️ CROSS-SELL Analysis:")
        print(f"   Possible: {'✅ YES' if result['crosssell']['possible'] else '❌ NO'}")
        print(f"   Confidence: {result['crosssell']['confidence']}")
        print(f"   Reason: {result['crosssell']['reason']}")
        
        if result['recommended_products']:
            print(f"\n🎁 Recommended Products:")
            for rec in result['recommended_products']:
                print(f"   • {rec['product']} ({rec['type']}) - {rec['probability']}%")
                print(f"     Reason: {rec['reason']}")
        
        print(f"\n📋 Action Plan:")
        for action in result['action_plan']:
            print(f"   {action}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_new_customers()
