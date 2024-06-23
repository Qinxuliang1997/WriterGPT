from rest_framework import status
from django.http import JsonResponse
from django.conf import settings
import os
import shutil
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .forms import UploadedFileForm
from .models import UploadedFile

class UploadView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        uploads = UploadedFile.objects.filter(user_name=request.user)
        upload_data = self.get_upload_list(uploads)
        return JsonResponse({'uploaded_files': upload_data}, status=status.HTTP_200_OK)     

    def post(self, request, format=None):
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file_instance = form.save(commit=False)
            uploaded_file_instance.user_name = request.user
            uploaded_file_instance.save()
            
            uploads = UploadedFile.objects.filter(user_name=request.user)
            uploaded_files = self.get_upload_list(uploads)
            return JsonResponse({'uploaded_files': uploaded_files}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': '[error]'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        uploads = UploadedFile.objects.filter(user_name=request.user)
        uploads.delete()
        files_dir = os.path.join(settings.MEDIA_ROOT, f"user_{request.user.id}", 'original_files')  
        for filename in os.listdir(files_dir):
            file_path = os.path.join(files_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)  # 删除文件
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')    
        files_dir = os.path.join(settings.MEDIA_ROOT, f"user_{request.user.id}", 'indexed_files')  
        if os.path.exists(files_dir):
            shutil.rmtree(files_dir)
        return JsonResponse({'message': 'completed!'}, status=status.HTTP_200_OK)

    def get_upload_list(self, uploads):
        upload_data = set()
        for upload in uploads:
            if upload.text:
                upload_data.add(upload.text[:10]+'...')
            if upload.file_name:
                upload_data.add(upload.file_name)
            if upload.url:
                upload_data.add(upload.url)
        return list(upload_data)
