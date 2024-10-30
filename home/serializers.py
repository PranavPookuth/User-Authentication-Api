from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import *
import uuid
import random
from django.core.mail import send_mail


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile_number', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        email = data.get('email')
        mobile_number = data.get('mobile_number')

        try:
            user = User.objects.get(email=email, mobile_number=mobile_number)
            if user.is_verified:
                raise serializers.ValidationError({
                    'email': 'User with this email is already verified.',
                    'mobile_number': 'User with this mobile number is already verified.',
                })
            else:
                # If user exists but is not verified, allow OTP regeneration
                self.context['existing_user'] = user
        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        if 'existing_user' in self.context:
            # User exists but not verified, regenerate OTP
            user = self.context['existing_user']
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            # Resend OTP via email
            send_mail(
                'OTP Verification',
                f'Your OTP is {otp}',
                'praveencodeedex@gmail.com',
                [user.email]
            )
            return user
        else:
            # New user, create account and generate OTP
            validated_data.pop('confirm_password')
            username = str(uuid.uuid4())[:8]

            user = User.objects.create_user(
                username=username,
                name=validated_data['name'],
                email=validated_data['email'],
                mobile_number=validated_data['mobile_number'],
                password=validated_data['password'],
                is_active=False
            )

            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            # Send OTP via email
            send_mail(
                'OTP Verification',
                f'Your OTP is {otp}',
                'praveencodeedex@gmail.com',
                [user.email]
            )

            return user


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Authenticate the user with email and password
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_verified:
            raise serializers.ValidationError("Email not verified.")

        # Store the user in the validated data for later use
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
   name=serializers.CharField(source='customer.customer_name',read_only=True)
   p_name=serializers.CharField(source='product.product_name',read_only=True)
   class Meta:
        model = Order
        fields = ['id','customer','product','quantity','order_date','name','p_name']


