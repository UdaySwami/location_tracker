import logging

from django.contrib.auth.hashers import make_password
from rest_framework_jwt.settings import api_settings

from ..models import *
from ..validators import *
from ..location_ops.serializer import LocationSerializer
from ..utils import get_distance_covered

logger = logging.getLogger('django')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4, validators=[validate_password],
                                     error_messages={
                                         "blank": "Password cannot be empty",
                                         "min_length": "Password too short(min 8 characters are required)"
                                     })
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'token')

    @staticmethod
    def as_serializer(json_object):
        s = UserSerializer(data=json_object)
        return s

    @staticmethod
    def get_token(obj):
        try:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(obj)
            token = jwt_encode_handler(payload)
            return 'JWT ' + token
        except Exception as e:
            logger.error("Unable to generate token %s" % e)
            return None

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['email'] = validated_data['email'].lower()
        user = self.Meta.model.objects.create(**validated_data)
        return user


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = User
        fields = ('email', 'password')

    @staticmethod
    def as_login_request(json_object):
        d = LoginRequestSerializer()
        d.__dict__.update(json_object)
        return d


class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class UserTrackSerializer(serializers.Serializer):
    date = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()
    distance_covered = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @staticmethod
    def get_date(obj):
        return obj.time.date()
        # return ResponseUserSerializer(obj.user).data

    @staticmethod
    def get_locations(obj):
        locations_travelled = [LocationSerializer(obj).data]
        while obj.next_location:
            obj = obj.next_location
            locations_travelled.append(LocationSerializer(obj).data)
        return locations_travelled

    @staticmethod
    def get_distance_covered(obj):
        locations = [obj]
        while obj.next_location:
            obj = obj.next_location
            locations.append(obj)
        return get_distance_covered(locations)

    class Meta:
        fields = ('date', 'locations', 'distance_covered')


class AllUserTrackSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()
    distance_covered = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @staticmethod
    def get_user(obj):
        return ResponseUserSerializer(obj.user).data

    @staticmethod
    def get_date(obj):
        return obj.time.date()
        # return ResponseUserSerializer(obj.user).data

    @staticmethod
    def get_locations(obj):
        locations_travelled = [LocationSerializer(obj).data]
        while obj.next_location:
            obj = obj.next_location
            locations_travelled.append(LocationSerializer(obj).data)
        return locations_travelled

    @staticmethod
    def get_distance_covered(obj):
        locations = [obj]
        while obj.next_location:
            obj = obj.next_location
            locations.append(obj)
        return get_distance_covered(locations)

    class Meta:
        fields = ('user', 'date', 'locations', 'distance_covered')
