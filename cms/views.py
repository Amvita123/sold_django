from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Cms
from cms.serializers.cms_serializers import CmsSerializers

class CmsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        slug = request.query_params.get('slug')
        if slug:
            cms = Cms.objects.filter(slug=slug)
            if cms.exists():
                serializer = CmsSerializers(cms, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Slug with this name not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cms = Cms.objects.all()
            serializer = CmsSerializers(cms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



    def post(self, request):
        serializer = CmsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cms_data = serializer.save()
            response_data = CmsSerializers(cms_data).data
            return Response({"message": "cms created successfully", "data": response_data},
                            status=status.HTTP_200_OK)

