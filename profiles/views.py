from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Profile
from .serializers import ProfileSerializer

# 1. CREATE USER API
class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny] # Anyone can sign up

    def post(self, request):
        try:
            profile = Profile.objects.create_profile(
                password=request.data.get('password'),
                email=request.data.get('email'),
                phone_number=request.data.get('phone_number'),
                **{k: v for k, v in request.data.items() if k not in ['password', 'email', 'phone_number']}
            )
            return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 2. UPDATE USER API
class UpdateUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        identifier = request.data.get('identifier')
        if not identifier:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        # Combine text data and potential file uploads (avatars)
        updates = {**request.data, **request.FILES}
        updates.pop('identifier', None)

        try:
            profile = Profile.objects.update_profile(identifier, **updates)
            return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 3. DELETE USER API
class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        identifier = request.data.get('identifier')
        success = Profile.objects.delete_profile(identifier)
        if success:
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# 4. LIST/DETAIL USER API
class AllUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        identifier = request.query_params.get('id')
        user_type = request.query_params.get('type')

        # If a specific ID/Email is passed in the URL (?id=...)
        if identifier:
            profile = Profile.objects.get_profile(identifier)
            if not profile:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(ProfileSerializer(profile).data)

        # Otherwise, handle list types
        if user_type == 'verified':
            queryset = Profile.objects.get_verified_profiles()
        elif user_type == 'unverified':
            queryset = Profile.objects.get_unverified_profiles()
        else:
            queryset = Profile.objects.get_all_profiles()

        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)