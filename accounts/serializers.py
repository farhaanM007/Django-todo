from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User
from rest_framework.authtoken.models import Token 
from posts.serializers import PostSerializer

class SignupSerializer(serializers.ModelSerializer):

    email=serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=50)
    password=serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model=User
        fields=[ "username","password","email"]

    def validate(self, attrs):

        email_exists=User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError("Email  already Exists")
        return super().validate(attrs)
    
    def create(self, validated_data):

        password= validated_data.pop("password")

        user=super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user
    

class CurrentUserPostsSerializer(serializers.ModelSerializer):

    posts= serializers.HyperlinkedRelatedField(
        many=True,
        view_name="post_details",
        queryset=User.objects.all()
    )

    class Meta:
        model=User
        fields=['id','username','email','posts']
