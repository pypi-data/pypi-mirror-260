import webbrowser
from flask import Flask, request, jsonify, send_file
from gevent.pywsgi import WSGIServer

def setup_webserver():
    app = Flask(__name__)

    # Enable CORS for all routes
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response

    @app.route('/auth') #Host the token processing html page
    def send_token():
        return send_file('token_getter.html')

    @app.route('/access_token', methods=["POST"]) #Listen for token webhook
    def receive_token():
      json_data = request.get_json()
      if 'access_token' in json_data:
        global global_token
        global_token = json_data['access_token']
        http_server.stop()
        print('Token obtained!')
        return jsonify({'message': 'Token received successfully'})
      
    http_server = WSGIServer(('127.0.0.1', 8888), app, log=None)

    def start_webserver():
        print('Authentificate in the opened tab')
        webbrowser.open(global_tooltip, 0)
        http_server.serve_forever()

    return start_webserver, http_server

def config_anilist():
  setup_function, _ = setup_webserver()  # Setup the server function here
  
  def gen_please(name, help):
      return f'Please input your {name} here ({help}):\n'
    
  def get_input(prompt, data_type = str):
      while True:
          user_input = input(prompt).lower()
          try:
              converted_input = data_type(user_input)
              return converted_input
          except ValueError:
              print("Invalid input. Please enter a valid", data_type.__name__)  

  def anilist_generate_api_key(client_id):
      global global_tooltip
      global_tooltip = f"https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=token" 
      setup_function()  # Start the server here
      user_token = global_token
      return user_token

  webbrowser.open('https://anilist.co/settings/developer', 0)
  anilist_client_token = get_input(gen_please('Anilist API Client ID',"Create a new client and copy its ID"))
  anilist_user_token = anilist_generate_api_key(anilist_client_token)
  return anilist_user_token