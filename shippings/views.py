from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shippings.serializers.shipping_serializers import ShippingSerializer
from shippings.models.shipping_info import ShippingInfo
from rest_framework.permissions import AllowAny, IsAuthenticated


class ShippingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            shipping_info= ShippingInfo.objects.get(user=user)
            serializer = ShippingSerializer(shipping_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ShippingInfo.DoesNotExist:
            return Response({"message": "shipping info not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        user = request.user
        try:
            shipping_info = ShippingInfo.objects.get(user=user)
        except ShippingInfo.DoesNotExist:
            return Response({"message": "Shipping info not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShippingSerializer(shipping_info, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "address update successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

