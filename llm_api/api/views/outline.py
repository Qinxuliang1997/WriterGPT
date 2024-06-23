from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
from .Writer import Writer

class OutlineView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            writer = Writer(user)
            outline = writer.write_outline(data)
            # outline = {
            #     '小节 1': {
            #         'title': "小节标题1",
            #         'paragraphs': {
            #             '段落 1': {'content': "这是第一段内容。"},
            #             '段落 2': {'content': "这是第二段内容。"}
            #         }
            #     },
            #     '小节 2': {
            #         'title': "小节标题2",
            #         'paragraphs': {
            #             '段落 1': {'content': "小节2的第一段内容。"}
            #         }
            #     },
            #     '小节 3': {
            #         'title': "小节标题3",
            #         'paragraphs': {
            #             '段落 1': {'content': "小节3的第一段落"}
            #         }
            #     }
            # }
            return JsonResponse({
                'status': 'success',
                # 'message': 'Article data received successfully.',
                # 'Access-Control-Allow-Origin': 'http://localhost:3000',
                # 'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
                'article': {"outline": outline}
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