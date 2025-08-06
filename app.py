from flask import Flask, render_template, request
import numpy as np
import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load model and scaler
model = load_model("model/stock_model.h5")
scaler = joblib.load("model/scaler.pkl")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form['last60']
    try:
        prices = [float(x) for x in data.split(',')]
        if len(prices) != 60:
            return "Error: You must enter exactly 60 values!"
        # Scale
        scaled = scaler.transform(np.array(prices).reshape(-1, 1))
        scaled = np.array(scaled).reshape(1, 60, 1)
        prediction = model.predict(scaled)
        prediction_price = scaler.inverse_transform(prediction)[0][0]
        return render_template("result.html", prediction=f"{prediction_price:.2f}")
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
