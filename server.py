from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import pandas as pd
import json
import webbrowser
from threading import Timer
from dotenv import load_dotenv
import subprocess

app = Flask(__name__, static_url_path='', static_folder='static')
load_dotenv()

# Global variable to store screening progress
screening_progress = []

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

def update_env_file(data):
    """Update .env file with new API keys"""
    env_vars = {}
    
    # Read existing .env file if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value

    # Update with new values based on selected AI model
    model = data.get('ai_model')
    
    if model == 'gemini':
        env_vars['GOOGLE_API_KEY'] = data.get('google_key', '')
    elif model in ['mixtral', 'llama3', 'gemma2']:
        env_vars['GROQ_API_KEY'] = data.get('groq_key', '')
    elif model == 'claude':
        env_vars['ANTHROPIC_API_KEY'] = data.get('anthropic_key', '')
    elif model == 'aws_claude':
        env_vars['AWS_ACCESS_KEY_ID'] = data.get('aws_access_key', '')
        env_vars['AWS_SECRET_ACCESS_KEY'] = data.get('aws_secret_key', '')
    elif model == 'openai':
        env_vars['OPENAI_API_KEY'] = data.get('openai_key', '')

    # Write updated variables back to .env file
    with open('.env', 'w') as f:
        for key, value in env_vars.items():
            f.write(f'{key}={value}\n')

def get_last_processed_paper(model_to_use):
    """Get the last processed paper number from existing output"""
    output_dir = os.path.join('AI_Output', model_to_use)
    excel_file = os.path.join(output_dir, 'screening_results.xlsx')
    
    if os.path.exists(excel_file):
        try:
            df = pd.read_excel(excel_file, sheet_name='screening_results_summary')
            if not df.empty:
                # Convert int64 to regular Python int for JSON serialization
                return int(df.iloc[:, 0].max())
        except Exception as e:
            print(f"Error reading Excel file: {str(e)}")
    return -1

def create_screening_config(data):
    """Create a temporary config file for main.py"""
    model_to_use = data.get('ai_model')
    last_paper = get_last_processed_paper(model_to_use)
    
    config = {
        'model_to_use': model_to_use,
        'n_agents': int(data.get('num_agents', 5)),
        'proj_location': '.',  # Use current directory
        'debug': False,
        'skip_criteria': True,
        'resume_from': last_paper + 1,  # Add resume point
        'pilot_percentage': float(data.get('pilot_percentage', 100))  # Add pilot percentage
    }
    
    with open('screening_config.json', 'w') as f:
        json.dump(config, f)

def get_existing_config():
    """Get existing configuration and criteria"""
    config = {
        'model_to_use': '',
        'n_agents': 5,
        'criteria': []
    }
    
    # Try to read existing config
    if os.path.exists('screening_config.json'):
        try:
            with open('screening_config.json', 'r') as f:
                saved_config = json.load(f)
                config['model_to_use'] = saved_config.get('model_to_use', '')
                config['n_agents'] = saved_config.get('n_agents', 5)
        except:
            pass
    
    # Try to read existing criteria
    if os.path.exists('ScreeningCriteria.csv'):
        try:
            df = pd.read_csv('ScreeningCriteria.csv')
            config['criteria'] = df.to_dict('records')
        except:
            pass
    
    return config

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get_config')
def get_config():
    """Endpoint to get existing configuration"""
    try:
        config = get_existing_config()
        return jsonify(config), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/screen', methods=['POST'])
def screen():
    try:
        # Get the uploaded file
        uploaded_file = request.files['data_file']
        if not uploaded_file:
            return jsonify({'error': 'No file uploaded'}), 400

        # Get file extension
        file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
        
        # Save the uploaded file temporarily
        temp_path = 'uploaded_papers' + file_ext
        uploaded_file.save(temp_path)

        # Read the file based on its extension
        if file_ext == '.csv':
            df = pd.read_csv(temp_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(temp_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        # Get the screening criteria
        criteria = json.loads(request.form['criteria'])
        
        # Save criteria to a CSV file as expected by main.py
        criteria_path = 'ScreeningCriteria.csv'
        criteria_df = pd.DataFrame(criteria)
        criteria_df.to_csv(criteria_path, index=False, encoding='utf-8-sig')

        # Convert to Excel format as expected by main.py
        excel_path = 'all_1400.xlsx'
        df.to_excel(excel_path, index=False)

        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Update .env file with API keys
        update_env_file(request.form)

        # Create config file for main.py
        create_screening_config(request.form)

        # Create output directory if it doesn't exist
        model_dir = os.path.join('AI_Output', request.form.get('ai_model'))
        os.makedirs(model_dir, exist_ok=True)

        # Clear previous screening progress
        global screening_progress
        screening_progress = []

        # Execute the screening script with the config
        pilot_percentage = float(request.form.get('pilot_percentage', 100))
        venv_python = sys.executable
        subprocess.Popen([venv_python, 'main.py', str(pilot_percentage)])

        return jsonify({'message': 'Screening process started successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/screening_progress')
def get_screening_progress():
    """Endpoint to get the current screening progress"""
    global screening_progress
    return jsonify(screening_progress)

def update_screening_progress(paper_number, title, decision):
    """Update the screening progress"""
    global screening_progress
    screening_progress.append({
        'paper_number': paper_number,
        'title': title,
        'decision': decision
    })

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)
