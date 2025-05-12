from ratings.serializers.user_rating_serializers import UserRatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ratings.models.user_rating import UserRating
from users.models.user import User

class UserRatingView(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"message": "User id required"}, status=status.HTTP_400_BAD_REQUEST)

        ratings = UserRating.objects.filter(rated_users__id=user_id)
        serializer = UserRatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        value = request.data.get('value')
        review = request.data.get('review')
        rated_users_id = request.data.get('user_id')

        try:
            rated_users = User.objects.get(id=rated_users_id)
        except User.DoesNotExist:
            return Response({"message": "Rated user not found"}, status=status.HTTP_404_NOT_FOUND)
        rating = UserRating.objects.create(value=value, review=review, owner=request.user, rated_users=rated_users)
        serializer = UserRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
