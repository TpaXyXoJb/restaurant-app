from rest_framework import routers

from apps.users.viewsets import UserViewSet
from apps.places.viewsets.restaurant import RestaurantViewSet
from apps.places.viewsets.dish import DishViewSet
from apps.places.viewsets.ingredient import IngredientViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('restaurants', RestaurantViewSet, basename='restaurants')
router.register('dishes', DishViewSet, basename='dishes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
