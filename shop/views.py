from shop.serializers.items_serializers import ShopItemSerializer, CategorySerializer, SubCategorySerializer, SubCategoryItemsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shop.models.items import ShopItem
from shop.models.favorite_item import FavoriteItem
from shop.models.brand import Brand
from shop.serializers.brand_serializers import BrandSerializer
from shop.models.category import Category
from shop.models.sub_category import SubCategory, SubCategoryItems
from shop.models.size import Size
from shop.serializers.size_serializers import SizeSerializer
from shop.models.colors import Color
from shop.serializers.color_serializers import ColorSerializer
from subscription.models.subscriptions import UserSubscription
from django.utils.timezone import now


class ShopItemView(APIView):
    def get(self, request):
        item_id = request.query_params.get("item_id")
        if item_id:
            try:
                items = ShopItem.objects.get(id=item_id)
                items.view_count += 1
                items.save()
                serializer = ShopItemSerializer(items)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ShopItem.DoesNotExist:
                return Response({"detail": "item with this id not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            items=ShopItem.objects.all().order_by('-created_at')
            serializer=ShopItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner']=request.user.id
        serializer = ShopItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            item = serializer.save()
            # print("item", item)
            response_data=ShopItemSerializer(item).data    # deserialization
            # print("response_data", response_data)
            return Response({"message": "item create successfully", "item": response_data}, status=status.HTTP_200_OK)

    def patch(self, request, item_id=None):
        try:
            item = ShopItem.objects.get(id=item_id, owner=request.user)
        except ShopItem.DoesNotExist:
            return Response({"error": "item with this id not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShopItemSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data= ShopItemSerializer(item).data
            return Response({"message": "item updated successfully", "item": response_data,}, status=status.HTTP_200_OK)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class UsersItemView(APIView):
    def get(self, request, user_id):
        try:
            items = ShopItem.objects.filter(owner_id=user_id)
            serializer = ShopItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        try:
            user=request.user
            item = ShopItem.objects.get(id=item_id)
            favorite_item, created = FavoriteItem.objects.get_or_create(user=user, item=item)

            if created:
                return Response({"message": "item added to favourite"}, status=status.HTTP_200_OK)
            else:
                favorite_item.delete()
                return Response({"message": "item removed from favourites"}, status=status.HTTP_200_OK)
        except ShopItem.DoesNotExist:
            return Response({"error": "item with this id not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BrandView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        brands = Brand.objects.all().order_by("-created_at")
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category=Category.objects.all().order_by("-created_at")
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            items=serializer.save()
            response_data=CategorySerializer(items).data
            return Response({"message": "Category create", "category": response_data}, status=status.HTTP_200_OK)


class SubCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"detail": "category with this id not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            sub_category=SubCategory.objects.all().order_by('-created_at')
            serializer=SubCategorySerializer(sub_category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            items = serializer.save()
            response_data = SubCategorySerializer(items).data
            return Response({"message": "subcategory create", "sub_category": response_data}, status=status.HTTP_200_OK)


class SubCategoryItemsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        subcategory_id = request.query_params.get('subcategory_id')
        if subcategory_id:
            try:
                sub_category = SubCategoryItems.objects.get(sub_category_id=subcategory_id)
                serializer = SubCategoryItemsSerializer(sub_category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"detail": "sub_category with this id not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            sub_category_items=SubCategoryItems.objects.all().order_by('-created_at')
            serializer=SubCategoryItemsSerializer(sub_category_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = SubCategoryItemsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            items = serializer.save()
            response_data = SubCategoryItemsSerializer(items).data
            return Response({"message": "subcategory items create", "sub_category_items": response_data}, status=status.HTTP_200_OK)


class SizeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        sizes = Size.objects.all().order_by("-created_at")
        serializer = SizeSerializer(sizes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ColorView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        colors = Color.objects.all().order_by("-created_at")
        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAsSoldView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, item_id):
        try:
            item = ShopItem.objects.get(id=item_id)

            if item.owner != request.user:
                return Response({"message": "not authorized to modify item"}, status=status.HTTP_403_FORBIDDEN)
            if item.is_sold:
                return Response({"message": "Item already sold"}, status=status.HTTP_400_BAD_REQUEST)
            item.is_sold = True
            item.save()
            return Response({"message": "Item marked as sold successfully"}, status=status.HTTP_200_OK)
        except ShopItem.DoesNotExist:
            return Response({"message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


class MostPopularItemsView(APIView):
    def get(self, request):
        boosted_user = UserSubscription.objects.filter(plan__subscription_type="BOOSTED_VISIBILITY",expire_on__gte=now()).values_list('user')
        boosted_item = ShopItem.objects.filter(owner__in=boosted_user)
        favorite_items = FavoriteItem.objects.values_list('item').distinct()
        used_favorite_items = ShopItem.objects.filter(condition="used", id__in=favorite_items)
        combine_items = boosted_item | used_favorite_items
        serializer = ShopItemSerializer(combine_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)