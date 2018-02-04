import logging

from ..models import *
from ..user_ops.serializer import UserSerializer
from ..validators import *

logger = logging.getLogger('django')


class LocationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'lat', 'lng', 'time', 'user')

    def create(self, validated_data):
        validated_data['user'] = self.context.pop('user')
        prev_location = Location.objects.filter(user=validated_data['user'], next_location=None).filter(
            time__date=validated_data['time'].date()).get()

        logger.info(prev_location)
        instance = self.Meta.model.objects.create(**validated_data)
        prev_location.next_location = instance
        prev_location.save()
        return instance
