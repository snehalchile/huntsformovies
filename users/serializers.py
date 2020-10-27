from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import AppUser

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=AppUser.objects.all(), message='E-mail ID already registered')]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = AppUser.objects.create_user(validated_data.pop('email'), validated_data.pop('password'), **validated_data)
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    class Meta:
        model = AppUser
        fields = ('email', 'password','first_name','last_name','is_agreed','date_joined')

class AdminUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=AppUser.objects.all(), message='E-mail ID already registered')]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = AppUser.objects.create_superuser(validated_data.pop('email'), validated_data.pop('password'), **validated_data)
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    class Meta:
        model = AppUser
        fields = ('email', 'password','first_name','last_name','date_joined')
