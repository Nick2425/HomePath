from flask import Flask, request, jsonify, send_file
import store_data
import os
import json

app = Flask(__name__, static_folder='..', static_url_path='')

# Allow simple CORS for local development
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

@app.route('/')
def serve_index():
    return send_file('../index.html')

@app.route('/save-profile', methods=['POST'])
def save_profile():
    try:
        data = request.get_json()
        
        # Extract data from the profile
        # Preserve the actual habit values (e.g., 'smoker', 'non-smoker', 'occasional')
        smoking_val = None
        drinking_val = None
        if isinstance(data.get('habits'), dict):
            smoking_val = data['habits'].get('smoking')
            drinking_val = data['habits'].get('drinking')

        # Convert pets booleans to a list of pet types
        pets_list = []
        pets_obj = data.get('pets') or {}
        if isinstance(pets_obj, dict):
            if pets_obj.get('dog'):
                pets_list.append('dog')
            if pets_obj.get('cat'):
                pets_list.append('cat')
            if pets_obj.get('other'):
                pets_list.append('other')

        # Dependents may be sent as a number or string
        dependents_val = data.get('dependents')
        try:
            # normalize to int when possible
            if dependents_val is not None and dependents_val != "":
                dependents_val = int(dependents_val)
        except Exception:
            dependents_val = None

        result = store_data.save_data(
            user_id=data.get('userId'),
            password=data.get('password'),
            age=data.get('age'),
            gender=data.get('gender'),
            smoking_habit=smoking_val,
            drinking_habit=drinking_val,
            pets=pets_list,
            dependents=dependents_val,
            name=data.get('name'),
            phone_number=data.get('phone'),
            can_be_found_at=data.get('location'),
            facial_data=data.get('facialData')
        )
        
        return jsonify({'success': True, 'message': 'Profile saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/load-profile/<user_id>', methods=['GET'])
def load_profile(user_id):
    try:
        filename = f"{user_id}.json"
        data = store_data.load_data(filename)
        if data:
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)