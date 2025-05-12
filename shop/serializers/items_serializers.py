from rest_framework import serializers
from shop.models import ShopItem
from shop.models.colors import Color
from shop.models.brand import Brand
from shop.models.category import Category
from shop.models.material import Material
from shop.models.size import Size
from shop.models.sub_category import SubCategory, SubCategoryItems
from users.serializers.user_serializers import UserSerializer


class ShopItemSerializer(serializers.ModelSerializer):
    brand = serializers.ListField(child=serializers.CharField(), write_only=True)
    colors = serializers.ListField(child=serializers.CharField(), write_only=True)
    size = serializers.ListField(child=serializers.CharField(), write_only=True)
    category = serializers.ListField(child=serializers.CharField(), write_only=True)
    sub_category = serializers.ListField(child=serializers.CharField(), write_only=True)
    material = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)


    class Meta:
        model = ShopItem
        fields = ['id', 'created_at', 'title', 'description', 'image', 'price', 'is_sold', 'state',
                  'type', 'view_count', 'payment_methods', 'shipping_methods', 'hash_tags', 'condition',
                  'brand', 'colors', 'size', 'category', 'sub_category', 'material','owner']

    def to_representation(self, instance):
        # print("to_representation")
        data=super().to_representation(instance)
        data['brand']=[b.name for b in instance.brand.all()]
        data['colors']=[c.name for c in instance.colors.all()]
        data['size'] = [s.name for s in instance.size.all()]
        data['category'] = [c.name for c in instance.category.all()]
        data['sub_category'] = [sc.name for sc in instance.sub_category.all()]
        data['material'] = [m.name for m in instance.material.all()]
        data['owner'] = UserSerializer(instance.owner).data


        return data

    def to_internal_value(self, data):
        # print("to_internal_value")
        internal = super().to_internal_value(data.copy())

        def get_valid_objects(model, names, field_name):
            objs = model.objects.filter(name__in=names)
            # print("objs", objs)
            found_names = set(obj.name for obj in objs)
            # print("found_names", found_names)
            missing = set(names) - found_names
            # print("missing", missing)
            if missing:
                raise serializers.ValidationError(
                    {field_name: f"Invalid value: {', '.join(missing)}"}
                )
            return list(objs)

        internal['brand'] = get_valid_objects(Brand, data.get('brand', []), 'brand')
        internal['colors'] = get_valid_objects(Color, data.get('colors', []), 'colors')
        internal['size'] = get_valid_objects(Size, data.get('size', []), 'size')
        internal['category'] = get_valid_objects(Category, data.get('category', []), 'category')
        internal['sub_category'] = get_valid_objects(SubCategory, data.get('sub_category', []), 'sub_category')
        internal['material'] = get_valid_objects(Material, data.get('material', []), 'material')
        return internal

    def create(self, validated_data):
        # print("create")
        brand = validated_data.pop('brand', [])
        colors = validated_data.pop('colors', [])
        size = validated_data.pop('size', [])
        category = validated_data.pop('category', [])
        sub_category = validated_data.pop('sub_category', [])
        material = validated_data.pop('material', [])

        shop_item = ShopItem.objects.create(**validated_data)
        shop_item.brand.set(brand)
        shop_item.colors.set(colors)
        shop_item.size.set(size)
        shop_item.category.set(category)
        shop_item.sub_category.set(sub_category)
        shop_item.material.set(material)

        return shop_item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('updated_at', 'deleted_at', 'is_deleted', 'is_active')

        extra_kwargs = {
            'name': {'required': True},
            'translation_key': {'required': True},
        }

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ('created_at', 'updated_at', 'deleted_at', 'is_deleted', 'is_active')

        extra_kwargs = {
            'name': {'required': True},
            'translation_key': {'required': True},
            'category': {'required': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['parent_category_name'] = instance.category.name if instance.category else None
        return data


class SubCategoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategoryItems
        exclude = ('created_at', 'updated_at', 'deleted_at', 'is_deleted', 'is_active')
        extra_kwargs = {
            'name': {'required': True},
            'translation_key': {'required': True},
            'sub_category': {'required': True},
        }


