from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

#for pagination
class CustomPagination(PageNumberPagination):
    page_size = 10 # default page size
    max_page_size = 1000 # default max page size
    page_size_query_param = 'PAGE_SIZE' 
      
    def get_paginated_response(self, data):
        if size := self.request.query_params.get('PAGE_SIZE'):
            self.page_size = int(size)
            
        return Response({
            'count': self.page.paginator.count,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'results': data
        })
    
#custom permissions class
from rest_framework import permissions
class IsDeliveryCrew(permissions.BasePermission):
    """
    Custom permission for delivery crew.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return request.user.groups.filter(name='Delivery_crew').exists()