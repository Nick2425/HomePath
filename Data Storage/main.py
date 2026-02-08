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
        print("Received /save-profile data:", data)

        if not isinstance(data, dict):
            return jsonify({'success': False, 'message': 'Invalid JSON body'}), 400

        # Accept both camelCase and snake_case keys from the frontend
        user_id = data.get('userId') or data.get('user_id')
        password = data.get('password')

        personal_info = data.get('personal_info') or {}
        if not isinstance(personal_info, dict):
            personal_info = {}

        # These may be sent at top-level (older client) or nested under personal_info (current client)
        name_val = data.get('name') if data.get('name') is not None else personal_info.get('name')
        phone_val = data.get('phone') if data.get('phone') is not None else personal_info.get('phone_number')
        location_val = data.get('location') if data.get('location') is not None else personal_info.get('can_be_found_at')
        age_val = data.get('age') if data.get('age') is not None else personal_info.get('age')
        gender_val = data.get('gender') if data.get('gender') is not None else personal_info.get('sex_at_birth')
        dependents_val = data.get('dependents') if data.get('dependents') is not None else personal_info.get('dependents')

        if not user_id:
            return jsonify({'success': False, 'message': 'Missing user_id'}), 400

        # Extract data from the profile
        smoking_val = None
        drinking_val = None
        habits_obj = data.get('habits') or {}
        if isinstance(habits_obj, dict):
            smoking_val = habits_obj.get('smoking')
            drinking_val = habits_obj.get('drinking')

        pets_list = []
        pets_obj = data.get('pets') or {}
        # Frontend may send pets as dict of booleans OR already as a list
        if isinstance(pets_obj, dict):
            if pets_obj.get('dog'):
                pets_list.append('dog')
            if pets_obj.get('cat'):
                pets_list.append('cat')
            if pets_obj.get('other'):
                pets_list.append('other')
        elif isinstance(pets_obj, list):
            pets_list = [p for p in pets_obj if isinstance(p, str)]

        try:
            if dependents_val is not None and dependents_val != "":
                dependents_val = int(dependents_val)
        except Exception:
            dependents_val = None
        result = store_data.save_data(
            user_id=user_id,
            password=password,
            age=age_val,
            gender=gender_val,
            smoking_habit=smoking_val,
            drinking_habit=drinking_val,
            pets=pets_list,
            dependents=dependents_val,
            name=name_val,
            phone_number=phone_val,
            can_be_found_at=location_val,
            facial_data=data.get('facialData')
        )
        print("Save result:", result)
        if result is False:
            return jsonify({'success': False, 'message': 'Failed to save profile'}), 500
        return jsonify({'success': True, 'message': 'Profile saved successfully'})
    except Exception as e:
        print("Error in /save-profile:", str(e))
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