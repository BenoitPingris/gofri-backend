from rest_framework import viewsets
from rest_framework import permissions

from .serializers import FoodSerializer
from .models import Food


class FoodView(viewsets.ModelViewSet):
    queryset = Food.objects.all().order_by('name')
    serializer_class = FoodSerializer

    #permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    permission_classes = [permissions.IsAuthenticated]


class FridgeView():
    pass
