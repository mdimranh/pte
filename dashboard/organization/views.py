from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView)
from rest_framework.response import Response

from accounts.models import User
from accounts.security.permission import IsOrganizationPermission
from accounts.serializers import UserCreateSerializer, UserDetailsSerializer
from practices.discussion.views import CustomPagination

from .serializers import (CreateStudentSerializer, StudentDetailsSerializer,
                          StudentListSerializer)


class RegistrationView(GenericAPIView):
    serializer_class = CreateStudentSerializer
    permission_classes = (IsOrganizationPermission,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserCreateSerializer(user, context=self.get_serializer_context()).data)

class StudenListView(ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsOrganizationPermission]
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = User.objects.filter(profile__organization__id=self.request.user.id)
        return queryset

class StudenDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    queryset = User.objects.all()
    serializer_class = StudentDetailsSerializer
    permission_classes = [IsOrganizationPermission]