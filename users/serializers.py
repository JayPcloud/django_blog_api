from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class PublicUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(read_only=True,)
    password = serializers.CharField(write_only=True, required=False)
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail', many=False)
    old_password = serializers.CharField(write_only=True, required=False)
    
    
    def validate(self, data):
        request_method = self.context['request'].method
        password = data.get('password', None)
        if request_method == 'POST':
            if password == None:
                raise serializers.ValidationError({"info": "Please provide a password" })
        elif (request_method == 'PUT' or request_method == 'PATCH'):
            old_password = data.get('old_password', None)
            if password != None and old_password == None:
                raise serializers.ValidationError({"info" : "Please provide the old password."})
        return data

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')

        base_username = f'{first_name.lower()}_{last_name.lower()}'
        username = base_username
        suffix = 1

        while User.objects.filter(username=username).exists():
            username = f'{base_username}_{suffix}'
            suffix += 1
            
        if 'old_password' in validated_data:
            validated_data.pop('old_password')
            
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            **validated_data
        )
        user.set_password(password)
        user.save()

        return user

    
    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else: 
                    raise Exception("Old password is incorrect.")
                user.save()
        except Exception as err:
            raise serializers.ValidationError({"info":err})
        return super().update(instance, validated_data)

    class Meta():
        model=User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'password','old_password','profile']


class PrivateUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(read_only=True,)
    old_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail', many=False)
    
    
    def validate(self, data):
        request_method = self.context['request'].method
        password = data.get('password', None)
        if request_method == 'POST':
            if password == None:
                raise serializers.ValidationError({"info": "Please provide a password" })
        elif (request_method == 'PUT' or request_method == 'PATCH'):
            old_password = data.get('old_password', None)
            if password != None and old_password == None:
                raise serializers.ValidationError({"info" : "Please provide the old password."})
        return data

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User.objects.create(**validated_data)
    #     user.set_password(password)
    #     user.save()

    #     return user
    
    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else: 
                    raise Exception("Old password is incorrect.")
                user.save()
        except Exception as err:
            raise serializers.ValidationError({"info":err})
        return super().update(instance, validated_data)

    
    class Meta():
        model=User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name','password', 'old_password', 'profile']



class ProfileSerializer(serializers.ModelSerializer):
    
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', many=False)
    class Meta():
        model = Profile
        fields = ['url','id','image', 'user']
