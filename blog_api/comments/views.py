from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer
from articles.models import Article
from .permissions import IsOwnerOrAdminOrReadOnly  # ודא שהקובץ קיים ומוגדר כראוי

class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: מחזיר את כל התגובות לכתבה מסוימת.
    POST: מוסיף תגובה חדשה לכתבה מסוימת (למשתמשים מחוברים בלבד).
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comment.objects.filter(article__id=article_id)

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        serializer.save(user=self.request.user, article=article)

class CommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    GET: מחזיר תגובה מסוימת.
    PUT/PATCH: מעדכן תגובה.
    מורשה רק אם המשתמש הוא היוצר או אדמין.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

class CommentDestroyAPIView(generics.DestroyAPIView):
    """
    DELETE: מוחק תגובה.
    מורשה רק אם המשתמש הוא היוצר או אדמין.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
