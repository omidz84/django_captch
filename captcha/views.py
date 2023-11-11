from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import GenerateCaptchaSerializer, ValidateCaptchaSerializer


class GenerateCaptchaView(GenericAPIView):
    serializer_class = GenerateCaptchaSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(request.data)
        return Response(serializer.data, status.HTTP_200_OK)


class ValidateCaptchaView(GenericAPIView):
    serializer_class = ValidateCaptchaSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Captcha is invalid'}, status.HTTP_200_OK)
