from django.test import TestCase, Client
from django.urls import reverse
import json

class MyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('ask_view')  # 假设您的URL名称为'my_view'

    def test_post_success(self):
        # Testing a valid POST request with JSON data
        data = json.dumps({'field1': 'value1', 'field2': 'value2'})
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.content.decode('utf-8'))

    def test_post_failure(self):
        # 测试无效的POST请求（例如，缺少必要字段）
        response = self.client.post(self.url, {'field1': 'value1'})
        self.assertEqual(response.status_code, 400)

    def test_get_method_not_allowed(self):
        # 测试GET请求（应该返回405方法不允许）
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
