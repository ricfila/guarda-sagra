import configparser
import os

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
    sezioni = {"PostgreSQL": {"server": "localhost",
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
