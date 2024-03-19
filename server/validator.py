from mongoengine import Document, StringField

class NameValidator(Document):
    name = StringField(required=True, min_length=3, max_length=32)

class PasswordValidator(Document):
    regexp_password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,32}$"
    password = StringField(regex=regexp_password_pattern, required=True)