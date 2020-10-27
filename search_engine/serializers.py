from rest_framework import serializers
from search_engine.models import MovieDetails

class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetails
        fields = '__all__'