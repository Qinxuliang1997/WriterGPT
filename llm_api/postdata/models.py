# from django.db import models
# from django.contrib.auth.models import User

# class UploadedFile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file_name = models.CharField(max_length=255)
#     file_path = models.CharField(max_length=255)  # 文件存储路径
#     upload_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.file_name
 
from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    uuid_name = str(uuid4())
    file_uuid = f"{uuid_name}.{ext}"    
    # 文件将被上传到MEDIA_ROOT/user_<id>/original_files/<filename>
    instance.file_uuid = uuid_name
    instance.file_name = filename
    return 'user_{0}/{1}/{2}'.format(instance.user_name.id, "original_files", file_uuid)

class UploadedFile(models.Model):
    # basic information
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_time = models.DateTimeField(auto_now_add=True)
    # file 
    single_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    file_name = models.CharField(max_length=250, blank=True, null=True)
    file_uuid = models.CharField(max_length=250, blank=True, null=True)
    # url
    url = models.URLField(max_length=200, blank=True, null=True ) 
    # text
    text = models.TextField(blank=True, null=True)