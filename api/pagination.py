from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10  # har bir sahifada nechta obyect chiqishi
    page_size_query_param = "page_size"
    max_page_size = 100  # maksimal obyekt soni
