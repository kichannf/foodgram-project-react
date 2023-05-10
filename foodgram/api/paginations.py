from rest_framework.pagination import PageNumberPagination


class LimitPaginations(PageNumberPagination):
    page_size_query_param = 'limit'
