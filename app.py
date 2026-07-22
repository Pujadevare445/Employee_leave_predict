import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the Logistic Regression model
with open('Logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ AI Employee Retention Analytics ⚡</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0b0f19;
            --card-bg: rgba(22, 28, 45, 0.7);
            --border-color: rgba(255, 255, 255, 0.1);
            --primary-neon: #00f2fe;
            --secondary-neon: #4facfe;
            --accent-purple: #7d5fff;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px 20px;
            overflow-x: hidden;
            position: relative;
        }

        /* Ambient Animated Glowing Orbs */
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(90px);
            opacity: 0.4;
            z-index: 1;
            animation: orbFloat 10s infinite ease-in-out alternate;
        }

        .orb-1 {
            width: 350px;
            height: 350px;
            background: var(--accent-purple);
            top: -50px;
            left: -50px;
        }

        .orb-2 {
            width: 400px;
            height: 400px;
            background: var(--primary-neon);
            bottom: -100px;
            right: -100px;
            animation-delay: -5s;
        }

        @keyframes orbFloat {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(30px, 40px) scale(1.1); }
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 28px;
            padding: 45px 40px;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            z-index: 2;
            animation: cardAppear 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes cardAppear {
            0% { opacity: 0; transform: translateY(30px) scale(0.96); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

        .header {
            text-align: center;
            margin-bottom: 35px;
        }

        .header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, var(--primary-neon) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        .header p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 8px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input, select {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 12px 16px;
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            border-color: var(--primary-neon);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.25);
            transform: translateY(-2deg);
        }

        select option {
            background-color: var(--bg-dark);
            color: var(--text-main);
        }

        .btn-submit {
            grid-column: 1 / -1;
            margin-top: 15px;
            padding: 16px;
            background: linear-gradient(135deg, var(--secondary-neon) 0%, var(--accent-purple) 100%);
            color: #ffffff;
            border: none;
            border-radius: 16px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 10px 25px -5px rgba(125, 95, 255, 0.4);
        }

        .btn-submit:hover {
            transform: translateY(-3deg);
            box-shadow: 0 15px 30px -5px rgba(0, 242, 254, 0.5);
            filter: brightness(1.1);
        }

        .result-box {
            margin-top: 30px;
            padding: 22px;
            border-radius: 18px;
            text-align: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            animation: pulseIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes pulseIn {
            0% { opacity: 0; transform: scale(0.92); }
            100% { opacity: 1; transform: scale(1); }
        }

        .result-title {
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .result-status {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--primary-neon);
            text-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        }
    </style>
</head>
<body>

    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>

    <div class="container">
        <div class="header">
            <h1>⚡ Employee Analytics Portal</h1>
            <p>Predict workforce outcomes using Logistic Classification</p>
        </div>

        <form action="/predict" method="post">
            <div class="grid">
                <div class="input-group">
                    <label>Education Level</label>
                    <select name="Education" required>
                        <option value="0">Bachelors (0)</option>
                        <option value="1">Masters (1)</option>
                        <option value="2">PHD (2)</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>Joining Year</label>
                    <input type="number" name="JoiningYear" placeholder="e.g. 2017" required>
                </div>

                <div class="input-group">
                    <label>City Location</label>
                    <select name="City" required>
                        <option value="0">Bangalore (0)</option>
                        <option value="1">Pune (1)</option>
                        <option value="2">New Delhi (2)</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>Payment Tier</label>
                    <select name="PaymentTier" required>
                        <option value="1">Tier 1</option>
                        <option value="2">Tier 2</option>
                        <option value="3">Tier 3</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>Age</label>
                    <input type="number" name="Age" placeholder="e.g. 28" required>
                </div>

                <div class="input-group">
                    <label>Gender</label>
                    <select name="Gender" required>
                        <option value="0">Female (0)</option>
                        <option value="1">Male (1)</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>Ever Benched</label>
                    <select name="EverBenched" required>
                        <option value="0">No (0)</option>
                        <option value="1">Yes (1)</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>Current Domain Exp (Yrs)</label>
                    <input type="number" name="ExperienceInCurrentDomain" placeholder="e.g. 3" required>
                </div>

                <button type="submit" class="btn-submit">Analyze Prediction 🚀</button>
            </div>
        </form>

        {% if prediction_text %}
            <div class="result-box">
                <div class="result-title">Classification Output</div>
                <div class="result-status">{{ prediction_text }}</div>
            </div>
        {% endif %}
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract the 8 expected features from form submission
    features = [
        float(request.form['Education']),
        float(request.form['JoiningYear']),
        float(request.form['City']),
        float(request.form['PaymentTier']),
        float(request.form['Age']),
        float(request.form['Gender']),
        float(request.form['EverBenched']),
        float(request.form['ExperienceInCurrentDomain'])
    ]
    
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    
    # Custom display label based on predicted class
    result = "Class 1 (High Likelihood)" if prediction[0] == 1 else "Class 0 (Low Likelihood)"

    return render_template_string(HTML_LAYOUT, prediction_text=f'Result: {result}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
