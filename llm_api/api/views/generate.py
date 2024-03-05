from django.http import JsonResponse
from rest_framework.views import APIView
import json
from .ContentAgent import ContentAgent

class GenerateView(APIView):
    # permission_classes = [IsAuthenticated]    
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            content_agent = ContentAgent(user)
            content = content_agent.write(data)
            return JsonResponse({
                'status': 'success',
                'message': 'Article data received successfully.',
                # 'Access-Control-Allow-Origin': 'http://localhost:3000',
                # 'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
                'content': content,
            }, status=200)
        except json.JSONDecodeError:
            # 如果请求体不是有效的 JSON，返回错误
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON.'
            }, status=400)
        except Exception as e:
            # 处理其他可能的异常
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)