from core.models import Movie
import django_filters

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='startswith', label='')
    class Meta:
        model = Movie
        fields = ['title']