import pandas as pd
import calendar
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

def train_and_predict(df):
    # 🔹 Step 1: Prepare Date & Features
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    df = df.drop(columns=['Product_ID'])

    # 🔹 Step 2: Encode categorical columns
    label_encoders = {}
    for col in ['Category', 'Gender', 'Region', 'Season']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    category_encoder = label_encoders['Category']

    # 🔹 Step 3: Train model - Added more features and hyperparameters
    X = df[['Category', 'Gender', 'Region', 'Season', 'Month', 'Year']]  # Added Year
    y = df['Quantity_Sold']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1)  # Tuned parameters
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = r2_score(y_test, y_pred)

    # 🔹 Step 4: Actual Monthly Sales for Chart 1
    actual_monthly = df.groupby(['Year', 'Month'])['Quantity_Sold'].sum().reset_index()
    actual_monthly['label'] = actual_monthly.apply(
        lambda row: f"{calendar.month_name[row['Month']]} {row['Year']}", axis=1
    )
    actual_sales = actual_monthly[['label', 'Quantity_Sold']].to_dict(orient='records')

    # 🔹 Step 5: Forecast next 3 months with proper temporal handling
    latest_date = df['Date'].max()
    base = X.drop_duplicates(subset=['Category', 'Gender', 'Region', 'Season']).copy()
    
    forecast = []
    forecast_grouped = {}
    all_preds = []

    for i in range(1, 4):
        forecast_date = (latest_date + pd.DateOffset(months=i))
        forecast_month = forecast_date.month
        forecast_year = forecast_date.year

        temp = base.copy()
        temp['Month'] = forecast_month
        temp['Year'] = forecast_year  # Include the forecast year
        
        # Get season for the forecast month (simple implementation)
        if forecast_month in [12, 1, 2]:
            season = 'Winter'
        elif forecast_month in [3, 4, 5]:
            season = 'Spring'
        elif forecast_month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'Autumn'
            
        # Encode the season
        temp['Season'] = label_encoders['Season'].transform([season])[0]
        
        preds = model.predict(temp)
        all_preds.extend(preds.tolist())
        total_sales = float(round(preds.sum(), 2))

        forecast.append({
            "month": f"{calendar.month_name[forecast_month]} {forecast_year}",
            "predicted_total": total_sales
        })

        # 🔹 Grouped Forecast
        temp['preds'] = preds
        grouped = temp.groupby(['Category', 'Gender', 'Region'])['preds'].sum().reset_index()

        for _, row in grouped.iterrows():
            key = f"{label_encoders['Category'].inverse_transform([int(row['Category'])])[0]}_" + \
                  f"{label_encoders['Gender'].inverse_transform([int(row['Gender'])])[0]}_" + \
                  f"{label_encoders['Region'].inverse_transform([int(row['Region'])])[0]}"
            forecast_grouped[key] = forecast_grouped.get(key, 0) + float(row['preds'])

    # 🔹 Category % Change
    past_category_avg = df.groupby('Category')['Quantity_Sold'].mean().to_dict()
    predicted_cats = base.copy()
    predicted_cats['preds'] = all_preds[:len(base)]  # just first month predictions
    predicted_avg = predicted_cats.groupby('Category')['preds'].mean().to_dict()

    category_changes = []
    for cat, past_avg in past_category_avg.items():
        if cat in predicted_avg:
            change = ((predicted_avg[cat] - past_avg) / past_avg) * 100
            category_changes.append({
                "category": category_encoder.inverse_transform([int(cat)])[0],
                "change": round(float(change), 2)
            })

    return {
        "accuracy": float(round(accuracy * 100, 2)),
        "actual_sales": actual_sales,
        "forecast": forecast,
        "grouped": forecast_grouped,
        "category_change": category_changes
    }
