
import os
from flask import Flask, jsonify, request, session, send_from_directory
from flask_session import Session
from inmemorydbadapter import InMemoryDBAdapter

app = Flask(__name__, static_folder="public/static")
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

API_BASE_ADDRESS = "/api"

def get_db_adapter():
    return InMemoryDBAdapter(session)

@app.route(API_BASE_ADDRESS + "/getActive", methods=['GET'])
def get_active():
    db = get_db_adapter()
    return jsonify(db.get_surveys())

@app.route(API_BASE_ADDRESS + "/getSurvey", methods=['GET'])
def get_survey():
    db = get_db_adapter()
    survey_id = request.args.get('surveyId')
    return jsonify(db.get_survey(survey_id))

@app.route(API_BASE_ADDRESS + "/changeName", methods=['GET'])
def change_name():
    db = get_db_adapter()
    obj_id = request.args.get('id')
    new_name = request.args.get('name')
    return jsonify(db.change_name(obj_id, new_name))

@app.route(API_BASE_ADDRESS + "/create", methods=['GET'])
def create():
    db = get_db_adapter()
    name = request.args.get('name')
    return jsonify(db.add_survey(name))

@app.route(API_BASE_ADDRESS + "/changeJson", methods=['POST'])
def change_json():
    db = get_db_adapter()
    data = request.get_json()
    obj_id = data.get('id')
    json_data = data.get('json')
    return jsonify(db.store_survey(obj_id, None, json_data))

@app.route(API_BASE_ADDRESS + "/post", methods=['POST'])
def post_results():
    db = get_db_adapter()
    data = request.get_json()
    post_id = data.get('postId')
    survey_result = data.get('surveyResult')
    return jsonify(db.post_results(post_id, survey_result))

@app.route(API_BASE_ADDRESS + "/delete", methods=['GET'])
def delete():
    db = get_db_adapter()
    obj_id = request.args.get('id')
    db.delete_survey(obj_id)
    return jsonify({'id': obj_id})

@app.route(API_BASE_ADDRESS + "/results", methods=['GET'])
def get_results():
    db = get_db_adapter()
    post_id = request.args.get('postId')
    return jsonify(db.get_results(post_id))

@app.route('/', defaults={'path': 'index.html'})
@app.route('/about', defaults={'path': 'index.html'})
@app.route('/run/<path:path>')
@app.route('/edit/<path:path>')
@app.route('/results/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    if not os.path.exists('flask_session'):
        os.makedirs('flask_session')
    
    app.run(debug=True)
