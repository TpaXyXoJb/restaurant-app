from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from apps.places.models.restaurant import Restaurant
from apps.places.models.dish import Dish
from apps.places.models.ingredient import Ingredient


class UserActionsTests(APITestCase):
    def setUp(self):
        self.user = {'username': 'test_user', 'password': 'test_password'}
        self.wrong_user = {'username': 'wrong_user', 'password': 'wrong_password'}
        self.users_url = reverse('users-list')
        self.token_url = reverse('tokens')

        self.users_count = User.objects.count()
        self.tokens_count = Token.objects.count()

    def test_creating_user_returns_token(self):
        """
        Test shows user creation, which returns token and compare with user's token
        :return:
        """
        response = self.client.post(self.users_url, self.user)
        token = User.objects.get(username=self.user['username']).auth_token

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.users_count + 1)

        self.assertTrue('token' in response.data)
        self.assertEqual(token.key, response.data['token'])

    def test_api_auth_token_returns_correct_token(self):
        """
        Test shows user creation, comparing from the list of tokens with the user's token
        :return:
        """
        self.client.post(self.users_url, self.user)
        response = self.client.post(self.token_url, self.user)
        token = User.objects.get(username=self.user['username']).auth_token

        self.assertTrue('token' in response.data)

        self.assertEqual(type(response.data['token']), str)
        self.assertEqual(token.key, response.data['token'])

    def test_api_token_fails(self):
        """
        Test shows that token does not match with the user's token
        :return:
        """
        response = self.client.post(self.token_url, self.wrong_user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RestaurantActionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testusername', password='testuserpass')
        self.owner = User.objects.create(username='testowner', password='testownerpass')

        self.users_token = Token.objects.create(user=self.user)
        self.owners_token = Token.objects.create(user=self.owner)

        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            name='testrestaurant',
            opening_time='09:00',
            closing_time='12:00',
            address='Москва Кунцевская улица 13/6'
        )
        self.restaurant_count = Restaurant.objects.count()
        self.restaurant_detail_url = reverse('restaurants-detail', args=(self.restaurant.id,))
        self.restaurants_list_url = reverse('restaurants-list')

        self.test_restaurant = {
            'name': 'testrestaurant',
            'opening_time': '09:00',
            'closing_time': '12:00',
            'address': 'Москва Кунцевская улица 13/6'
        }

    def test_restaurant_list_success(self):
        """
        Test that the restaurants list endpoint successful
        :return:
        """
        self.client.credentials()
        response = self.client.get(self.restaurants_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_detail_success(self):
        """
        Test that the restaurant detail endpoint successful
        :return:
        """
        response = self.client.get(self.restaurant_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_post_success(self):
        """
        Test shows the successful restaurant post request
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.owners_token.key}')
        response = self.client.post(self.restaurants_list_url, self.test_restaurant)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), self.restaurant_count + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('address' in response.data)
        self.assertTrue('latitude' in response.data)
        self.assertTrue('longitude' in response.data)

        self.assertEqual(self.test_restaurant['name'], response.data['name'])
        self.assertEqual(self.owner.id, response.data['owner'])

    def test_restaurant_post_unauthorized(self):
        """
        Test that an unauthorized user can't create a restaurant
        :return:
        """
        self.client.credentials()
        response = self.client.post(self.restaurants_list_url, self.test_restaurant)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_update_allowed(self):
        """
        Test that the restaurant can be updated successfully by the owner
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.owners_token}")
        response = self.client.put(self.restaurant_detail_url, self.test_restaurant)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_update_unauthorized(self):
        """
        Test that an unauthorized user can't update the restaurant
        :return:
        """
        self.client.credentials()
        response = self.client.put(self.restaurant_detail_url, self.test_restaurant)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_update_not_owner(self):
        """
        Test that an authorized user, except owner, can't update the restaurant
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.users_token}")
        response = self.client.put(self.restaurant_detail_url, self.test_restaurant)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_delete_allowed(self):
        """
        Test that the restaurant can be deleted successfully by the owner
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.owners_token}")
        response = self.client.delete(self.restaurant_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restaurant_delete_unauthorized(self):
        """
        Test that an unauthorized user can't delete the restaurant
        :return:
        """
        self.client.credentials()
        response = self.client.delete(self.restaurant_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_delete_not_owner(self):
        """
        Test that an authorized user, except owner, can't delete the restaurant
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.users_token}")
        response = self.client.delete(self.restaurant_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DishActionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testusername', password='testuserpass')
        self.owner = User.objects.create(username='testowner', password='testownerpass')

        self.users_token = Token.objects.create(user=self.user)
        self.owners_token = Token.objects.create(user=self.owner)

        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            name='testrestaurant',
            opening_time='09:00',
            closing_time='12:00',
            address='Москва Кунцевская улица 13/6'
        )
        self.dish = Dish.objects.create(
            name='testdish',
            price='1560.23',
            restaurants=self.restaurant
        )
        self.dish.ingredients.add(32, 12, 87)

        self.dish_count = Dish.objects.count()

        self.test_dish = {
            'name': 'testdish',
            'price': '1510.00',
            'ingredients': [5, 63, 199],
            'restaurants': self.restaurant.id
        }
        self.dish_detail_url = reverse('dishes-detail', args=(self.dish.id,))
        self.dish_list_url = reverse('dishes-list')

    def test_dish_list_success(self):
        """
        Test that the dish list endpoint successful
        :return:
        """
        response = self.client.get(self.dish_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dish_detail_success(self):
        """
        Test that the dish detail endpoint successful
        :return:
        """
        response = self.client.get(self.dish_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dish_post_success(self):
        """
        Test shows the successful dish post request
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.owners_token}')
        response = self.client.post(self.dish_list_url, self.test_dish)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), self.dish_count + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('total_calories' in response.data)
        self.assertTrue('price' in response.data)
        self.assertTrue('ingredients' in response.data)
        self.assertTrue('restaurants' in response.data)

        self.assertEqual(self.test_dish['name'], response.data['name'])

    def test_dish_post_unauthorized(self):
        """
        Test that an unauthorized user can't create dish
        :return:
        """
        self.client.credentials()
        response = self.client.post(self.dish_list_url, self.test_dish)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dish_update_allowed(self):
        """
        Test that the dish can be updated successfully by the owner
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.owners_token}')
        response = self.client.put(self.dish_detail_url, self.test_dish)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dish_update_unauthorized(self):
        """
        Test that an unauthorized user can't update the dish
        :return:
        """
        self.client.credentials()
        response = self.client.put(self.dish_detail_url, self.test_dish)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dish_update_not_owner(self):
        """
        Test that an authorized user, except owner, can't update the dish
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.users_token}')
        response = self.client.put(self.dish_detail_url, self.test_dish)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dish_delete_allowed(self):
        """
        Test that the dish can be deleted successfully by the owner
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.owners_token}')
        response = self.client.delete(self.dish_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_dish_delete_unauthorized(self):
        """
        Test that an unauthorized user can't delete the dish
        :return:
        """
        self.client.credentials()
        response = self.client.delete(self.dish_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dish_delete_not_owner(self):
        """
        Test that an authorized user, except owner, can't delete the dish
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.users_token}')
        response = self.client.delete(self.dish_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IngredientActionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testuserpass')
        self.users_token = Token.objects.create(user=self.user)

        self.ingredient = Ingredient.objects.create(
            name='testingredient',
            product_calorie='222.02'
        )

        self.test_ingredient = {
            'name': 'test_ingredient',
            'product_calorie': '111.01'
        }

        self.ingredient_detail_url = reverse('ingredients-detail', args={self.ingredient.id, })
        self.ingredient_list_url = reverse('ingredients-list')

    def test_ingredient_list_success(self):
        """
        Test that the ingredient list endpoint successful
        :return:
        """
        response = self.client.get(self.ingredient_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredient_detail_success(self):
        """
        Test that the ingredient detail endpoint successful
        :return:
        """
        response = self.client.get(self.ingredient_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredient_post_not_allowed(self):
        """
        Test that the ingredient can't be added by the user
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.users_token}')
        response = self.client.post(self.ingredient_list_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ingredient_post_unauthorized(self):
        """
        Test that the ingredient can't be added by the unauthorized user
        :return:
        """
        self.client.credentials()
        response = self.client.post(self.ingredient_list_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredient_update_not_allowed(self):
        """
        Test that the ingredient can't be updated by the user
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.users_token}')
        response = self.client.put(self.ingredient_detail_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ingredient_update_unauthorized(self):
        """
        Test that the ingredient can't be updated by the unauthorized user
        :return:
        """
        self.client.credentials()
        response = self.client.put(self.ingredient_detail_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredient_delete_not_allowed(self):
        """
        Test that the ingredient can't be deleted by the user
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.users_token}')
        response = self.client.delete(self.ingredient_detail_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ingredient_delete_unauthorized(self):
        """
        Test that the ingredient can't be deleted by the unauthorized user
        :return:
        """
        self.client.credentials()
        response = self.client.delete(self.ingredient_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
