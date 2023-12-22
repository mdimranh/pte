from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        page_number = int(self.request.query_params.get(self.page_query_param, 1))
        page_size = self.get_page_size(self.request)

        total = self.page.paginator.count
        start_index = (page_number - 1) * page_size + 1
        end_index = start_index + len(data) - 1
        next_page_number = self.page.next_page_number() if self.page.has_next() else None
        previous_page_number = self.page.previous_page_number() if self.page.has_previous() else None

        links = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        }

        return Response({
            'total': total,
            'start_index': start_index if total > 0 else 0,
            'end_index': end_index,
            'links': links,
            'next': bool(next_page_number),
            'prev': bool(previous_page_number),
            "results": data
        })