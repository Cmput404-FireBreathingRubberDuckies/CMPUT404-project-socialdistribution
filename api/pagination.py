from rest_framework import pagination

# Need to finish this, was just copied from
# http://www.django-rest-framework.org/api-guide/pagination/#custom-pagination-styles
class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })