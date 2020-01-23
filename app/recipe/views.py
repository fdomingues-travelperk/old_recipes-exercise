from rest_framework import viewsets, mixins

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """Retrieves the recipes and apply name filter if necessary"""
        name_filter = self.request.query_params.get('name')
        queryset = self.queryset
        if name_filter:
            queryset = queryset.filter(name__contains=name_filter)
        return queryset
