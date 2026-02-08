from flask import Flask, request, jsonify
from ..models.user import User, UserRole

# Seed users
users: list[User] = [
    User("admin@pulsefleet.com", "", UserRole.ADMIN),
    User("inactive@pulsefleet.com", "", UserRole.DRIVER, active=False),
    User("dispatcher@pulsefleet.com", "", UserRole.DISPATCHER),
    User("driver@pulsefleet.com", "", UserRole.DRIVER),
]


# Main app definition
def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    def get_user(email):
        for user in users:
            if user.email == email:
                return user

    @app.route("/auth/login", methods=["POST"])
    def login():
        if not request.is_json:
            return jsonify({"message": "Body must be json"}), 400

        data = request.get_json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            return {"message": "Malformed request"}, 400

        user = get_user(email)

        if user and user.validate_password(password):
            if not user.active:
                return {"message": "Inactive user"}, 403

            return (
                jsonify(
                    {
                        "message": "Successfully generated token",
                        "token": user.generate_token(),
                    }
                ),
                200,
            )
        else:
            return {"message": "Invalid credentials"}, 401

    @app.route("/")
    def main():
        return "Hello World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
