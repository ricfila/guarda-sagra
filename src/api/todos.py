from flask import jsonify, render_template
from . import app

todos = [
    {"user": 1, "id": 1, "title": "Fare la spesa", "completed": False},
    {"user": 1, "id": 2, "title": "Studiare per l'esame", "completed": True},
    {"user": 2, "id": 3, "title": "Riordinare gli appunti", "completed": True},
    {"user": 2, "id": 4, "title": "Andare a correre", "completed": False},
]

def _find_next_id():
    return max(todo["id"] for todo in todos) + 1

def _find_todo_by_id(t_id):
    for todo in todos:
        if todo["id"] == t_id or todo["id"] == int(t_id):
            return todo
    return None


# Prima di servire qualsiasi richiesta,
# verificare che il Content-type sia
# application/json, se non lo è allora
# restituire un messaggio di errore
#@app.before_request
#def check_cont_type_json():
    #if not request.is_json:
    #    return {"errore": "Content-type non supportato (deve essere JSON)"}, 415


# ----- TODOS -----

@app.get("/")
def index():
    #return "aaa"
    return render_template("index.html")

# Recupera tutti i Todo
@app.get("/todos")
def get_todos2():
    return jsonify(todos), 200


# Recupera un Todo dato il suo ID
# Se non lo trova, restituisce un
# oggetto JSON vuoto, ovvero {}, e
# risponde con stato HTTP 404
@app.get("/todos/<t_id>")
def get_todo_by_id(t_id):
    found = _find_todo_by_id(t_id)
    if not found:
        return jsonify({}), 404
    else:
        return jsonify(found), 200


# Crea un nuovo Todo, del quale l'id
# viene impostato al successivo id disponibile
# (come se fosse un autoincrementante)
@app.post("/todos")
def add_todo():
    new_todo = request.json
    new_todo["id"] = _find_next_id()
    todos.append(new_todo)
    return jsonify(new_todo), 201


# Modifica/Sostituisce un Todo esistente,
# restituendo al Client la risorsa modificata
# e lo stato HTTP 201
@app.put("/todos/<t_id>")
def put_todo(t_id):
    found = False
    for i in range(len(todos)):
        if todos[i]['id'] == int(t_id):
            found = True
            del todos[i]
            break
    if not found:
        return jsonify({}), 404
    todo = request.json
    todo["id"] = int(t_id)
    todos.append(todo)
    return jsonify(todo), 200


# Elimina un Todo esistente
@app.delete("/todos/<t_id>")
def delete_todo(t_id):
    deleted = {}
    for i in range(len(todos)):
        if todos[i]['id'] == int(t_id):
            deleted = todos[i]
            del todos[i]
            break
    if deleted == {}:
        return jsonify({}), 404
    else:
        return jsonify(deleted), 200

"""
def demone():
    app.run("localhost", port=5000, debug=False)

if __name__ == "__main__":
    #x = threading.Thread(target=demone, daemon=True)
    x = threading.Thread(target=app.run, kwargs=dict(port=5000, debug=False), daemon=True)
    x.start()

    i = 0
    while(True):
        print(i)
        i += 1
        time.sleep(2)
    
"""