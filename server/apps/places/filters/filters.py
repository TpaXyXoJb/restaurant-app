import django_filters
from django_filters import rest_framework as filters
from drf_yasg.inspectors import CoreAPICompatInspector, NotHandled
from apps.places.models.restaurant import Restaurant
from apps.places.models.dish import Dish
from apps.places.models.ingredient import Ingredient


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    """
    Description for filter fields
    """

    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, filters.DjangoFilterBackend):
            result = super(DjangoFilterDescriptionInspector, self).get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    param.description = "Filter the returned list by {field_name}".format(field_name=param.name)
            return result
        return NotHandled


class RestaurantFilter(django_filters.FilterSet):
    """
    Filter for restaurants
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    cost_gte = django_filters.NumberFilter(field_name='avg_cost', lookup_expr='gte', label='Мин. средняя стоимость')
    cost_lte = django_filters.NumberFilter(field_name='avg_cost', lookup_expr='lt', label='Макс. средняя стоимость')
    cost_range = django_filters.RangeFilter(field_name='avg_cost', label='Диапазон стоимости')
    order_by = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('avg_cost', 'avg_cost')
        )
    )

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'cost_gte',
            'cost_lte',
            'cost_range',
            'order_by'
        ]


class DishFilter(django_filters.FilterSet):
    """
    Filter for dishes
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    calories_gte = django_filters.NumberFilter(field_name='total_calories', lookup_expr='gte',
                                               label='Мин. калорийность')
    calories_lte = django_filters.NumberFilter(field_name='total_calories', lookup_expr='lte',
                                               label='Макс. калорийность')
    calories_range = django_filters.RangeFilter(field_name='total_calories', label="Диапазон калорийности")
    cost_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Мин. средняя стоимость')
    cost_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Макс. средняя стоимость')
    cost_range = django_filters.RangeFilter(field_name='price', label='Диапазон стоимости')
    order_by = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('total_calories', 'total_calories'),
            ('avg_cost', 'avg_cost')
        )
    )

    class Meta:
        model = Dish
        fields = [
            'name',
            'restaurants',
            'ingredients',
            'calories_gte',
            'calories_lte',
            'calories_range',
            'cost_gte',
            'cost_lte',
            'cost_range',
            'order_by'
        ]


class IngredientFilter(django_filters.FilterSet):
    """
    Filter for ingredients
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    calories_gte = django_filters.NumberFilter(field_name='product_calorie', lookup_expr='gte',
                                               label='Мин. калорийность')
    calories_lte = django_filters.NumberFilter(field_name='product_calorie', lookup_expr='lte',
                                               label='Макс. калорийность')
    calories_range = django_filters.RangeFilter(field_name='product_calorie', label="Диапазон калорийности")
    order_by = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('product_calorie', 'product_calorie')
        )
    )

    class Meta:
        model = Ingredient
        fields = [
            'name',
            'calories_gte',
            'calories_lte',
            'calories_range',
            'order_by'
        ]
