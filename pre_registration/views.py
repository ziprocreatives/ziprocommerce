# import random
# from django.forms import ValidationError
# from django.shortcuts import render
# from rest_framework import generics
# from pre_registration.serializer import PreRegistrationSerializer
# from pre_registration.models import Pre_registration 
# # Create your views here.

# class CreatePreRegistrationCreateUser:
#     queryset = Pre_registration.objects.all()
#     serializer_class = PreRegistrationSerializer
#     def perform_create(self, serializer):
#         identifier =self.kwargs.get('identifier')
#         if Pre_registration.objects.filter(identifier=identifier).exists():
#             raise ValidationError("Pre-registration with this identifier already exists.")
#         otp_code = random.randint(100000, 999999)
#         serializer.save(identifier=identifier, otp=str(otp_code))
#         self.send_otp_notification(identifier, otp_code)

#     def send_otp_notification(self, identifier, otp):
#         # Add your Email or SMS logic here
#         print(f"DEBUG: OTP {otp} sent to {identifier}")

# class PreRegistrationDetailView(generics.ListAPIView):
#     queryset = Pre_registration.objects.all()
#     serializer_class = PreRegistrationSerializer
#     serializer_class.save()
# class PreRegistrationVerifyView(generics.UpdateAPIView):
#     queryset = Pre_registration.objects.all()
#     serializer_class = PreRegistrationSerializer
#     serializer_class.save()
# class PreRegistrationDeleteView(generics.DestroyAPIView):
#     queryset = Pre_registration.objects.all()
#     serializer_class = PreRegistrationSerializer
#     serializer_class.save()