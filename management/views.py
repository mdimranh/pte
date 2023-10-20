from django.db.models import (Count, ExpressionWrapper, F, OuterRef, Q,
                              Subquery, fields)
from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Purchase
from .serializers import PlanList, PlanSerializer


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

# class PlanList(ListAPIView):
#     serializer_class = PlanList
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         queryset = Answer.objects.filter(summarize=pk)
#         return queryset
    
