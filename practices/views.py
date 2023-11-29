from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from .AI import voiceAuthentication
from pte import settings
import os

from dashboard.superadmin.views import _models

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

class PracticeDestroyView(APIView):
    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        model = _models.get(self.kwargs.get('model'))
        question = model.objects.filter(id=id).first()
        if question is None:
            return Response({
                "detail": "Not found."
            }, status=status.HTTP_404_NOT_FOUND)
        question.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


