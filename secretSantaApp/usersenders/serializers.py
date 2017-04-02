from rest_framework import serializers
from usersenders.models import UserSender
from django.utils.translation import ugettext_lazy as _


class UserSenderRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSender
        fields = ("name", "age", "group")

    def create(self, validated_data):
        return super(UserSenderRegistrationSerializer, self).create(validated_data)


class UserSenderGifteeAPIView(serializers.Serializer):
    name = serializers.CharField(required=True)

    default_error_messages = {
        'Nonexistent': _('Non existent name')
    }

    def __init__(self, *args, **kwargs):
        super(UserSenderGifteeAPIView, self).__init__(*args, **kwargs)
        self.userSender = None

    def validate(self, attrs):
        try:
            user = UserSender.objects.get_by_name(attrs.get("name"))
            user.send_to = UserSender.objects.get_giftee(user)
            self.userSender = user
            return attrs
        except:
            raise serializers.ValidationError(self.error_messages['Nonexistent'])
