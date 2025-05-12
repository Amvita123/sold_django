import re
from rest_framework import serializers
from users.models.user import User
from shop.serializers.favorite_item_serializers import FavoriteItemSerializer
from profile.serializers.user_following_serializers import UserFollowingSerializer
from profile.models.user_following import UserFollowing
from shop.models.favorite_item import FavoriteItem
from shop.models.items import ShopItem
from datetime import timedelta
from django.utils.timezone import now

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    # date_created = serializers.DateTimeField("%d-%m-%Y", required=False)
    # extra fields
    username = serializers.SerializerMethodField()
    online = serializers.SerializerMethodField()
    ratings_count =serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    favorited_topics = serializers.SerializerMethodField()
    favorite_items = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = User

        exclude = ('is_superuser','last_login', 'is_staff', 'is_active', 'groups', 'user_permissions')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'fullname': {'required': True},
            'auth_provider': {'required': True},
        }

    def validate_fullname(self, name):
        pattern = r"^[A-Za-z\s]+$"
        if not re.match(pattern, name):
            raise serializers.ValidationError("fullname contain only alphabets")
        return name

    def validate_phone_number(self, value):
        if len(value) !=10:
            raise serializers.ValidationError("Phone number contain only integer value")
        if not value.isdigit():
            raise serializers.ValidationError("phone number must contain only digits")
        return value

    def create(self, validate_data):
        user=User.objects.create_user(**validate_data)
        return user

    def get_username(self, obj):
        return f"{obj.fullname.replace(' ', '').lower()}011" if obj.fullname else ""

    def get_online(self, obj):
        return True

    def get_ratings_count(self, obj):
        return 0

    def get_average_rating(self, obj):
        return 0.0

    def get_following(self, obj):
        return []

    def get_followers(self, obj):
        return []

    def get_favorited_topics(self, obj):
        return []

    def get_favorite_items(self, obj):
        return []

    def get_items_count(self, obj):
        return 0

    def get_status(self, obj):
        return True

    def get_is_verified(self, obj):
        return False


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4, required=True)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    # extra fields
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    favorite_items = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    online = serializers.SerializerMethodField()

    favorited_topics = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()


    class Meta:
        model = User
        exclude = ('is_superuser','groups', 'user_permissions', 'is_active', 'is_staff', 'last_login')

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({'email': 'user with this email not found'})

        if not user.is_active:
            raise serializers.ValidationError({'is_active': 'user account is not active'})

        attrs['user']=user
        return attrs

    def get_followers(self, obj):
        followers = UserFollowing.objects.filter(following=obj)
        return [str(f.follower.id) for f in followers]

    def get_following(self, obj):
        followings = UserFollowing.objects.filter(follower=obj)
        return [str(f.following.id) for f in followings]

    def get_favorite_items(self, obj):
        favorites = FavoriteItem.objects.filter(user = obj)
        return [str(f.item.id) for f in favorites]

    def get_items_count(self, obj):
        return ShopItem.objects.filter(owner=obj).count()

    def get_is_verified(self, obj):
        return obj.is_email_verified

    def get_online(self, obj):
        if obj.last_login:
            return obj.last_login + timedelta(minutes=5) > now()
        return False

    def get_favorited_topics(self, obj):
        return []

    def get_username(self, obj):
        return f"{obj.fullname.replace('', '').lower()}011" if obj.fullname else ""

    def get_ratings_count(self, obj):
        return 0

    def get_average_rating(self, obj):
        return 0.0

    def get_status(self, obj):
        return True

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password")
        return value


class CreateSuperUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        exclude = ('last_login', 'is_staff', 'is_active', 'is_email_verified', 'is_number_verified', 'groups', 'user_permissions', 'about', 'country', 'sex', 'address', 'nickname',
                   'is_superuser', 'show_location', 'show_notification', 'holiday_mode', 'phone_number', 'auth_provider', 'date_created')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'fullname': {'required': True},
            'auth_provider': {'required': True},
        }

    def validate_fullname(self, name):
        pattern = r"^[A-Za-z\s]+$"
        if not re.match(pattern, name):
            raise serializers.ValidationError("fullname contain only alphabets")
        return name

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    favorite_items = FavoriteItemSerializer(many=True, read_only=True)
    followers = UserFollowingSerializer(source='user_followers', many=True, read_only=True)
    following = UserFollowingSerializer(source='user_following', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'fullname', 'phone_number', 'auth_provider', 'account_status',
            'is_email_verified', 'address', 'is_number_verified', 'country', 'sex', 'nickname',
            'about', 'profile_pic', 'favorite_items', 'followers', 'following', 'show_location',
            'show_notification', 'holiday_mode'
        ]



