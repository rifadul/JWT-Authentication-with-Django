from rest_framework import serializers
from account.models import User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserModelSerializer(serializers.ModelSerializer):
    # we are writing this because we need to confirm password field and our registration request
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name', 'phone','password','password2', 'tc']
        extra_kwargs = {
            'password':{'write_only':True},
        }

# validating passowrd and confirm password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password dosen't match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('email','password')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name', 'phone')


class UserpasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password dosen't match")
        user.set_password(password)
        user.save()
        return attrs    



class SendPasswordResetEmailSerializer(serializer.Serializer):
    email = serializer.EmailField(max_length=255)
    class Meta:
        fields = ['email']

        def validate(self,attrs):
            email = attrs.get('email')
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
                return attrs
            else:
                raise ValidationError('You are not a Registered User')
