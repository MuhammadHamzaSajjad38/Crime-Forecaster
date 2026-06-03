from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

# Correct syntax for initializing the Flask app
app = Flask(__name__)

# --- Load All Model Assets at Startup ---
try:
    with open('models/crime_model_v2.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/feature_encoders_v2.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    with open('models/feature_columns_v2.pkl', 'rb') as f:
        model_columns = pickle.load(f)
    with open('models/scaler_v2.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('models/target_encoder_v2.pkl', 'rb') as f:
        target_encoder = pickle.load(f)
    
    # We get the string names from the loaded encoder object for dropdowns
    location_options = list(label_encoders['Location Description'].classes_)
    
    # For districts, we load the saved list of unique numbers
    with open('models/district_options.pkl', 'rb') as f:
        district_options = pickle.load(f)

    print("Model and assets loaded successfully.")
except Exception as e:
    print(f"Error loading files: {e}")
    # Set to None so the app knows there's an issue
    model = None
    location_options = ["STREET", "RESIDENCE"] # Fallback values
    district_options = [1.0, 2.0] # Fallback values

# =======================================================
# --- APPLICATION ROUTES ---
# =======================================================

# --- Homepage Route ---
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# --- Predictor Page Route (GET request) ---
@app.route('/predictor')
def predictor():
    # Get the current time to set as a default in the form
    now = datetime.now()
    return render_template('predictor.html', 
                           title='Crime Predictor',
                           location_options=location_options,
                           district_options=district_options,
                           now=now)

# --- Forecast Logic Route (POST request) ---
@app.route('/forecast', methods=['POST'])
def forecast():
    if not model:
        return redirect(url_for('predictor', error="Model not loaded."))

    now = datetime.now() # Define 'now' for the error case

    try:
        # 1. Get Data from Form
        form_data = {
            'Latitude': [float(request.form['latitude'])],
            'Longitude': [float(request.form['longitude'])],
            'Location Description': [request.form['location_description']],
            'District': [float(request.form['district'])],
            'Beat': [int(request.form['beat'])],
            'Date': [request.form['date']],
            'Time': [request.form['time']],
            'Arrest': [request.form['arrest'] == 'True'],
            'Domestic': [request.form['domestic'] == 'True']
        }
        
        # 2. Preprocess the Input Data
        input_df = pd.DataFrame(form_data)
        datetime_str = input_df['Date'][0] + ' ' + input_df['Time'][0]
        dt_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        input_df['Year'] = dt_object.year
        input_df['Month'] = dt_object.month
        input_df['Day'] = dt_object.day
        input_df['Hour'] = dt_object.hour
        
        # Only encode truly categorical columns from the form
        # (Latitude, Y Coordinate etc. are in label_encoders because they were
        #  object dtype in the CSV, but they are numeric — do NOT encode them)
        categorical_form_cols = ['Location Description']
        for col in categorical_form_cols:
            if col in input_df.columns and col in label_encoders:
                input_df[col] = label_encoders[col].transform(input_df[col])[0]
        
        placeholder_values = {'Block': 0, 'IUCR': 0, 'Description': 0, 'FBI Code': 0, 'X Coordinate': 0, 'Y Coordinate': 0, 'Ward': 0, 'Community Area': 0}
        for col, val in placeholder_values.items():
            if col in model_columns and col not in input_df.columns:
                input_df[col] = val

        features_for_prediction = input_df.reindex(columns=model_columns, fill_value=0)
        scaled_features = scaler.transform(features_for_prediction)

        # 3. Predict and Decode
        prediction_code = model.predict(scaled_features)[0]
        predicted_crime = target_encoder.inverse_transform([prediction_code])[0]
        
        # Handle confidence score based on model type
        try:
            # This will work if your model was trained with voting='soft'
            prediction_proba = model.predict_proba(scaled_features)[0]
            confidence_value = round(np.max(prediction_proba) * 100, 2)
        except AttributeError:
            # This is the fallback for models with voting='hard'
            confidence_value = "N/A"

        # 4. Render the PREDICTOR page with results
        return render_template('predictor.html',
                       title='Prediction Result',
                       prediction=predicted_crime.title(),
                       confidence=confidence_value,
                       lat=float(request.form['latitude']),
                       lon=float(request.form['longitude']),
                       location_options=location_options,
                       district_options=district_options,
                       now=now
                       )

    except Exception as e:
        print(f"Error during forecast: {e}")
        return render_template('predictor.html', 
                               error="An error occurred during prediction. Please check your inputs.",
                               location_options=location_options,
                               district_options=district_options,
                               now=now)


# --- Static Page Routes ---
@app.route('/dataset')
def dataset():
    return render_template('dataset.html', title='Dataset Analysis')

@app.route('/model-tech')
def model_tech():
    return render_template('model-tech.html', title='Model & Technology')

@app.route('/about')
def about():
    return render_template('about.html', title='About Project')

@app.route('/team')
def team():
    return render_template('team.html', title='Our Team')

# Correct syntax for running the app
if __name__ == '__main__':
    app.run(debug=True)