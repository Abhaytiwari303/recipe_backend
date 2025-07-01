from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can view, only logged-in users can post/edit/delete

    def perform_create(self, serializer):
        print("DEBUG: Creating recipe by user:", self.request.user)
        serializer.save(created_by=self.request.user)
