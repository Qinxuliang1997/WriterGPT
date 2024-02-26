from django import forms
from .models import UploadedFile

class UploadedFileForm(forms.ModelForm):
    text = forms.CharField(required=False)
    single_file = forms.FileField(required=False)
    website = forms.URLField(required=False)
    class Meta:
        model = UploadedFile  # 指定这个表单对应的模型是UploadedFile
        fields = ['text', 'single_file', 'url']  # 指定表单中需要包含的字段，这里只需要上传的文件字段

    # 如果你需要对这个表单进行额外的定制或验证，可以在这里添加
    # 例如，添加一个清理方法来验证文件类型或大小
    # def clean_file(self):
    #     file = self.cleaned_data.get('file', False)
    #     if file:
    #         if file.size > 4*1024*1024:
    #             raise forms.ValidationError("文件大小不能超过4MB")
    #         if not file.content_type in ["image/jpeg", "image/png"]:
    #             raise forms.ValidationError("文件类型不支持")
    #     else:
    #         raise forms.ValidationError("无法读取文件")
    #     return file
