from users.serializers.user_serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from profile.models.user_following import UserFollowing



class ProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        users = request.user
        if users.is_authenticated:
            serializer = UserSerializer(users)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            response_data=UserSerializer(user).data
            return Response({"message": "profile updated successfully", "profile": response_data},status=status.HTTP_200_OK)


class UserFollowView(APIView):
    def post(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({"message": "invalid user id"}, status=status.HTTP_400_BAD_REQUEST)

        # already_following = UserFollowing.objects.filter(follower=follower, following=following).exists()
        # if already_following:
        #     return Response({"message": "you are already following this user"}, status=status.HTTP_400_BAD_REQUEST)

        follow_relation = UserFollowing.objects.filter(follower=follower, following=following).first()

        if follow_relation:
            follow_relation.delete()
            return Response({"message": "you unfollow this user"}, status=status.HTTP_200_OK)

        UserFollowing.objects.create(follower=follower, following=following)
        return Response({"message": "you are now following this user"}, status=status.HTTP_200_OK)


class ProfileByIdView(APIView):
    def get(self, request, user_id):
        # user = request.user
        try:
            user_detail = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({"message": "User with ID not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowersView(APIView):
    def get(self, request):
        user = request.user
        followers = UserFollowing.objects.filter(following=user).select_related('follower')
        serializer = LoginSerializer([data.follower for data in followers], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingView(APIView):
    def get(self, request):
        user = request.user
        followings = UserFollowing.objects.filter(follower=user).select_related("following")
        serializer = LoginSerializer([data.following for data in followings], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
