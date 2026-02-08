from flask import Flask, request, jsonify
from fleet_pulse.auth.decorators import requires_roles
from ..models.user import User, UserRole

# Seed users
users: list[User] = [
    User("admin@fleetpulse.com", "", UserRole.ADMIN),
    User("inactive@fleetpulse.com", "", UserRole.DRIVER, active=False),
    User("dispatcher@fleetpulse.com", "", UserRole.DISPATCHER),
    User("driver@fleetpulse.com", "", UserRole.DRIVER),
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
        email = data.get("email")
        password = data.get("password")

        if email is None or password is None:
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

    @requires_roles([UserRole.ADMIN])
    @app.route("/admin/health", methods=["GET"])
    def admin_health():
        return {"message": "Success!"}, 200

    @requires_roles([UserRole.ADMIN, UserRole.DISPATCHER])
    @app.route("/dispatch/jobs", methods=["GET"])
    def dispatch_jobs():
        return {"message": "Success!"}, 200

    @requires_roles([UserRole.DRIVER])
    @app.route("/driver/jobs", methods=["GET"])
    def driver_jobs():
        return {"message": "Success!"}, 200

    @app.route("/")
    def main():
        return "Hello World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
