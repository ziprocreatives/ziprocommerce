from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Customer  # Ensure your model is named Customer

# Basic index to resolve your routing error
def index(request):
    return HttpResponse("Customer API is operational.")

# ==========================================
# 1. AUTHENTICATION VIEWS
# ==========================================

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        customer, msg = Customer.objects.register(
            shop_id=data.get('shop_id'),
            password=data.get('password'),
            email=data.get('email'),
            phone=data.get('phone'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        if customer:
            return Response({"message": msg}, status=status.HTTP_201_CREATED)
        return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        customer, msg = Customer.objects.authenticate_customer(
            shop_id=data.get('shop_id'),
            credential=data.get('credential'),
            password=data.get('password')
        )
        if customer:
            return Response({
                "message": msg,
                "identifier": customer.identifier,
                "email": customer.email
            }, status=status.HTTP_200_OK)
        return Response({"error": msg}, status=status.HTTP_401_UNAUTHORIZED)

# ==========================================
# 2. OTP & SECURITY VIEWS
# ==========================================

class RequestOTPView(APIView):
    def post(self, request):
        data = request.data
        customer, result = Customer.objects.request_otp(
            shop_id=data.get('shop_id'),
            credential=data.get('credential')
        )
        if customer:
            # result contains {"otp": code, "method": "email/sms"}
            return Response(result, status=status.HTTP_200_OK)
        return Response({"error": result}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    def post(self, request):
        data = request.data
        success, msg = Customer.objects.verify_otp(
            shop_id=data.get('shop_id'),
            credential=data.get('credential'),
            input_code=data.get('otp_code')
        )
        return Response({"message": msg}, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        success, msg = Customer.objects.reset_password_via_otp(
            shop_id=data.get('shop_id'),
            credential=data.get('credential'),
            otp_code=data.get('otp_code'),
            new_password=data.get('new_password')
        )
        return Response({"message": msg}, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)

# ==========================================
# 3. PROFILE & ACCOUNT MANAGEMENT
# ==========================================

class UpdateProfileView(APIView):
    def patch(self, request):
        data = request.data
        success, msg = Customer.objects.update_basic_info(
            shop_id=data.get('shop_id'),
            identifier=data.get('identifier'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        return Response({"message": msg}, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)

class UpdatePhoneView(APIView):
    def patch(self, request):
        data = request.data
        success, msg = Customer.objects.update_contact_phone(
            shop_id=data.get('shop_id'),
            identifier=data.get('identifier'),
            new_phone=data.get('new_phone')
        )
        return Response({"message": msg}, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)