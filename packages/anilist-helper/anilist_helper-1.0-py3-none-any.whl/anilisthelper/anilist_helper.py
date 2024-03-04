from gevent import monkey
monkey.patch_all()
import requests, time, json, os, webbrowser, datetime
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
  script_path = os.path.dirname(os.path.abspath(__file__))
  config = os.path.join(script_path, 'data', 'config', 'config.json')

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

  config_dict = {}
  webbrowser.open('https://anilist.co/settings/developer', 0)
  config_dict['anilist_client_token'] = get_input(gen_please('Anilist API Client ID',"Create a new client and copy its ID"))
  config_dict['anilist_user_token'] = anilist_generate_api_key(config_dict['anilist_client_token'])
  utils_save_json(config ,config_dict)

def init_setup():

  script_path = os.path.dirname(os.path.abspath(__file__))
  anilist_cache = os.path.join(script_path, 'data', 'cache', 'anilist_cache.json')
  search_cache = os.path.join(script_path, 'data', 'cache', 'search_cache.json')
  config = os.path.join(script_path, 'data', 'config', 'config.json')
  script_files = [anilist_cache, search_cache, config]
  for file in script_files:
    folder_path = os.path.dirname(file)
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
    does_exist = os.path.exists(file)
    if not does_exist:
      utils_save_json(file, {})
  if not utils_read_json(config):
    print('Config not found! Please follow the on-screen instructions. Generating....')
    config_anilist()

    
def clear_cache():
  cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cache')
  files = os.listdir(cache_path)
  for file in files:
    utils_save_json(os.path.join(cache_path, file), {})
  pass

def utils_save_json(file_path, data, overwrite = True):
  def update_json():
    json_copy = utils_read_json(file_path)
    if json_copy is None:
      json_copy = {}
    json_copy.update(data)
    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(json_copy, file, indent=4, ensure_ascii=False)

  json_file = utils_read_json(file_path)
  if json_file != None:
      if overwrite:
        with open(file_path, "w", encoding="utf-8") as file:
          json.dump(data, file, indent=4, ensure_ascii=False)
      else:
        update_json()
  else:
    update_json() 

def utils_read_json(file_path):
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
      data = json.load(json_file)
    if data == {}:
      return None
    else:
      return data
  else:
    return None

# Helper function for making GraphQL requests
def make_graphql_request(query, variables=None):
    
    # Constants for GraphQL endpoint and headers
    ANILIST_API_URL = 'https://graphql.anilist.co'
    HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Bearer {anilist_user_token}'}

    def make_request():
        response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
        return response

    retries = 0
    while True:
        response = make_request()
        if response.status_code == 200:
            return response.json().get('data', {})
        elif response.status_code == 429:
            print(f"Rate limit exceeded. Waiting before retrying...")
            retry_after = int(response.headers.get('retry-after', 1))
            time.sleep(retry_after)
            retries += 1
        elif response.status_code == 500 or response.status_code == 400:
            print(f"Unknown error occured, retrying...")
            retries += 1
        else:
            print(f"Error {response.status_code}: {variables}")
            return {}

        # Exponential backoff with a maximum of 5 retries
        if retries >= 5:
            print("Maximum retries reached. Exiting.")
            return {}
            
        print(f"Retrying... (Attempt {retries})")

def get_latest_anime_entry_for_user(username, status = 'ALL'):
    status = status.upper()
    status_options = ['CURRENT', 'PLANNING', 'COMPLETED', 'DROPPED', 'PAUSED', 'REPEATING']
    if status != 'ALL':
      if not status in status_options:
        print("Invalid status option. Allowed options are:", ', '.join(str(option) for option in status_options) )
        return
      query = '''
              query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME, status: %s, sort: [UPDATED_TIME_DESC]) {
              ''' %status
    else:
      query = '''
              query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME, sort: [UPDATED_TIME_DESC]) {
              '''    
    query += '''
                lists {
                  entries {
                    id
                    progress
                    status
                    media {
                      id
                      episodes
                      title {
                        romaji
                        english
                        native
                      }
                      synonyms
                      status
                      startDate {
                        year
                        month
                        day
                      }
                      endDate {
                        year
                        month
                        day
                      }
                      nextAiringEpisode {
                        episode
                      }
                      format
                      relations {
                        edges {
                          relationType(version: 2)
                          node {
                            id
                            title {
                              romaji
                            }
                            status
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            '''
    variables = {'username': username}

    data = make_graphql_request(query, variables)

    if not username in user_entries:
      user_entries[username] = {}
      
    if data:
        entries = data.get('MediaListCollection', {}).get('lists', [])[0].get('entries', [])
        if entries:
            for anime in entries:
              anime_id = str(anime['media']['id'])
              anime_info = generate_anime_entry(anime['media'])
              user_entry = {}  # Initialize as a dictionary if not already initialized
              user_entry[anime_id] = {}  # Initialize as a dictionary if not already initialized
              user_entry[anime_id].update(anime_info)
              user_entry[anime_id]['watched_ep'] = anime['progress']
              user_entry[anime_id]['watching_status'] = anime['status']
              user_entries[username][anime_id] = user_entry
              return user_entry

    print(f"No entries found for {username}'s planned anime list.")
    return None

