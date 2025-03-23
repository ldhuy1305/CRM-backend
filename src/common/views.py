from django.db.models import Model, Q, QuerySet
from rest_framework import viewsets

from api.constants import SortOderEnum


class SortAndFilterViewSet(viewsets.ModelViewSet):
    model = None

    def get_queryset_by_filter(self, queryset):
        request = self.request
        user = request.user
        is_view_all = getattr(request, "is_view_all", None)
        if not is_view_all:
            queryset = queryset.filter(created_by=user)

        return self._generate_query_with_filter(
            queryset=queryset,
            search_fields=(
                self.model.SEARCH_FIELDS
                if self.model and self.model.SEARCH_FIELDS
                else {}
            ),
            search_fields_contains=(
                self.model.SEARCH_FIELDS_CONTAINS
                if self.model and self.model.SEARCH_FIELDS_CONTAINS
                else {}
            ),
            query_params=request.query_params,
        )

    def get_queryset_by_sort(self, queryset):
        params = self.request.query_params
        sort_order = params.get("sort_order", None)
        sort_by = params.get("sort_by", None)
        return self._generate_query_with_sort(
            queryset=queryset,
            sort_order=sort_order,
            sort_by=sort_by,
        )

    @staticmethod
    def _generate_query_with_filter(
        queryset: QuerySet,
        search_fields: dict,
        search_fields_contains: dict,
        query_params,
    ) -> QuerySet:
        filters = {}

        for key, value in search_fields.items():
            if key in query_params:
                filters[value] = query_params[key]

        for key, value in search_fields_contains.items():
            if key in query_params:
                filters[f"{value}__icontains"] = query_params[key]

        return queryset.filter(Q(**filters))

    @staticmethod
    def _generate_query_with_sort(
        queryset: QuerySet,
        sort_order: str,
        sort_by: str,
    ) -> QuerySet:
        if sort_order == SortOderEnum.ASC.value:
            queryset = queryset.order_by(f"{sort_by}")
        elif sort_order == SortOderEnum.DESC.value:
            queryset = queryset.order_by(f"-{sort_by}")
        return queryset
