from django.test import TestCase
from videoflix.models import Video
from datetime import date
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from videoflix.models import Video
from rest_framework import status
from django.test import TestCase
from videoflix.serializers import VideoSerializer
from videoflix.models import Video
from datetime import date
from django.test import TestCase
from videoflix.tasks import create_thumbnail, convert720p
import os

class VideoModelTest(TestCase):
    
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="This is a test video.",
            genre="fitness",
            created_at=date.today()
        )

    def test_video_creation(self):
        """
        Test that a Video object is created successfully.
        """
        self.assertIsInstance(self.video, Video)
        self.assertEqual(self.video.title, "Test Video")
        self.assertEqual(self.video.genre, "fitness")
        self.assertEqual(self.video.description, "This is a test video.")
    
    def test_video_default_date(self):
        """
        Test that the 'created_at' field defaults to today's date.
        """
        self.assertEqual(self.video.created_at, date.today())
        
class VideoViewTest(APITestCase):
    
    def setUp(self):
        # Create a user and token for authenticated requests
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create some test videos
        self.video = Video.objects.create(
            title="Test Video",
            description="This is a test video.",
            genre="fitness"
        )
    
    def test_video_list(self):
        """
        Test that the video list API returns a 200 status and video data.
        """
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure there's 1 video
    
    def test_video_detail(self):
        """
        Test fetching a single video by ID.
        """
        video_id = self.video.id
        response = self.client.get(f'/videos/{video_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Video")
    
    def test_login(self):
        """
        Test user login with correct credentials.
        """
        response = self.client.post('/login/', {
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_logout(self):
        """
        Test user logout by ensuring token is deleted.
        """
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.filter(user=self.user).count(), 0)
        

class VideoSerializerTest(TestCase):

    def setUp(self):
        self.video_data = {
            "title": "Test Video",
            "description": "This is a test video.",
            "genre": "fitness",
            "created_at": date.today()
        }
        self.video = Video.objects.create(**self.video_data)
    
    def test_video_serialization(self):
        """
        Test that the VideoSerializer correctly serializes the Video object.
        """
        serializer = VideoSerializer(self.video)
        data = serializer.data
        self.assertEqual(data['title'], self.video.title)
        self.assertEqual(data['genre'], self.video.genre)
    
    def test_video_deserialization(self):
        """
        Test that the VideoSerializer correctly deserializes data to create a Video object.
        """
        serializer = VideoSerializer(data=self.video_data)
        self.assertTrue(serializer.is_valid())
        video = serializer.save()
        self.assertEqual(video.title, "Test Video")
        
class ThumbnailAndConversionTest(TestCase):
    
    def setUp(self):
        # Assuming you have some test video file in your test environment
        self.test_video = "media/videos/3327959-hd_1920_1080_24fps.mp4"
    
    def test_create_thumbnail(self):
        """
        Test that the thumbnail is created successfully.
        """
        thumbnail_path = create_thumbnail(self.test_video)
        self.assertTrue(os.path.exists(thumbnail_path))
    
    def test_convert720p(self):
        """
        Test that the video is converted to 720p.
        """
        convert720p(self.test_video)
        converted_video_path = "media/videos/3327959-hd_1920_1080_24fps.mp4"
        self.assertTrue(os.path.exists(converted_video_path))