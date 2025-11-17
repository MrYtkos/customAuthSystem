from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.permissions_utils import has_permission


class OrdersView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        if not has_permission(request.user, 'orders', 'read'):
            return Response({'detail': 'Forbidden'}, status=403)

        orders = [
            {'id': 1, 'name': 'Order 1', 'owner_id': "id_владельца"},
            {'id': 2, 'name': 'Order 2', 'owner_id': "id_владельца"},
        ]
        return Response(orders)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        if not has_permission(request.user, 'orders', 'create'):
            return Response({'detail': 'Forbidden'}, status=403)

        return Response({'detail': 'Order created'}, status=201)
