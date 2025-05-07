from rest_framework import serializers

def positive_amount(value):
    if value <= 0:
        raise serializers.ValidationError('Amount must be positive.')

class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value % self.base != 0:
            raise serializers.ValidationError(f'Must be a multiple of {self.base}')
