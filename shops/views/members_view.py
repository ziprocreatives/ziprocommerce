from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import ShopMember


class BaseMemberAPI(APIView):
    """Helper to standardize manager responses."""

    def handle_manager_response(self, result_or_success, msg=None):
        # Case for methods returning (result, message)
        if msg is not None:
            if not result_or_success:
                return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": msg}, status=status.HTTP_200_OK)

        # Case for methods returning a single string message
        if "not found" in result_or_success.lower() or "error" in result_or_success.lower():
            return Response({"error": result_or_success}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": result_or_success}, status=status.HTTP_200_OK)


# --- 1. PRE-REGISTRATION (STAGING) ---

class StartPreRegistrationAPI(APIView):
    """
    Step 1: User submits email and all shop/account info.
    Data is stored in 'PreeRegistration' and an OTP is sent.
    """

    def post(self, request):
        identifier = request.data.get('identifier')
        data = request.data
        otp, msg = ShopMember.objects.start_pre_registration(data)
        if not otp:
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": msg,
            "otp_debug": otp  # In production, remove this and send via email
        }, status=status.HTTP_200_OK)


class FinalizeRegistrationAPI(APIView):
    """
    Step 2: User submits email and OTP code.
    The Shop and Creator are finally created.
    """

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        member, msg = ShopMember.objects.finalize_registration(email, code)
        if not member:
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": msg,
            "member_id": member.id,
            "shop_id": member.shop.id,
            "role": member.role
        }, status=status.HTTP_201_CREATED)


# --- 2. AUTH & OTP (For Existing Members) ---

class GenerateOtpAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp, msg = ShopMember.objects.generate_otp(email)
        if not otp:
            return Response({"error": msg}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": msg, "otp_debug": otp}, status=status.HTTP_200_OK)


class VerifyOtpAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        success, member_or_msg = ShopMember.objects.verify_otp(email, code)
        if success:
            return Response({
                "message": "Verified successfully.",
                "member_id": member_or_msg.id,
                "role": member_or_msg.role
            }, status=status.HTTP_200_OK)
        return Response({"error": member_or_msg}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteOtpAPI(BaseMemberAPI):
    def post(self, request, member_id):
        msg = ShopMember.objects.delete_otp(member_id)
        return self.handle_manager_response(msg)


# --- 3. STAFF MANAGEMENT ---

class AddStaffAPI(BaseMemberAPI):
    def post(self, request, shop_id):
        data = request.data
        member, msg = ShopMember.objects.add_staff(
            shop_id=shop_id,
            admin_id=data.get('admin_id'),
            nickname=data.get('nickname'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role', 'handler')
        )
        return self.handle_manager_response(member, msg)


class GetStaffMemberAPI(APIView):
    def post(self, request, shop_id, target_id):
        req_id = request.data.get('requester_id')
        member, msg = ShopMember.objects.get_staff_by_id(shop_id, req_id, target_id)
        if not member:
            return Response({"error": msg}, status=status.HTTP_403_FORBIDDEN)
        return Response({
            "nickname": member.nickname,
            "email": member.identifier,  # Updated to match model
            "role": member.role
        })


class DeleteStaffAPI(BaseMemberAPI):
    def post(self, request, shop_id, target_id):
        admin_id = request.data.get('admin_id')
        success, msg = ShopMember.objects.delete_staff(shop_id, admin_id, target_id)
        return self.handle_manager_response(success, msg)


# --- 4. ACCESS HANDOVER ---

class HandoverAccessAPI(BaseMemberAPI):
    def post(self, request, shop_id):
        cur_id = request.data.get('current_creator_id')
        new_id = request.data.get('new_creator_id')
        success, msg = ShopMember.objects.handover_access(shop_id, cur_id, new_id)
        return self.handle_manager_response(success, msg)


# --- 5. GRANULAR UPDATES ---

class UpdateMemberNicknameAPI(BaseMemberAPI):
    def post(self, request, member_id):
        msg = ShopMember.objects.update_nickname(member_id, request.data.get('value'))
        return self.handle_manager_response(msg)


class UpdateMemberEmailAPI(BaseMemberAPI):
    def post(self, request, member_id):
        msg = ShopMember.objects.update_email(member_id, request.data.get('value'))
        return self.handle_manager_response(msg)


class UpdateMemberPasswordAPI(BaseMemberAPI):
    def post(self, request, member_id):
        msg = ShopMember.objects.update_password(member_id, request.data.get('value'))
        return self.handle_manager_response(msg)


class UpdateMemberRoleAPI(BaseMemberAPI):
    def post(self, request, shop_id, target_id):
        admin_id = request.data.get('admin_id')
        new_role = request.data.get('value')
        msg = ShopMember.objects.update_role(shop_id, admin_id, target_id, new_role)
        return self.handle_manager_response(msg)