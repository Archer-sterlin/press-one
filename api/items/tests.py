from django.test import TestCase
from django.utils import timezone
from items.models import Item
from items.serializers import ItemFormSerializer, ItemSerializer
from rest_framework import status
from rest_framework.test import APIClient


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="macbook pro", description="a really nice laptop.", price=299.99
        )

    def test_item_str_representation(self):
        """
        Test the __str__ method of the Item model.
        """
        expected_str = f"{self.item.id} - {self.item.name}"
        self.assertEqual(str(self.item), expected_str)

    def test_item_defaults(self):
        """
        Test the default values of the Item model.
        """
        new_item = Item.objects.create()
        self.assertIsNone(new_item.name)
        self.assertIsNone(new_item.description)
        self.assertIsNone(new_item.price)
        self.assertIsNotNone(new_item.created_at)
        self.assertIsNotNone(new_item.updated_at)

    def test_item_created_at_auto_now_add(self):
        """
        Test that created_at is set to the current time on creation.
        """
        now = timezone.now()
        self.assertLess(self.item.created_at, now)

    def test_item_updated_at_auto_now(self):
        """
        Test that updated_at is set to the current time on update.
        """
        initial_updated_at = self.item.updated_at
        self.item.save()
        self.assertLess(initial_updated_at, self.item.updated_at)


class ItemSerializerTest(TestCase):
    def setUp(self):
        self.sample_item_data = {
            "id": 1,
            "name": "Playstation 5",
            "description": "This is a really nice console.",
            "price": 319.99,
            "created_at": timezone.now(),
            "updated_at": timezone.now(),
        }

    def test_item_serializer_valid_data(self):
        serializer = ItemSerializer(data=self.sample_item_data)
        self.assertTrue(serializer.is_valid())


class ItemFormSerializerTest(TestCase):
    def setUp(self):
        self.sample_item_data = {
            "name": "LG TV",
            "description": "This is a has a really nice display.",
            "price": 199.99,
        }

    def test_item_form_serializer_valid_data(self):
        serializer = ItemFormSerializer(data=self.sample_item_data)
        self.assertTrue(serializer.is_valid())

    def test_item_form_serializer_empty_name(self):
        # Test the serializer with an empty 'name' field
        invalid_data = self.sample_item_data.copy()
        invalid_data["name"] = ""
        serializer = ItemFormSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    # def test_item_form_serializer_price(self):
    #     # Test the serializer with an empty 'name' field
    #     invalid_data = self.sample_item_data.copy()
    #     invalid_data["price"] = -2
    #     serializer = ItemFormSerializer(data=invalid_data)
    #     self.assertFalse(serializer.is_valid(raise_exception=False))
    #     self.assertIn("price", serializer.errors)


class ItemViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_data = {
            "name": "Test Item",
            "description": "Test Description",
            "price": 199.99,
        }
        self.url = "/api/v1/items/"

    def test_create_item(self):
        response = self.client.post(self.url, self.item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")

    def test_retrieve_item(self):
        item = Item.objects.create(name="Test Item", price=29.99)
        response = self.client.get(f"/api/v1/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"].get("name"), item.name)

    def test_update_item(self):
        item = Item.objects.create(name="Test Item", price=29.99)
        updated_data = {"name": "Updated Item", "price": 39.99}
        response = self.client.put(
            f"/api/v1/items/{item.id}/", updated_data, format="json"
        )  # Update the URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=item.id).name, "Updated Item")

    def test_delete_item(self):
        item = Item.objects.create(name="Test Item", price=29.99)
        response = self.client.delete(f"/api/v1/items/{item.id}/")  # Update the URL
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
