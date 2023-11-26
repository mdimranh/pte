from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from .AI import voiceAuthentication
from pte import settings
import os

class AudioToText(APIView):
    def post(self, request):
        audio = request.FILES['audio']
        
        fs = FileSystemStorage(location="practices/audio")  # Specify the location
        filename = fs.save(audio.name, audio)
        
        file_path = os.path.join(settings.BASE_DIR, "practices/audio", filename)  # Construct the file path
        
        text = voiceAuthentication(file_path)  # Pass the correct file path to voiceAuthentication
        
        # Delete the file after extracting text
        os.remove(file_path)
        
        return Response({
            "text": text
        })
