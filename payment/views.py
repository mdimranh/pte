from django.shortcuts import redirect
from django.utils import timezone
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.views import APIView
from accounts.models import User
from .models import Payment
from management.models import Purchase, Profile
from accounts.security.permission import IsStudentPermission, IsSuperAdmin, IsOrganizationPermission
from .serializers import *
from rest_framework.response import Response

from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from dashboard.superadmin.models import Coupon

settings = { 'store_id': 'pte6564c943b9553', 'store_pass': 'pte6564c943b9553@ssl', 'issandbox': True }

# class PaymentView(APIView):
#     permission_classes = [IsStudentPermission, IsOrganizationPermission]
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = PaymentSerializer(data=data)
#         if serializer.is_valid():
#             # if "organization_package" in serializer.validated_data:
#             price = serializer.validated_data['plan'].price
#             purchase = Purchase(
#                 plan = serializer.validated_data['plan']
#             )
#             if request.user.is_organization:
#                 purchase.organization = request.user
#             else:
#                 purchase.student = request.user
#             if 'coupon_code' in serializer.validated_data:
#                 coupon = Coupon.objects.filter(code=serializer.validated_data['coupon_code'], start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
#                 if coupon is None:
#                     return Response({
#                         "error": "Coupon not found."
#                     }, status=status.HTTP_404_NOT_FOUND)
#                 if coupon.type == 'fixed':
#                     price -= coupon.amount
#                 else:
#                     price -= (amount*coupon.amount) / 100
#                 purchase.coupon = coupon

#         purchase.save()

#         tid = "PPTE-"+timezone.now().strftime("%d%m%y")+"-"+timezone.now().strftime("%H%M%S")
#         sslcommez = SSLCOMMERZ(settings)
#         post_body = {}
#         post_body['total_amount'] = price
#         post_body['currency'] = "BDT"
#         post_body['tran_id'] = tid
#         post_body['success_url'] = f"{get_current_site(request).domain}/payment/success/{request.user.id}/{purchase.id}"
#         post_body['fail_url'] = f"{get_current_site(request).domain}/payment/fail/{purchase.id}"
#         post_body['cancel_url'] = f"{get_current_site(request).domain}/payment/cancel/{purchase.id}"
#         post_body['emi_option'] = 0
#         post_body['cus_name'] = request.user.full_name
#         post_body['cus_email'] = request.user.email
#         post_body['cus_phone'] = "01700000000"
#         post_body['cus_add1'] = request.user.prfile.address
#         post_body['cus_city'] = "Dhaka"
#         post_body['cus_country'] = "Bangladesh"
#         post_body['shipping_method'] = "NO"
#         post_body['multi_card_name'] = ""
#         post_body['num_of_item'] = 1
#         post_body['product_name'] = "Test"
#         post_body['product_category'] = "Test Category"
#         post_body['product_profile'] = "general"
#         response = sslcommez.createSession(post_body)
#         return Response({
#             "redirect_url": response.get("redirectGatewayURL", "/")
#         })
#         # return redirect(response.get("redirectGatewayURL", "/"))
#         # return redirect("pricing")

def payment_payload(request, price, purchase):
    tid = "PPTE-"+timezone.now().strftime("%d%m%y")+"-"+timezone.now().strftime("%H%M%S")
    post_body = {}
    post_body['total_amount'] = price
    post_body['currency'] = "BDT"
    post_body['tran_id'] = tid
    post_body['success_url'] = f"https://{get_current_site(request).domain}/payment/success/{request.user.id}/{purchase.id}"
    post_body['fail_url'] = f"https://{get_current_site(request).domain}/payment/fail/{purchase.id}"
    post_body['cancel_url'] = f"https://{get_current_site(request).domain}/payment/cancel/{purchase.id}"
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.full_name
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = "01700000000"

    profile = Profile.objects.filter(user=request.user).first()

    post_body['cus_add1'] = profile.address if profile is not None else ""

    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"
    return post_body


class OrganizationPaymentView(APIView):
    permission_classes = [IsOrganizationPermission]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = OrgPaymentSerializer(data=data)
        if serializer.is_valid():
            sslcommez = SSLCOMMERZ(settings)
            package = serializer.validated_data['package']
            price = None
            for item in package.validation:
                if item['id'] == serializer.validated_data['validation']:
                    price = item['cost']
                    break
            if price is None:
                return Response({
                    "validation": "Not found."
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            purchase = Purchase(
                org_package = package,
                validation_id = serializer.validated_data['validation'],
                organization = request.user
            )

            purchase.save()

            payload = payment_payload(request, price, purchase)

            response = sslcommez.createSession(payload)
            return Response({
                "redirect_url": response.get("redirectGatewayURL", "/")
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class StudentPaymentView(APIView):
    permission_classes = [IsStudentPermission]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = StudentPaymentSerializer(data=data)
        if serializer.is_valid():
            sslcommez = SSLCOMMERZ(settings)
            package = serializer.validated_data['package']

            purchase = Purchase(
                org_package = package,
                organization = request.user
            ).save()

            payload = payment_payload(request, package.cost, purchase)

            response = sslcommez.createSession(payload)
            return Response({
                "redirect_url": response.get("redirectGatewayURL", "/")
            })

@csrf_exempt
def PaymentSuccess(request, uid, pid):
    user = User.objects.get(id=uid)
    purchase = Purchase.objects.get(id=pid)
    data = request.POST
    payment_data = {}
    payment_data["tran_id"] = data.get("tran_id")
    payment_data["val_id"] = data.get("val_id")
    payment_data["amount"] = data.get("amount")
    payment_data["store_amount"] = data.get("store_amount")
    payment_data["card_type"] = data.get("card_type")
    payment_data["card_no"] = data.get("card_no")
    payment_data["bank_tran_id"] = data.get("bank_tran_id")
    payment_data["status"] = data.get("status")
    payment_data["author"] = user
    payment_data["details"] = data
    
    payment = Payment(**payment_data)
    payment.save()
    purchase.payment = payment
    purchase.save()

    return redirect(f"https://{get_current_site(request).domain}")

@csrf_exempt
def PaymentCancel(request, pid):
    data = request.POST
    purchase = Purchase.objects.get(id=pid)
    purchase.delete()
    return redirect(f"https://{get_current_site(request).domain}")

@csrf_exempt
def PaymentFail(request, pid):
    data = request.POST
    purchase = Purchase.objects.get(id=pid)
    purchase.delete()
    return redirect(f"https://{get_current_site(request).domain}")
