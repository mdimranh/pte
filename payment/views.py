from rest_framework.views import APIView
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ 
settings = { 'store_id': 'pte6564c943b9553', 'store_pass': 'pte6564c943b9553@ssl', 'issandbox': True }

class Payment(APIView):
    def get(self, request):
        sslcommez = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = 100.26
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "12345"
        post_body['success_url'] = "https://api.codebyamirus.link/payment/cancel"
        post_body['fail_url'] = "https://api.codebyamirus.link/payment/cancel"
        post_body['cancel_url'] = "https://api.codebyamirus.link/payment/cancel"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "Dhaka, Bangladesh"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcommez.createSession(post_body)
        print(response)
        return Response(response)

class PaymentCancel(APIView):
    def post(self, request):
        data = request.data
        print(data)
        return Response({
            "status": "success"
        })
