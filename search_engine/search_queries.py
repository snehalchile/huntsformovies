from search_engine.models import MovieDetails
from googlesearch import search 

class Search(object):
    def __init__(self, query_string=None, universe=None, user_id=None):
        if query_string is None:
            query_string = ""
     
        self.universe = universe

        if query_string:
            self.query_string = query_string.lower()

    def show_google_links(self):
        search_string = self.query_string + ' movie'
        search_links = [link for link in search(search_string, tld="com", num=10, stop=10, pause=2)]
        return search_links

    def default_movies(self):
        ''' Allowing default search for top score movies and popular movies '''
        movie_data = []
        top_result = {}
        top_result['top_scored_movies'] = list(MovieDetails.objects.order_by('-imdb_score').values('imdb_score', 'name'))[:10]
        top_result['popular_movies'] = list(MovieDetails.objects.order_by('-popularity_99').values('popularity_99', 'name'))[:10]
        movie_data.append(top_result)
        return movie_data

    def get_query_result(self):
        result = {}
        movie_data = []
        if self.universe == 'name':
            movie_data = list(MovieDetails.objects.filter(name__icontains=self.query_string).values('popularity_99','director','genre','imdb_score','name'))[:10]
        elif self.universe == 'director':
            movie_data = list(MovieDetails.objects.filter(director__icontains=self.query_string).values('popularity_99','director','genre','imdb_score','name'))[:10]
        else:
            ''' If universe not given, Fetch the data by movie names '''
            movie_data = list(MovieDetails.objects.filter(name__icontains=self.query_string).values('popularity_99','director','genre','imdb_score','name'))[:10]

        if len(movie_data) > 0:
            result['data'] = movie_data
        else:
            ''' Since having less data show google links where user can get data '''
            result['search_links'] = self.show_google_links()
        result['query'] = self.query_string
        return result
 

