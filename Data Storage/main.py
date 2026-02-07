from flask import Flask, request, jsonify, send_file
import store_data
import os
import json

app = Flask(__name__, static_folder='..', static_url_path='')

@app.route('/')
def serve_index():
    return send_file('../index.html')

@app.route('/save-profile', methods=['POST'])
def save_profile():
    try:
        data = request.get_json()
        
        # Extract data from the profile
        result = store_data.save_data(
            user_id=data.get('userId'),
            password=data.get('password'),
            age=data.get('age'),
            gender=data.get('gender'),
            smoking_habit='Yes' if data.get('habits', {}).get('smoking') else 'No',
            drinking_habit='Yes' if data.get('habits', {}).get('drinking') else 'No',
            pets=[],  # Can be enhanced to handle pet details
            dependents=[],  # Can be enhanced
            name=data.get('name'),
            phone_number=data.get('phone'),
            can_be_found_at=data.get('location'),
            facial_data={'data': data.get('facialData')}
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