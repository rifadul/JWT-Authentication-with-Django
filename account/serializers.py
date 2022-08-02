from rest_framework import serializers
from account.models import User

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


class UserpasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ('password','password2')
        def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            user = self.context.get('user')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password dosen't match")
            user.set_password(password)
            user.save()
            return attrs