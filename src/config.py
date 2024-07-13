import configparser
import os
import requests
import json

configs = configparser.ConfigParser()


def init():
    # Crea la cartella .configs e il file configs.ini se non esistono
    configs_folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), ".configs")
    if not os.path.exists(configs_folder_path):  # Create configs directory
        os.makedirs(configs_folder_path)
    config_file_path = os.path.join(configs_folder_path, 'configs.ini')
    if not os.path.exists(config_file_path):
        open(config_file_path, 'x')

    # Importa le impostazioni dal file
    configs.read(config_file_path)

    # Aggiunge impostazioni di default se non erano presenti nel file
    sezioni = {"API": {"server": "localhost",
                       "port":5000},
               "PostgreSQL": {"server": "localhost",
                              "port": 5432,
                              "database": "gs",
                              "username": "postgres",
                              "password": "pwd"},
               "SQLite": {"enabled": "true"}
               }

    for k, v in sezioni.items():
        if (k not in configs.sections()
                or any(key not in configs[k] for key in v.keys())):
            configs[k] = v

    # Salva tutte le impostazioni (vecchie e nuove) su file
    configfile = open(config_file_path, 'w')
    configs.write(configfile)

def api_url():
    return 'http://' + configs['API']['server'] + ':' + configs['API']['port']
def api_get(query_url, id_profilo = -1, id_listino = -1, id_tipologia = -1):
    request_url = api_url() + query_url

    if id_profilo != -1:
        request_url += str(id_profilo)
    elif id_listino != -1:
        request_url += str(id_listino)
    elif id_tipologia != -1:
        request_url += '/' + str(id_tipologia)

    response = requests.get(request_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore api_get: {response.status_code} - {response.text}")
def api_post(query_url, data_to_send):
    request_url = api_url() + query_url

    json_data = json.dumps(data_to_send)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(request_url, data=json_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore api_post: {response.status_code} - {response.text}")



''' #ESEMPIO LETTURA DA CONFIG
config = configparser.ConfigParser()
config.sections() >>>[]
config.read('example.ini') >>>['example.ini']
config.sections() >>>['forge.example', 'topsecret.server.example']
'forge.example' in config >>>True
'python.org' in config >>>False
config['forge.example']['User'] >>>'hg'
config['DEFAULT']['Compression'] >>>'yes'
topsecret = config['topsecret.server.example']
topsecret['ForwardX11'] >>>'no'
topsecret['Port'] >>>'50022'
for key in config['forge.example']:  
    print(key)
>>>user
>>>compressionlevel
>>>serveraliveinterval
>>>compression
>>>forwardx11
config['forge.example']['ForwardX11'] >>>'yes'
'''
