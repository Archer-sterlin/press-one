from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ViewSet

from .pagination import CustomPaginator


class CustomFilter(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, "get_filterset_kwargs"):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class AbstractBaseViewSet:
    custom_filter_class = CustomFilter()
    search_backends = SearchFilter()
    order_backend = OrderingFilter()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    paginator_class = CustomPaginator()

    def __init__(self):
        pass

    @staticmethod
    def error_message_formatter(serializer_errors):
        """Formats serializer error messages to dictionary"""
        return {
            f"{name}": f"{message[0]}" for name, message in serializer_errors.items()
        }

    @staticmethod
    def price_filtering(price_from, price_to, queryset):
        if price_from and price_to:
            try:
                queryset = queryset.filter(
                    price__range=[float(price_from), float(price_to)]
                )
            except Exception as ex:
                logger.error(f"error filtering price due to {str(ex)}")
        return queryset


class BaseViewSet(ViewSet, AbstractBaseViewSet):
    @staticmethod
    def get_data(request) -> dict:
        """Returns a dictionary from the request"""
        return request.data if isinstance(request.data, dict) else request.data.dict()

    def get_list(self, queryset):
        if "search" in self.request.query_params:
            query_set = self.search_backends.filter_queryset(
                request=self.request, queryset=queryset, view=self
            )
        elif self.request.query_params:
            query_set = self.custom_filter_class.filter_queryset(
                request=self.request, queryset=queryset, view=self
            )
        else:
            query_set = queryset
        if "ordering" in self.request.query_params:
            query_set = self.order_backend.filter_queryset(
                request=self.request, queryset=queryset, view=self
            )
        else:
            query_set = query_set.order_by("-pk")  # was originally 'pk'
        return query_set

    def get_paginated_data(self, queryset, serializer_class):
        paginated_data = self.paginator_class.generate_response(
            queryset, serializer_class, self.request
        )
        return paginated_data