def get_all_anime_for_user(username, status = 'ALL'):
    status = status.upper()
    status_options = ['CURRENT', 'PLANNING', 'COMPLETED', 'DROPPED', 'PAUSED', 'REPEATING']
    if status != 'ALL':
      if not status in status_options:
        print("Invalid status option. Allowed options are:", ', '.join(str(option) for option in status_options) )
        return
      query = '''
              query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME, status: %s, sort: [UPDATED_TIME_DESC]) {
              ''' %status
    else:
      query = '''
              query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME, sort: [UPDATED_TIME_DESC]) {
              '''    
    query += '''
                lists {
                  entries {
                    id
                    progress
                    status
                    media {
                      id
                      episodes
                      title {
                        romaji
                        english
                        native
                      }
                      synonyms
                      status
                      startDate {
                        year
                        month
                        day
                      }
                      endDate {
                        year
                        month
                        day
                      }
                      nextAiringEpisode {
                        episode
                      }
                      format
                      relations {
                        edges {
                          relationType(version: 2)
                          node {
                            id
                            title {
                              romaji
                            }
                            status
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            '''
    variables = {'username': username}

    data = make_graphql_request(query, variables)

    if not username in user_entries:
      user_entries[username] = {}

    user_ids = {}
      
    if data:
        entries = data.get('MediaListCollection', {}).get('lists', [])
        full_entries = {}
        for entry in entries: 
          for list_entry in entry['entries']:
            full_entries[str(list_entry['id'])] = {}
            full_entries[str(list_entry['id'])].update(list_entry) 
        if full_entries:
            for anime_entry in full_entries:
              anime = full_entries[anime_entry]
              anime_entry_data = anime['media']
              anime_id = anime_entry_data['id']
              anime_id = str(anime_id)
              anime_info = generate_anime_entry(anime_entry_data)
              user_ids[anime_id] = {}  # Initialize as a dictionary if not already initialized
              user_ids[anime_id].update(anime_info)
              user_ids[anime_id]['watched_ep'] = anime['progress']
              user_ids[anime_id]['watching_status'] = anime['status']
              user_entries[username].update(user_ids)
            return user_ids

    print(f"No entries found for {username}'s planned anime list.")
    return None

def get_anime_entry_for_user(username, anilist_id):
  anilist_id = str(anilist_id)
  try:
    if anilist_id in user_entries[username]:
          return {anilist_id: user_entries[username][anilist_id]}
  except KeyError:
    get_all_anime_for_user(username)
    return get_anime_entry_for_user(username, anilist_id)
  return None

def get_anime_info(anime_id):
    anime_cache = utils_read_json(anilist_id_cache_path)
    anime_id = str(anime_id)
    if not anime_id:
      return None
    def fetch_from_anilist():
      # Fetch anime info from Anilist API or any other source
      anime_info = anilist_fetch_anime_info(anime_id)
      # Cache the fetched anime info
      utils_save_json(anilist_id_cache_path, anime_info, False)
      return anime_info
    # Check if anime_id exists in cache
    try:
      if anime_id in anime_cache:
          print("Returning cached result for anime_id:", anime_id)
          return anime_cache[anime_id]
      else:
        return fetch_from_anilist()
    except TypeError:
      return fetch_from_anilist()


