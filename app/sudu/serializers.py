from django.contrib.auth.models import User, Group
from cinema.models import Festival, Film
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FestivalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Festival
        fields = ['name', 'month_occurence', 'is_african', 'country']


class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = ['name']
