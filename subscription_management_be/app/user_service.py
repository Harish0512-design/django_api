import re
from typing import Any
from app.models import Profile
from app.password_manager import PasswordManager
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth.models import User
from random import randint
from app.user_exceptions import (
    InvalidEmailException,
    InvalidFirstNameException,
    InvalidFullNameException,
    InvalidLastNameException,
    InvalidPasswordException,
    InvalidPhoneNumberException,
    EmailAlreadyExistsException,
    InvalidIsActiveException,
)
from app.common_exceptions import ValidationError, InternalServerError


class UserService:
    @staticmethod
    def add_user(request_payload_data: dict):
        try:
            validation_service = UserValidationService(request_payload_data)
            validation_service.validate()
            data = validation_service.get_validated_data()
            response = UserDBService.save_user(**data)
            return response
        except Exception as ex:
            raise ex

    @staticmethod
    def get_users():
        try:
            response = UserDBService.get_users()
            return response
        except Exception as ex:
            raise ex


class UserValidationService:

    def __init__(self, data):
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.phonenumber = data.get("phonenumber")
        self.is_active = data.get("is_active")
        self.domains = ["gmail.com", "yahoo.com", "outlook.com"]
        self.full_name = None
        self.username = None

    @staticmethod
    def get_required_fields():
        required_fields = ("full_name", "email", "password")
        return required_fields

    @staticmethod
    def get_all_fields():
        fields = ("full_name", "email", "password", "phone_number", "is_active")
        return fields

    def validate_email(self):
        """
        Validates the email Id with given domain

        Rules:
        1. email should contain only 1 @ special char

        """
        if not isinstance(self.email, str):
            raise InvalidEmailException("Email field should be a string.")
        if not self.email:
            raise InvalidEmailException("Required Email (email)")
        if "@" not in self.email or self.email.count("@") != 1:
            raise InvalidEmailException("Invalid Email Format")
        extracted_domain = self.email.split("@")[-1]
        if extracted_domain not in self.domains:
            raise InvalidEmailException("Invalid Domain")

        return

    def validate_first_name(self):
        """
        Validates first Name of the User

        Rules:
        1. First Name should have atleast 3 characters and not more than 10 chars
        2. Contains only alphabets
        3. First letter should be capital (Convert to Upper if Required)

        """

        if not self.first_name:
            raise InvalidFirstNameException("FirstName requried (first_name)")

        if not isinstance(self.first_name, str):
            raise InvalidFirstNameException("FirstName field should be a string.")

        self.first_name: str = self.first_name.strip()

        if not len(self.first_name) >= 3 and len(self.first_name) <= 20:
            raise InvalidFirstNameException(
                "FirstName should be greater than 3 chars and less than 20 chars",
            )
        if not self.first_name.isalpha():
            raise InvalidFirstNameException("FirstName should contain only alphabets")

        return

    def validate_last_name(self):
        """
        Validates last Name of the User

        Rules:
        1. Last Name should have atleast 1 character and not more than 20 chars
        2. Contains only alphabets
        3. First letter should be capital (Convert to Upper if Required)

        """

        if not self.last_name:
            raise InvalidLastNameException("LastName required (last_name)")

        if not isinstance(self.last_name, str):
            raise InvalidLastNameException("LastName field should be a string.")

        self.last_name: str = self.last_name.strip()

        if not len(self.last_name) >= 1 and len(self.last_name) <= 20:
            raise InvalidLastNameException(
                "LastName should be atleast 1 char and less than 20 chars"
            )
        if not self.last_name.isalpha():
            raise InvalidLastNameException("LastName should contain only alphabets")

        return

    def validate_password(self):
        """
        Validates password as per the rules

        Rules:
        1. Password should contain atleast 8 chars and not more than 15 characters
        2. Password should contain alphanumeric and also special chars (!@#$%^&*())
        3. Password should contain combination of lower case and upper case letters

        """
        if not isinstance(self.password, str) or not self.password.strip():
            raise InvalidPasswordException("Password cannot be empty.")

        # Length Check: 8 to 15 characters
        if not (8 <= len(self.password) <= 15):
            raise InvalidPasswordException(
                "Password must be between 8 and 15 characters long."
            )

        # At least one uppercase letter
        if not re.search(r"[A-Z]", self.password):
            raise InvalidPasswordException(
                "Password must contain at least one uppercase letter."
            )

        # At least one lowercase letter
        if not re.search(r"[a-z]", self.password):
            raise InvalidPasswordException(
                "Password must contain at least one lowercase letter."
            )

        # At least one digit
        if not re.search(r"\d", self.password):
            raise InvalidPasswordException("Password must contain at least one digit.")

        # At least one special character (!@#$%^&*())
        if not re.search(r"[!@#$%^&*()]", self.password):
            raise InvalidPasswordException(
                "Password must contain at least one special character (!@#$%^&*())."
            )

        return

    def validate_phone_number(self):
        """
        Validates the phone number provided by the user.

        Rules:
        - Must contain only numeric digits (0-9).
        - Should not contain any decimal values.
        - Must be exactly 10 digits long.
        - The first digit must be (6, 7, 8, or 9).
        - Should not contain more than 5 consecutive zeros.
        - Should not be a single repeated digit (e.g., 1111111111).
        - Should not contain spaces, special characters, or alphabets.

        """
        if self.phonenumber:
            if not isinstance(self.phonenumber, str):
                raise InvalidPhoneNumberException("Phone number should be string.")

            self.phonenumber = self.phonenumber.strip()

            # Ensure the number is exactly 10 digits
            if not re.fullmatch(r"\d{10}", self.phonenumber):
                raise InvalidPhoneNumberException(
                    "Phone number must be exactly 10 digits long and contain only numbers."
                )

            # First digit should be 6, 7, 8, or 9
            if self.phonenumber[0] not in "6789":
                raise InvalidPhoneNumberException(
                    "Phone number must start with 6, 7, 8, or 9."
                )

            # Should not contain more than 5 consecutive zeros
            if "000000" in self.phonenumber:
                raise InvalidPhoneNumberException(
                    "Phone number should not contain more than 5 consecutive zeros."
                )

            # Should not be a single repeated digit (e.g., 1111111111)
            if len(set(self.phonenumber)) == 1:
                raise InvalidPhoneNumberException(
                    "Phone number should not be a single repeated digit."
                )

            return

    def validate_is_active(self):
        if self.is_active:
            if not isinstance(self.is_active, bool):
                raise InvalidIsActiveException(
                    "is_active field should be a boolean (True/False)"
                )
            return

    def _generate_full_name(self):
        """
        Returns the full name after validating first and last names.

        Returns:
            str: Full name if valid, otherwise an error message.
        """
        try:
            self.validate_first_name()
            self.validate_last_name()

            self.full_name = self.first_name + " " + self.last_name
            self.full_name = self.full_name.title()

        except InvalidFirstNameException as ex:
            raise InvalidFullNameException(str(ex))
        except InvalidLastNameException as ex:
            raise InvalidFullNameException(str(ex))

    def validate(self):
        try:
            self.validate_first_name()
            self.validate_last_name()
            self.validate_password()
            self.validate_email()
            self.validate_phone_number()
            self.validate_is_active()
        except Exception as ex:
            raise ValidationError(ex)

    def get_validated_data(self):
        self._generate_full_name()
        self._generate_username()
        return {
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "password": self.password,
            "phonenumber": self.phonenumber,
            "is_active": self.is_active,
        }

    def _generate_username(self):
        self.username = (
            self.first_name + "_" + self.last_name + "-" + str(randint(11, 1000))
        )


