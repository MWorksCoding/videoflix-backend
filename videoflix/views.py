from django.conf import settings
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from videoflix.models import Video
from videoflix.serializers import VideoSerializer
from django.shortcuts import get_object_or_404


# Create your views here.

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })  
        

class LogoutView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        request.auth.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    
    
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("created_at")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class VideoView(APIView):
    permission_classes = [IsAuthenticated]
    """
    VideoView class for handling video-related requests.

    This view supports GET and POST methods for retrieving and creating videos respectively.
    The view requires the user to be authenticated.

    Methods:
    - get: Retrieves videos based on visibility (public or private).
    - post: Creates a new video entry for the authenticated user.
    """

# @method_decorator(cache_page(CACHE_TTL))
class VideoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        try:
            if pk:
                video = get_object_or_404(Video, pk=pk)
                serializer = VideoSerializer(video, context={'request': request})
            else:
                videos = Video.objects.all()
                serializer = VideoSerializer(videos, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
