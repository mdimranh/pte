from rest_framework import serializers
from management.models import OrganizationPackage, StudentPackage

class OrgPaymentSerializer(serializers.Serializer):
    package = serializers.PrimaryKeyRelatedField(queryset=OrganizationPackage.objects.all())
    validation = serializers.IntegerField()

class StudentPaymentSerializer(serializers.Serializer):
    package = serializers.ModelField(model_field=StudentPackage)