class UserDBService:
    @staticmethod
    def check_email_exists(email: str):
        """
        Checks whether the email is present in the Profile Table or not

        Args:
            email (str): Email of the user

        Return:
            msg, bool (Tuple): Returns a valid/error message and True/False value.
        """
        if Profile.objects.filter(email=email).exists():
            raise EmailAlreadyExistsException("Email Already Exists.")
        return

    @staticmethod
    def save_user(
        username: str,
        full_name: str,
        email: str,
        password: str,
        phonenumber: str | None = None,
        is_active: bool | None = None,
    ) -> dict:
        print(full_name)
        try:
            UserDBService.check_email_exists(email)
            user = UserDBService._create_user_for_user_model(
                username=username, password=password
            )
            if user:
                with transaction.atomic():
                    profile = Profile()
                    profile.user = user
                    profile.full_name = full_name
                    profile.email = email
                    profile.password_hash = PasswordManager.hash_password(
                        password=password
                    )
                    if is_active is not None:
                        profile.is_active = is_active
                    if phonenumber is not None:
                        profile.phone_number = phonenumber

                    profile.save()
                    data = {
                        "profile_id": profile.pk,
                        "full_name": profile.full_name,
                        "email": profile.email,
                        "username": username,
                    }
                    return {"message": "User Created successfully.", "data": data}
            else:
                return {
                    "message": "Something Went wrong, Please try again after few minutes."
                }
        except EmailAlreadyExistsException as ex:
            raise ex
        except IntegrityError as ex:
            raise InternalServerError(ex)

    @staticmethod
    def _create_user_for_user_model(username, password):
        user, created = User.objects.get_or_create(username=username, password=password)
        if created:
            return user
        else:
            return False

    @staticmethod
    def get_users():
        user_profiles = []
        profiles = Profile.objects.values_list("id", "full_name", "email", "user")
        for profile in profiles:
            user = profile[3]
            username = User.objects.get(id=user).username
            user_profiles.append(
                {
                    "profile_id": profile[0],
                    "full_name": profile[1],
                    "email": profile[2],
                    "username": username,
                }
            )

        print(user_profiles)
        return {
            "message": "User profiles retrieved successfully.",
            "no_of_users": len(user_profiles),
            "users": user_profiles,
        }
