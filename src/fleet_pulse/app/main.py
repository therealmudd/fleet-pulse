from flask import Flask, app, request, jsonify
from ..auth.decorators import requires_roles
from ..models.user import Driver, User, UserRole

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

    @app.route("/admin/drivers", methods=["POST"])
    @requires_roles([UserRole.ADMIN])
    def create_driver():
        if not request.is_json:
            return jsonify({"message": "Body must be json"}), 400

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        phone = data.get("phone")

        if email is None or password is None:
            return {"message": "Malformed request"}, 400

        user = get_user(email)
        if user:
            return {"message": "User already exists"}, 409

        driver = Driver(email, password)
        driver.full_name = full_name
        driver.phone = phone
        users.append(driver)

        return {
            "message": "Driver created successfully",
            "details": {
                "id": driver.id,
                "full_name": driver.full_name,
                "email": driver.email,
                "status": "ACTIVE",
            },
        }, 201

    @app.route("/admin/health", methods=["GET"])
    @requires_roles([UserRole.ADMIN])
    def admin_health():
        return {"message": "Success!"}, 200

    @app.route("/dispatch/jobs", methods=["GET"])
    @requires_roles([UserRole.ADMIN, UserRole.DISPATCHER])
    def dispatch_jobs():
        return {"message": "Success!"}, 200

    @app.route("/driver/jobs", methods=["GET"])
    @requires_roles([UserRole.DRIVER])
    def driver_jobs():
        return {"message": "Success!"}, 200

    @app.route("/")
    def main():
        return "Hello World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
