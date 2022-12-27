from rest_framework import viewsets, mixins, status
from rest_framework.permissions import *
from rest_framework.authentication import TokenAuthentication
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import *
from .models import *


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # автоматически создаем токен
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class KeyForRequest(TokenAuthentication):  # Для работы с Postman
    keyword = 'Bearer'


class BankAccountView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = BankAccount.objects.all()
    authentication_classes = (KeyForRequest,)
    serializer_class = BankAccountSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailTransaction(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = FormTransactionSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.username)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sender = BankAccount.objects.get(user=self.request.user).pk
        except ValueError:
            content = {'error': 'Пользователь не найден'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data['sender'] = sender
        serializer.save()

        try:
            Transaction.do_transaction(**serializer.validated_data)
            serializer.validated_data['is_success'] = True
            serializer.save()
        except ValueError:
            content = {'error': 'Ошибка перевода. Проверьте введенные данные'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
