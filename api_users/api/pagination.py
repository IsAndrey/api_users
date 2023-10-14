from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'limit'
