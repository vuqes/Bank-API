from rest_framework import serializers

from .models import *


class BankAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['first_name', 'last_name', 'city', 'balance']


class FormTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True)
    is_success = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['recipient', 'sender', 'value', 'date_transaction', 'is_success']
