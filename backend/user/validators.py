import re
from rest_framework.exceptions import ValidationError 
from django.core.validators import EmailValidator 


class CustomEmailValidator():
    """Customised email validation"""

    def __init__(self):
        self.email_validation = EmailValidator()

    
    def _validate_format(self,email):
        try:
            self.email_validation(email)
        except ValidationError:
            raise ValidationError('Invalid email format')


    def _validate_length(self, email):
        email = email.strip()

        if len(email) > 254:
            raise ValidationError('Email too long')
        
        local_part, domain_part = email.split('@')

        if len(local_part) > 64:
            raise ValidationError("Local part of email is too long")
        
        if len(domain_part) > 253:
            raise ValidationError("Domain part of email is too long")
        
    
    def validate_email(self, email):

        email = email.lower().strip()

        self._validate_format(email)
        self._validate_length(email)

        return email
    

class CustomUserNameValidator():
    """
    Validate a username to ensure it contains
    - At least one uppercase letter
    - At least one lowercase letter
    - At least a digit
    - No spaces allowed
    """

    def _validate_length(self, username):
        """validate username length"""
        if len(username) < 4 or len(username) > 20:
            raise ValidationError("username must be between 4 and 20 characters long")
        
    def _validate_format(self, username):
        pattern = r"^(?=.*[a-z])(?=.*\d)(?!.*\s).+$"
        if not re.match(pattern, username):
            raise ValidationError("Username does not match the given pattern")

    
    def validate_username(self, username):
        # username = username.strip()
        self._validate_format(username)
        self._validate_length(username)

        return username
    

class CustomNameValidator():
    """
    Validate user's first and last name
    """

    def _validate_length(self, name:str):
        """validate user's name's length"""
        if len(name) > 30:
            raise ValidationError("Name cannot exceed length of 30 characters")
        
    def _validate_format(self, name:str):
        """Validate user's name's format"""
        if not name.isalpha():
            raise ValidationError("Name cannot have characters other than alphabets")
        
    def validate_name(self, name:str):
        name = name.strip()

        self._validate_format(name)
        self._validate_length(name)

        return name
    

class CustomPasswordValidator():
        """
        Validate a password to ensure it contains
        - At least one uppercase letter
        - At least one lowercase letter
        - At least a digit
        - At least a special character
        - No spaces allowed
        """

        def _validate_length(self, password):
            """validate password length"""
            if len(password) < 6 or len(password) > 20:
                raise ValidationError("Password must be between 6 and 20 characters long")
            
        def _validate_format(self, password):
            pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z\s])(?!.*\s).+$"
            if not re.match(pattern, password):
                raise ValidationError("Password does not match the given pattern")
        
        def validate_password(self, password):
            self._validate_format(password)
            self._validate_length(password)

            return password
