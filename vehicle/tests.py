from rest_framework import status
from rest_framework.test import APITestCase

from vehicle.models import Car


class VehicletestCase(APITestCase):

    def setUp(self):
        pass

    def test_create_car(self):
        """Тестирование создания машины"""
        data={
            "title":"Test",
            "description": "Test"
        }
        responce = self.client.post(
            '/cars/',
            data
        )
        # print(responce.json())
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(responce.json(), {'id': 1, 'mileage': [], 'title': 'Test', 'description': 'Test', 'owner': None})
        self.assertTrue(Car.objects.all().exists())

    def test_list_car(self):
        Car.objects.create(
            title="list_test",
            description="list_test"
        )
        """Тестирование вывода списка машин"""
        responce = self.client.get("/cars/")

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.json(),
                         [{'id': 2, 'mileage': [], 'title': 'list_test', 'description': 'list_test', 'owner': None}])