def anilist_fetch_anime_info(anilist_id):
    query = '''
    query ($mediaId: Int) {
      Media(id: $mediaId) {
        id
        episodes
        title {
          romaji
          english
          native
        }
        synonyms
        status
        startDate {
          year
          month
          day
        }
        endDate {
          year
          month
          day
        }
        nextAiringEpisode {
          episode
        }
        format
        relations {
        edges {
            relationType(version: 2)
            node {
                id
                title {
                  romaji
                }  
                status
            }
          }
        }
      }
    }
    '''
    
    variables = {'mediaId': anilist_id}

    data = make_graphql_request(query, variables)
    anime_data = {}
    if data:
      anime = data.get('Media', {})
      if anime:
        anime_id = str(anime['id'])
        anime_info = anime
        anime_data[anime_id] = {}
        anime_data[anime_id].update(generate_anime_entry(anime_info))
      return anime_data
    return {}

def generate_anime_entry(anime_info):
  def get_release_date(anime_data):
      start_date = anime_data.get('startDate', {})
      day = start_date.get('day', 1)
      day = 1 if day is None else day
      try:
        release_date = datetime.datetime(start_date['year'], start_date.get('month', 1), day).strftime('%Y-%m-%d')
      except TypeError:
        release_date = None
      return release_date
    
  def get_end_date(anime_data):
      end_date = anime_data.get('endDate', {})
      day = end_date.get('day', 1)
      day = 1 if day is None else day
      try:
        end_date = datetime.datetime(end_date['year'], end_date.get('month', 1), day).strftime('%Y-%m-%d')
      except TypeError:
        end_date = None
      return end_date     

  def getRelated():
    relations = {}
    edges = anime_info['relations']['edges']
    for edge in edges:
      if edge['relationType'] == 'PREQUEL' or edge['relationType'] == 'SEQUEL':
        relations[edge['node']['id']] = {}
        relations[edge['node']['id']]['main_title'] = edge['node']['title']['romaji']
        relations[edge['node']['id']]['status'] = edge['node']['status']
        relations[edge['node']['id']]['type'] = edge['relationType']
    if not relations:
      relations = None
    return relations

  anime_data = {}
  anime_data['total_eps'] = anime_info['episodes']
  anime_data['main_title'] = anime_info['title']['romaji']
  anime_data['synonyms'] = [
      anime_info['title']['romaji'],
      anime_info['title']['english'],
      anime_info['title']['native'],
  ] + anime_info['synonyms']
  anime_data['synonyms'] = [item for item in anime_data['synonyms'] if item is not None]  
  anime_data['status'] = anime_info['status']
  anime_data['release_date'] = get_release_date(anime_info)
  anime_data['end_date'] = get_end_date(anime_info)
  try:
    anime_data['upcoming_ep'] = anime_info.get('nextAiringEpisode').get('episode')
  except:
    anime_data['upcoming_ep'] = None
  anime_data['format'] = anime_info['format']
  anime_data['related'] = getRelated()
  return anime_data

def get_id(name):
  search_cache = utils_read_json(search_cache_path)
  
  def fetch_from_anilist():
    # Fetch anime info from Anilist API or any other source
    anime_info = anilist_fetch_id(name)
    if not anime_info:
      return None
    json_out = {name: anime_info}
    # Cache the fetched anime info
    utils_save_json(search_cache_path, json_out, False)
    return anime_info
  
  # Check if anime_id exists in cache
  try:
    if name in search_cache:
        print("Returning cached result for search query:", name)
        return search_cache[name]
    else:
        return fetch_from_anilist()
  except TypeError:
    return fetch_from_anilist()
      
def anilist_fetch_id(name):
    query = '''
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        id
      }
    }
    '''
    variables = {'search': name}
    data = make_graphql_request(query, variables)

    if data:
        anime_list = data['Media']['id']

        if anime_list:
            return anime_list

    return []

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(data_path):
  init_setup()
user_entries = {}
try:
  anilist_user_token = utils_read_json(os.path.join(data_path, 'config', 'config.json'))['anilist_user_token']
except:
  print('Config not found! Please follow the on-screen instructions. Generating....')
  config_anilist()
  anilist_user_token = utils_read_json(os.path.join(data_path, 'config', 'config.json'))['anilist_user_token']
anilist_id_cache_path = os.path.join(data_path, 'cache', 'anilist_cache.json')
search_cache_path = os.path.join(data_path, 'cache', 'search_cache.json')
