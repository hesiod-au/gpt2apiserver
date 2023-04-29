from functools import wraps
from flask import Flask, request, jsonify, current_app
from pyChatGPT import ChatGPT
import os
# Read the environment variable
token = os.environ.get('CHATGPT_TOKEN')
# Make it available as a global variable
# globals()['token'] = token
app = Flask(__name__)

global api
api = ChatGPT(token, model="4")


def require_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if api is None:
            return jsonify({'status': 'error', 'message': 'API not initialized'}), 400
        return func(*args, **kwargs)
    return wrapper


# @app.route('/auth/google', methods=['POST'])
# def auth_google():
#     if request.json is None:
#         return jsonify({'status': 'error',
#                         'message': 'Missing request body'}), 400

#     email = request.json.get('email')
#     password = request.json.get('password')

#     if not email or not password:
#         return jsonify({'status': 'error',
#                         'message': 'Missing email or password'}), 400
#     global api
#     api = ChatGPT(auth_type='google', email=email, password=password)
#     return jsonify({'status': 'success'})
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/send_message', methods=['POST'])
@require_api
def send_message():
    if request.json is None:
        response = jsonify({'status': 'error', 'message': 'Missing request body'}), 400
        current_app.logger.debug(f"Response: {response}")
        return response

    message = request.json.get('message')
    id = request.json.get('id')

    if not message or not id:
        response = jsonify({'status': 'error', 'message': 'Missing required param'}), 400
        current_app.logger.debug(f"Response: {response}")
        return response

    resp = api.send_message(message=message, id=id)
    return jsonify(resp)


@app.route('/v1/chat/completions', methods=['POST'])
@require_api
def chat_completion_message():
    if request.json is None:
        response = jsonify({'status': 'error', 'message': 'Missing request body'}), 400
        current_app.logger.debug(f"Response: {response}")
        return response

    message = ""
    messages = request.json.get('messages')
    for msg in messages:
        message = message + f"{msg.role}: " + msg.content + "\n\n"
    id = request.json.get('id')
    if not id:
        id = "0"

    if not message:
        response = jsonify({'status': 'error', 'message': 'Missing required param'}), 400
        current_app.logger.debug(f"Response: {response}")
        return response

    resp = api.send_message(message=message, id=id)
    return jsonify(resp)


@app.route('/reset_conversation', methods=['GET'])
@require_api
def reset_conversation():
    api.reset_conversation()
    return jsonify({'status': 'success'})


@app.route('/clear_conversations', methods=['POST'])
@require_api
def clear_conversations():
    api.clear_conversations()
    return jsonify({'status': 'success'})


@app.route('/refresh_chat_page', methods=['POST'])
@require_api
def refresh_chat_page():
    api.refresh_chat_page()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
