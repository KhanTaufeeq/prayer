from django.shortcuts import render
# from django.core import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import validators
# Create your views here.

email_validator = validators.CustomEmailValidator()
username_validator = validators.CustomUserNameValidator()
name_validator = validators.CustomNameValidator()
password_validator = validators.CustomPasswordValidator()


@api_view(['POST'])
def register(request):

    user_data = request.data
    if user_data:
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')
    else:
        return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)

    try:
        email = email_validator.validate_email(email)
        username = username_validator.validate_username(username)
        first_name = name_validator.validate_name(first_name)
        last_name = name_validator.validate_name(last_name)
        password = password_validator.validate_password(password)
    except ValidationError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response("There is something wrong", str(e))
    
    try:
        User = get_user_model()
        user = User.objects.create_user(username,email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response("The user has been registered successfully", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
