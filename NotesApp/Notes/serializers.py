from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, NoteHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class NoteSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(NoteSerializer, self).__init__(*args, **kwargs)
        if self.context.get('exclude_user_field'):
            self.fields.pop('user', None)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'user']
        
class NoteHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NoteHistory
        fields = ['id', 'title', 'content', 'updated_at']