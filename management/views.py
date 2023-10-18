from django.db.models import Count, ExpressionWrapper, F, fields
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, Profile
from .serializers import PlanList, PlanSerializer


class PlanView(APIView):
    def get(self, request):
        plans = Plan.objects.annotate(
            profile_count=Count('profile')
        ).filter(
            maximum_accounts__gt=ExpressionWrapper(F('profile_count'), output_field=fields.IntegerField())
        )
        serializer = PlanSerializer(data=plans, many=True)
        if serializer.is_valid():
            return Response({
                "plans": serializer.data
            })
        return Response({
            "plans": serializer.data
        })

# class PlanList(ListAPIView):
#     serializer_class = PlanList
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         queryset = Answer.objects.filter(summarize=pk)
#         return queryset
    
