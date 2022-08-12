from movies import models, serializer
from rest_framework import generics
from movies.base.classes import Pagination
from movies.models import Filmwork

class MoviesListApi(generics.ListAPIView):
    serializer_class = serializer.FilmworkSerializer
    pagination_class = Pagination
    lookup_field = 'id'

    def get_queryset(self):
        return models.Filmwork.objects.all()

class MoviesDetailApi(generics.RetrieveAPIView):

    serializer_class = serializer.FilmworkDetailSerializer
    queryset = Filmwork.objects.all()

