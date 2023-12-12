from flask import Flask, jsonify, request
import functions

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Airis database(CRUD)"

@app.route("/profiles")
def get_profiles():
    result = functions.get_profiles_from_file()
    return functions.jsonify_response(result)

@app.route("/profiles/<int:id>")
def get_profile_by_id(id):
    profiles = functions.get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            return functions.jsonify_response(profile)
    return functions.jsonify_response(None, message=f"There is no profile with ID:{id}", status_code=404)

@app.route("/profiles/create", methods=["POST"])
def create_profile():
    profiles = functions.get_profiles_from_file()
    login = request.form.get("login")

    for profile in profiles:
        if profile.get("login") == login:
            return functions.jsonify_response(None, message="Такой логин есть, попробуйте повторить еще раз")

    age = request.form.get("age")
    cash = request.form.get("cash")
    nat = request.form.get("nationality")
    country = request.form.get("country")
    language = request.form.get("language")

    create_profile = {
        "id": len(profiles) + 1,
        "login": login,
        "age": age,
        "cash": cash,
        "nationality": nat,
        "country": country,
        "language": language
    }

    profiles.append(create_profile)
    functions.set_profiles_to_file(profiles)

    return functions.jsonify_response(create_profile)

@app.route("/profiles/update/<int:id>", methods=["POST"])
def update_profile_by_id(id):
    profiles = functions.get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            for key, value in request.form.items():
                profile[key] = value
            functions.set_profiles_to_file(profiles)
            return functions.jsonify_response(profile)
    return functions.jsonify_response(None, message=f"Sorry, but cannot find a person with ID {id}", status_code=404)

@app.route('/profiles/delete/<int:id>', methods=['POST'])
def delete_profile_by_id(id):
    profiles = functions.get_profiles_from_file()
    index = next((i for i, profile in enumerate(profiles) if profile['id'] == id), None)

    if index is not None:
        profiles.pop(index)
        functions.set_profiles_to_file(profiles)
        return functions.jsonify_response(True, message=f"Profile with ID {id} deleted.", status_code=200)
    else:
        return functions.jsonify_response(False, message=f"Profile with ID {id} not found.", status_code=404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
