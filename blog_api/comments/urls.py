from django.urls import path
from .views import (
    CommentListCreateAPIView,
    CommentUpdateAPIView,
    CommentDestroyAPIView,
)

urlpatterns = [
    # לקבלת תגובות והוספת תגובה לכתבה מסוימת
    path('articles/<int:article_id>/comments/', CommentListCreateAPIView.as_view(), name='article-comments'),
    # לעדכון תגובה
    path('comments/<int:pk>/update/', CommentUpdateAPIView.as_view(), name='comment-update'),
    # למחיקת תגובה – מאפשר גם למשתמש שיצר את התגובה וגם למנהל למחוק
    path('comments/<int:pk>/delete/', CommentDestroyAPIView.as_view(), name='comment-delete'),
]
