from django.urls import path
from .views import ArticleView
from .views import ModifyView
from .views import OutlineView

urlpatterns = [
    path('ask/', ArticleView.as_view(), name='article_view'),
    path('modify/', ModifyView.as_view(), name='modify_view'),
    path('outline/', OutlineView.as_view(), name='outline_view')
]