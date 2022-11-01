from core.models import Genre, Movie
import django_filters
from django import forms

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='startswith', label='')
    # genres = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Movie
        fields = ['genres','title',]