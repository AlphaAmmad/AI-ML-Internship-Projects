from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import pandas as pd
import json
from werkzeug.utils import secure_filename
from data_processor import DataProcessor
from model_trainer import ModelTrainer
import plotly
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_super_secret_key_1234567890'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the uploaded file
        try:
            processor = DataProcessor()
            df, validation_results = processor.process_csv(filepath)
            
            if validation_results['is_valid']:
                # Store processed data in session or temporary file
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'processed_{filename}')
                df.to_csv(processed_filepath, index=False)
                
                return render_template('forecast.html', 
                                     filename=filename,
                                     processed_filename=f'processed_{filename}',
                                     validation_results=validation_results,
                                     data_preview=df.head().to_html(classes='table table-striped'))
            else:
                flash(f"Data validation failed: {validation_results['errors']}")
                return redirect(url_for('index'))
                
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload a CSV file.')
    return redirect(url_for('index'))

@app.route('/forecast', methods=['POST'])
def generate_forecast():
    try:
        processed_filename = request.form['processed_filename']
        forecast_months = int(request.form['forecast_months'])
        
        if forecast_months < 1 or forecast_months > 24:
            flash('Please enter a forecast period between 1 and 24 months.')
            return redirect(url_for('index'))
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        
        # Load processed data
        df = pd.read_csv(filepath)
        
        # Train model and generate forecast
        trainer = ModelTrainer()
        model_results = trainer.train_and_forecast(df, forecast_months)
        
        # Create visualizations
        charts = create_charts(df, model_results)
        print("Charts created:", charts is not None)
        print("Chart keys:", list(charts.keys()) if charts else "None")

        return render_template('results.html',
                             forecast_data=model_results['forecast_df'].to_html(classes='table table-striped'),
                             model_performance=model_results['performance'],
                             charts=charts,
                             forecast_months=forecast_months)
        
    except Exception as e:
        flash(f"Error generating forecast: {str(e)}")
        return redirect(url_for('index'))

def create_charts(historical_df, model_results):
    """Create interactive charts for visualization"""
    forecast_df = model_results['forecast_df']

    # Prepare data for plotting
    historical_dates = pd.to_datetime(historical_df['Month'])
    forecast_dates = pd.to_datetime(forecast_df['Month'])



    # Create category breakdown chart
    categories = ['Miscellaneous', 'Financial', 'CapEx', 'COGS', 'Operating']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

    fig_categories = go.Figure()

    for i, category in enumerate(categories):
        if category in forecast_df.columns:
            fig_categories.add_trace(go.Scatter(
                x=forecast_dates,
                y=forecast_df[category],
                mode='lines+markers',
                name=category,
                line=dict(color=colors[i], width=3),
                marker=dict(size=6),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Amount: %{y:,.0f}<extra></extra>'
            ))

    fig_categories.update_layout(
        title={
            'text': 'AI Forecast by Category',
            'x': 0.5,
            'font': {'size': 18}
        },
        xaxis_title='Date',
        yaxis_title='Expenses',
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Convert to JSON for template
    charts = {
        'categories_chart': json.dumps(fig_categories, cls=plotly.utils.PlotlyJSONEncoder)
    }

    return charts

if __name__ == '__main__':
    app.run(debug=True)
