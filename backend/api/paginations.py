from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class QuestionPagination(PageNumberPagination):
    """
    Custom paginator.
    Returns extra meta info (total, current page, total pages).
    """
    page_size = 20                          # full Big Five set on a single page
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "total_questions": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "results": data,
        })
