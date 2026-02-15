from enum import Enum
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import hashlib
from ..auth.jwt_token import jwt_encode


class UserRole(Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"
    DRIVER = "driver"


class AccountStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class DriverStatus(Enum):
    AVAILABLE = "available"
    ON_JOB = "on_job"
    OFFLINE = "offline"


class User:
    def __init__(
        self,
        email: str,
        password: str,
        role: UserRole | None = None,
        active: AccountStatus = AccountStatus.ACTIVE,
    ):
        self.id = str(uuid4())[:7]
        self.email = email
        self.password_hash = User.generate_password_hash(password)
        self.role: UserRole = role
        self.active = active
        self.created_at = datetime.now(tz=timezone.utc)
        self.updated_at = datetime.now(tz=timezone.utc)

    def _update(self):
        self.updated_at = datetime.now(tz=timezone.utc)

    @staticmethod
    def generate_password_hash(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, password):
        return User.generate_password_hash(password) == self.password_hash

    def generate_token(self):
        return jwt_encode(
            {
                "sub": self.id,
                "role": self.role.value,
                "iat": int(datetime.now(tz=timezone.utc).timestamp()),
                "exp": int(
                    (datetime.now(tz=timezone.utc) + timedelta(hours=1)).timestamp()
                ),
            }
        )

    def update_email(self, new_email):
        self.email = new_email
        self._update()

    def deactivate(self):
        self.active = False
        self._update()

    def reactivate(self):
        self.active = True
        self._update()

    def update_role(self, new_role):
        self.role = new_role
        self._update()


class Driver(User):
    def __init__(self, email: str, password: str, active: bool = True):
        super().__init__(email, password, UserRole.DRIVER, active)

        self.full_name = ""
        self.phone = ""
        self.status = DriverStatus.OFFLINE
