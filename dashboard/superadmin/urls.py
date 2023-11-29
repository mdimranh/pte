from django.urls import path

from .views import *

urlpatterns = [
    path('study_material/add', StudyMaterialCreateAPIView.as_view()),
    path('study_materials/<str:category>', StudyMaterialListAPIView.as_view()),
    path('study_material/<int:id>', StudyMaterialDestroyAPIView.as_view()),
    path("superadmin/test/counts", TestStatisticsView.as_view()),
    path("organization/add", OrgRegistrationView.as_view()),
    path("organization/<int:id>/update", OrganizationUpdateApiView.as_view()),
    path("organization/<int:pk>", OrganizationRetriveDestroyApiView.as_view()),
    path("organizations", OrganizationListView.as_view()),
    path("organization/passwordchange", OrgPasswordChange.as_view()),
    path("organization/useridchange", OrgUseridChange.as_view()),
    path("adminuser/add", AdminUserAddView.as_view()),
    path("adminusers", AdminUserListView.as_view()),
    path("adminuser/<int:id>", DeleteAdminUserView.as_view()),
    path("coupon", CouponListCreateAPIView.as_view()),
    path("coupon/<int:pk>", CouponRetrieveUpdateDestroyAPIView.as_view()),
    path("discussion/count", DiscussionCountView.as_view()),
    path("<model>/questions", ModelWiseDiscussion.as_view()),
    # path("promo_banner", PromoBannerView.as_view()),
    # path("promo_banner/<int:id>", PromoBannerRUDView.as_view()),
    path("promo_banner", PromoBannerRetriveUpdateView.as_view()),
]
