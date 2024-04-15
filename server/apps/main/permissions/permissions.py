from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Custom permission to allow only owners of an object to edit it
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user == obj.owner
        )


class IsPlaceOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Custom permission to allow only owners of the restaurant to add or edit the dish
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        restaurant_id = obj.restaurants.id
        return bool(
            request.method in SAFE_METHODS or
            request.user.restaurants.filter(id=restaurant_id).exists()
        )
