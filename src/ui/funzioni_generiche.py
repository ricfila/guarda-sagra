import tkinter as tk
from tkinter import ttk
import functools
import requests
import json
from config import configs

def replace_single_quotes(input_string):
    return input_string.replace("'", "''")

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