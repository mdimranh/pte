from django.db.models import (Count, ExpressionWrapper, F, OuterRef, Q,
                              Subquery, fields)
from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import IsAdminUser

from .models import *
from .serializers import *


class PlanView(APIView):
    def get(self, request):
        # Get the current date and time
        current_datetime = timezone.now()

        # Subquery to calculate the number of students for each purchase
        student_count_subquery = Purchase.objects.filter(
            id=OuterRef('id')
        ).annotate(student_count=Count('student')).values('student_count')

        # Query to retrieve purchases where available_account is greater than 0
        purchases = Purchase.objects.annotate(
            student_count=Subquery(student_count_subquery, output_field=fields.IntegerField())
        ).annotate(
            available_account=ExpressionWrapper(
                F('plan__maximum_accounts') - F('student_count'),
                output_field=fields.IntegerField()
            )
        ).filter(
            Q(plan__end_date__isnull=True) | Q(plan__end_date__gte=current_datetime),
            organization = request.user,
            available_account__gt = 0
        )
        serializer = PlanSerializer(data=purchases, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.data)

class PlanList(ListAPIView):
    serializer_class = PlanList
    def get_queryset(self):
        queryset = Plan.objects.filter(start_date__lte = timezone.now(), end_date__gte = timezone.now())
        return queryset


# class OrganizationPackageView(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = OrganizationPackageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OrganizationPackageListView(ListAPIView):
    serializer_class = OrganizationPackageSerializer
    queryset = OrganizationPackage.objects.all()

class OrganizationPackageDetailsView(RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = OrganizationPackageSerializer
    queryset = OrganizationPackage.objects.all()

class OrganizationPackageCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrganizationPackageSerializer
    queryset = OrganizationPackage.objects.all()

class OrganizationPackageUpdateView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    serializer_class = OrganizationPackageSerializer
    queryset = OrganizationPackage.objects.all()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    




class StudentPackageListView(ListAPIView):
    serializer_class = StudentPackageSerializer
    queryset = StudentPackage.objects.all()

class StudentPackageDetailsView(RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = StudentPackageSerializer
    queryset = StudentPackage.objects.all()

class StudentPackageCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudentPackageSerializer
    queryset = StudentPackage.objects.all()

class StudentPackageUpdateView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    serializer_class = StudentPackageSerializer
    queryset = StudentPackage.objects.all()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
