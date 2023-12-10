from django.utils import timezone
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.views import APIView
from accounts.models import User
from .models import Payment
from management.models import Purchase
from accounts.security.permission import IsStudentPermission, IsSuperAdmin, IsOrganizationPermission
from .serializers import PaymentSerializer
from rest_framework.response import Response

from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from dashboard.superadmin.models import Coupon

settings = { 'store_id': 'pte6564c943b9553', 'store_pass': 'pte6564c943b9553@ssl', 'issandbox': True }

class PaymentView(APIView):
    permission_classes = [IsStudentPermission, IsOrganizationPermission]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            price = serializer.validated_data['plan'].price
            purchase = Purchase(
                plan = serializer.validated_data['plan']
            )
            if request.user.is_organization:
                purchase.organization = request.user
            else:
                purchase.student = request.user
            if 'coupon_code' in serializer.validated_data:
                coupon = Coupon.objects.filter(code=serializer.validated_data['coupon_code'], start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
                if coupon is None:
                    return Response({
                        "error": "Coupon not found."
                    }, status=status.HTTP_404_NOT_FOUND)
                if coupon.type == 'fixed':
                    price -= coupon.amount
                else:
                    price -= (amount*coupon.amount) / 100
                purchase.coupon = coupon

        purchase.save()

        tid = "PPTE-"+timezone.now().strftime("%d%m%y")+"-"+timezone.now().strftime("%H%M%S")
        sslcommez = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = price
        post_body['currency'] = "BDT"
        post_body['tran_id'] = tid
        post_body['success_url'] = f"{get_current_site(request).domain}/payment/success/{request.user.id}/{purchase.id}"
        post_body['fail_url'] = f"{get_current_site(request).domain}/payment/fail/{purchase.id}"
        post_body['cancel_url'] = f"{get_current_site(request).domain}/payment/cancel/{purchase.id}"
        post_body['emi_option'] = 0
        post_body['cus_name'] = request.user.full_name
        post_body['cus_email'] = request.user.email
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = request.user.prfile.address
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"
        response = sslcommez.createSession(post_body)
        return Response({
            "redirect_url": response.get("redirectGatewayURL", "/")
        })
        # return redirect(response.get("redirectGatewayURL", "/"))
        # return redirect("pricing")

@csrf_exempt
def PaymentSuccess(request, uid, pid):
    data = request.POST

    user = User.objects.get(id=uid)
    plan = Plan.objects.get(id=pid)
    
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
    
    payment = Payment(**payment_data)
    payment.save()

    purchase = Purchase.objects.get(id=pid)
    purchase.payment = payment

    purchase = Purchase(
        payment=payment
    )
    purchase.save()

    return redirect(get_current_site(request).domain)

@csrf_exempt
def PaymentCancel(request, pid):
    data = request.POST
    purchase = Purchase.objects.get(id=pid)
    purchase.delete()
    return redirect(get_current_site(request).domain)

@csrf_exempt
def PaymentFail(request, pid):
        data = request.POST
        purchase = Purchase.objects.get(id=pid)
        purchase.delete()
        return redirect(get_current_site(request).domain)
