from flask import Flask, jsonify, request# Импортируем необходимые модули и функции из фреймворка Flask
import functions# Импортируем пользовательские функции из модуля 'functions'
from functions import jsonify_response, get_profiles_from_file, set_profiles_to_file
import random # Импортируем модуль random для генерации случайных идентификаторов
from flask import jsonify

# Создаем экземпляр приложения Flask
app = Flask(__name__)


# Определяем маршрут для корневой точки входа
@app.route("/")
def index():
    return "Welcome to the Airis database(CRUD)"

# Определяем маршрут для получения всех профилей
@app.route("/profiles")
def get_profiles():
    result = get_profiles_from_file()
    return jsonify_response(result)

# Определяем маршрут для получения конкретного профиля по идентификатору
@app.route("/profiles/<int:id>")
def get_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            return jsonify_response(profile)
    return jsonify_response(None, message=f"There is no profile with ID:{id}", status_code=404)

# Определяем маршрут для создания нового профиля (метод HTTP POST)
@app.route("/profiles/create", methods=["POST"])
def create_profile():
    profiles = get_profiles_from_file()
    login = request.form["login"]
    for profile in profiles:
        if profile.get("login") == login:
            return jsonify_response(None, message="Такой логин есть, попробуйте повторить еще раз")
    age = request.form["age"]
    cash = request.form["cash"]
    nat = request.form["nationality"]
    country = request.form["country"]
    language = request.form["language"]

    create_profile = {
        "id": random.randrange(1, 100_000),
        "login": login,
        "age": age,
        "cash": cash,
        "nationality": nat,
        "country": country,
        "language": language
    }

    profiles.append(create_profile)
    set_profiles_to_file(profiles)

    return jsonify_response(create_profile)

# Определяем маршрут для обновления профиля по идентификатору (метод HTTP POST)
@app.route("/profiles/update/<int:id>", methods=["POST"])
def update_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            for key in request.form:
                profile[key] = request.form[key]
            set_profiles_to_file(profiles)    # Сохраняем обновленные профили в файл
            return jsonify_response(profile)  # Используем jsonify_response вместо jsonify
    return jsonify_response(None, message=f"Sorry, but cannot find a person with ID {id}", status_code=404)


# Определяем маршрут для удаления профиля по идентификатору (метод HTTP POST)
@app.route('/profiles/delete/<int:id>', methods=['POST'])
def delete_profile_by_id(id):
    profiles = get_profiles_from_file()  # Retrieve profiles from the file

    # Проверяем, существует ли профиль с указанным ID
    index = next((i for i, profile in enumerate(profiles) if profile['id'] == id), None)

    if index is not None:
        # Если профиль существует, удаляем его
        profiles.pop(index)
        set_profiles_to_file(profiles)    # Сохраняем обновленные профили в файл
        return jsonify_response(True, message=f"Profile with ID {id} deleted.", status_code=200)
    else:
        # Если профиль не существует, возвращаем ошибку
        return jsonify_response(False, message=f"Profile with ID {id} not found.", status_code=404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
