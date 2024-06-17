from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'role', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'role', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            name=validated_data.get('name'),
            role=validated_data.get('role'),
            email=validated_data.get('email')
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include 'phone_number' and 'password'")

        data['user'] = user
        return data


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        # Создайте новый refresh токен
        new_refresh = RefreshToken.for_user(refresh.user)
        new_refresh.set_jti()
        new_refresh.set_exp()
        new_refresh.set_iat()

        return {
            'access': str(refresh.access_token),
            'refresh': str(new_refresh),
        }