import configparser
import os

# Verrà usato per gestire preferenze e configurazioni. copia incolla da internet da tenere come esempio.
# Dal secondo commento in poi, fatto ad hoc

config = configparser.ConfigParser()
config['DEFAULT'] = dict(ServerAliveInterval='45', Compression='yes', CompressionLevel='9')
config['forge.example'] = {}
config['forge.example']['User'] = 'hg'
config['topsecret.server.example'] = {}

topsecret = config['topsecret.server.example']
topsecret['Port'] = '50022'  # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here

config['DEFAULT']['ForwardX11'] = 'yes'

#gestione file di configurazioni
configs_folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), ".configs")

if not os.path.exists(configs_folder_path):  # Create configs directory
    os.makedirs(configs_folder_path)

config_file_path = os.path.join(configs_folder_path, 'configs.ini')

with open(config_file_path, 'w') as configfile:  # Create configs.ini file
    config.write(configfile)

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