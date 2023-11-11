import uuid
import base64

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_captcha import captcha
from rest_captcha.settings import api_settings

from .utils import random_char_challenge


class GenerateCaptchaSerializer(serializers.Serializer):
    captcha = serializers.SerializerMethodField(read_only=True)

    def get_captcha(self, instance):
        key = str(uuid.uuid4())
        value = random_char_challenge(api_settings.CAPTCHA_LENGTH)
        settings.REDIS_CAPTCHA.set(key, value, settings.REDIS_CAPTCHA_TIME)
        image_bytes = captcha.generate_image(value)
        image_b64 = base64.b64encode(image_bytes)

        data = {
            'CAPTCHA_KEY': key,
            'CAPTCHA_IMAGE': image_b64,
            "image_type": "image/png",
            "image_decode": "base64",
            # 'value': value
        }
        return data


class ValidateCaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=300, read_only=False, write_only=True)
    captcha_value = serializers.CharField(max_length=5, read_only=False, write_only=True)

    def validate(self, data):
        try:
            captcha_key = data.get('captcha_key')
            captcha_value = data.get('captcha_value')
            captcha_value_redis = settings.REDIS_CAPTCHA.get(name=captcha_key)
            captcha_value_redis = captcha_value_redis.decode('utf-8')
        except:
            raise ValidationError(_('Captcha is invalid or expired'))
        if captcha_value_redis != captcha_value:
            raise ValidationError(_('Captcha is invalid or expired'))
        return data
