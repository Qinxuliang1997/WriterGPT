from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import shutil
import threading
from .utils.create_index import index_documents, save_all_index

# Global list to track indexing threads
threads = []   
class UploadView(APIView):
    def get(self, request, format=None):
        # Return a list of uploaded files
        original_data_dir = os.path.join(os.path.dirname(__file__), '..', 'original_data')
        uploaded_files, _, _ = get_file_list(original_data_dir)
        return JsonResponse({'uploaded_files': uploaded_files}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        single_file = request.FILES.get('single_file')
        website_url = request.POST.get('website')
        text_content = request.POST.get('text')
        folder_files = request.FILES.getlist('folder')
        original_data_dir = os.path.join(os.path.dirname(__file__), '..', 'original_data')
        
        if single_file:
            file_path = os.path.join(original_data_dir, 'original_documents', single_file.name)
            with open(file_path, 'wb') as f:
                for chunk in single_file.chunks():
                    f.write(chunk)
            index_thread = threading.Thread(target=index_documents, args=(file_path,))
            index_thread.start()
            threads.append(index_thread)
            # index_thread.join()
            # print("所有索引操作已完成。")
        if website_url:
            file_path = os.path.join(original_data_dir, "urls.txt")
            with open(file_path, 'a') as f:
                f.write(website_url + '\n')
            index_thread = threading.Thread(target=index_documents, args=(file_path,))
            index_thread.start() 
            threads.append(index_thread) 
            # index_thread.join()
            # print("所有索引操作已完成。")
        if text_content:
            file_path = os.path.join(original_data_dir, 'original_documents', "text.txt")
            with open(file_path, 'a') as f:
                f.write(text_content + '\n')
            index_thread = threading.Thread(target=index_documents, args=(file_path,))
            index_thread.start()
            index_thread.join()
            # print("所有索引操作已完成。")            
        if folder_files:
            for folder_file in folder_files:
                save_file_from_folder(folder_file, os.path.join(original_data_dir, 'original_documents/'))
                index_thread = threading.Thread(target=index_documents, args=(os.path.join(original_data_dir, 'original_documents', folder_file.name)))
                index_thread.start()
                threads.append(index_thread)
        uploaded_files, _, _ = get_file_list(original_data_dir) 
        indexed_data_dir = os.path.join(os.path.dirname(__file__), '..', 'indexed_documents')
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        save_all_index(indexed_data_dir)    
        return JsonResponse({'uploaded_files': uploaded_files}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        original_data_dir = os.path.join(os.path.dirname(__file__), '..', 'original_data')
        indexed_documents_dir = os.path.join(os.path.dirname(__file__), '..', 'indexed_documents')
        shutil.rmtree(original_data_dir)
        os.makedirs(original_data_dir)
        os.makedirs(os.path.join(original_data_dir, "original_documents"))
        shutil.rmtree(indexed_documents_dir)
        os.makedirs(indexed_documents_dir)
        uploaded_files, _, _ = get_file_list(original_data_dir) 
        return JsonResponse({'uploaded_files': uploaded_files}, status=status.HTTP_200_OK)

class FinishUploadView(APIView):
    def get(self, request, format=None):
        indexed_data_dir = os.path.join(os.path.dirname(__file__), '..', 'indexed_documents')
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        save_all_index(indexed_data_dir)
        return Response({'status': 'Indexing completed'})

def save_file_from_folder(file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if file.content_type == 'application/x-directory':
        folder_path = os.path.join(output_dir, file.name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for sub_file in file:
            save_file_from_folder(sub_file, folder_path)
    else:
        file_path = os.path.join(output_dir, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

def get_file_list(folder_path):
    overall_list = []
    document_names = []
    urls_list = []
    if not os.path.exists(folder_path):
        return overall_list, document_names, urls_content
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            document_names = os.listdir(file_path)
        elif os.path.isfile(file_path) and file.lower().endswith(".txt"):
            with open(file_path, 'r') as f:
                urls_content = f.read()
                urls_list = urls_content.split("\n")
        else:
            return overall_list, document_names, urls_content
    overall_list = document_names + urls_list
    return overall_list, document_names, urls_list
