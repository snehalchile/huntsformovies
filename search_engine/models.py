from django.db import models

# Create your models here.

class MovieDetails(models.Model):
	id = models.AutoField(primary_key=True)
	popularity_99 = models.IntegerField(blank=True, null=True)
	director = models.CharField(max_length=200, blank=True, null=True)
	genre = models.TextField(blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	imdb_score = models.FloatField(null=False, default=0.0)
	class Meta:
		managed = False
		db_table = 'movie_details'
