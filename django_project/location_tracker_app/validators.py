from rest_framework import serializers


def validate_password(password):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    # if not any(char.isdigit() for char in password):
    #     raise serializers.ValidationError('Password must contain digits')
    # if not any(char.isalpha() for char in password):
    #     raise serializers.ValidationError('Password must contain alphabets')
    # if not any(char in special_characters for char in password):
    #     raise serializers.ValidationError('Password must contain special characters')
    return password
