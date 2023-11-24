import logging

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from api.utils.base import BaseViewSet

from .models import Item
from .serializers import ItemFormSerializer, ItemSerializer

logger = logging.getLogger("items")


class ItemViewSet(BaseViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    serializer_form_class = ItemFormSerializer
    filter_fields = ["id", "name", "price"]
    search_fields = ["id", "name", "price"]

    def get_queryset(self):
        self.queryset = self.price_filtering(
            self.request.GET.get("price_from"),
            self.request.GET.get("price_to"),
            self.queryset,
        )
        return self.queryset.order_by("-pk")

    def get_object(self):
        return get_object_or_404(Item, id=self.kwargs.get("pk"))

    swagger_auto_schema(
        operation_summary="List all items",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="item id",
            ),
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Item name",
            ),
            openapi.Parameter(
                "price_from",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Item sales price from",
            ),
            openapi.Parameter(
                "price_to",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Item sales price to",
            ),
            openapi.Parameter(
                "price",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Item price",
            ),
        ],
    )

    def list(self, request, *args, **kwargs):
        context = {"status": status.HTTP_200_OK}

        try:
            logger.info(f"Fetching all items")
            paginate = self.get_paginated_data(
                queryset=self.get_list(self.get_queryset()),
                serializer_class=self.serializer_class,
            )
            context.update({"status": status.HTTP_200_OK, "data": paginate})
        except Exception as ex:
            logger.error(f"Error fetching all items due to {str(ex)}")
            context.update({"status": status.HTTP_400_BAD_REQUEST, "message": str(ex)})
        return Response(context, status=context["status"])

    @swagger_auto_schema(
        operation_description="Retrieve item details",
        operation_summary="Retrieve item details",
    )
    def retrieve(self, requests, *args, **kwargs):
        context = {"status": status.HTTP_200_OK}
        try:
            context.update({"data": self.serializer_class(self.get_object()).data})
        except Exception as ex:
            context.update({"status": status.HTTP_400_BAD_REQUEST, "message": str(ex)})
        return Response(context, status=context["status"])

    @swagger_auto_schema(
        operation_description="Delete item",
        operation_summary="Delete item",
    )
    def destroy(self, requests, *args, **kwargs):
        context = {"status": status.HTTP_204_NO_CONTENT}
        try:
            instance = self.get_object()
            instance.delete()
            context.update({"message": "Item deleted successfully"})
        except Exception as ex:
            context.update({"status": status.HTTP_400_BAD_REQUEST, "message": str(ex)})
        return Response(context, status=context["status"])

    @swagger_auto_schema(
        operation_summary="Add new Item", request_body=ItemFormSerializer
    )
    def create(self, request, *args, **kwargs):
        """
        This method handles creating of new item
        """
        context = {"status": status.HTTP_201_CREATED}
        try:
            data = self.get_data(request)
            serializer = self.serializer_form_class(data=data)

            if serializer.is_valid():
                instance = serializer.create(serializer.validated_data)
                context.update({"data": self.serializer_class(instance).data})
            else:
                context.update(
                    {
                        "errors": self.error_message_formatter(serializer.errors),
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                )
        except Exception as ex:
            context.update({"status": status.HTTP_400_BAD_REQUEST, "message": str(ex)})
        return Response(context, status=context["status"])

    @swagger_auto_schema(
        operation_summary="Update item", request_body=ItemFormSerializer
    )
    def update(self, request, *args, **kwargs):
        """
        This method handle updating item information
        """
        context = {"status": status.HTTP_200_OK}
        try:
            data = self.get_data(request)
            instance = self.get_object()
            serializer = self.serializer_form_class(data=data, instance=instance)
            if serializer.is_valid():
                _ = serializer.update(instance, serializer.validated_data)
                context.update(
                    {
                        "data": self.serializer_class(self.get_object()).data,
                        "status": status.HTTP_200_OK,
                    }
                )
            else:
                context.update(
                    {
                        "errors": self.error_message_formatter(serializer.errors),
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                )
        except Exception as ex:
            context.update({"status": status.HTTP_400_BAD_REQUEST, "message": str(ex)})
        return Response(context, status=context["status"])
