from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models.subscriptions import *
from subscription.serializers.serializers import UserSubscriptionSerializer, SubscriptionPlanSerializer


class SubscriptionView(APIView):

    def get(self, request):
        subcription_plan = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(subcription_plan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubscriptionPlanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Subscription plan create successfully"}, status=status.HTTP_200_OK)


class UserSubscriptionView(APIView):

    def get(self, request):
        user_subcription = UserSubscription.objects.all()
        serializer = UserSubscriptionSerializer(user_subcription, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            users = serializer.save()
            response_data=UserSubscriptionSerializer(users).data
            return Response({"message": "subscribe successfully.", "subscribe": response_data}, status=status.HTTP_200_OK)

