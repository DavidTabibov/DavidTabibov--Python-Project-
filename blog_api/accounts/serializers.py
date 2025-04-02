from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    # Adding a second field for password confirmation
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        # We'll use username, email, password and password2 for registration
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        # Ensure the two passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove the confirmation field before creating the user
        validated_data.pop('password2')
        # Use Django's built-in create_user method which handles password hashing
        user = User.objects.create_user(**validated_data)
        return user
