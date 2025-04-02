from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    # storing tags as a comma-separated string (אפשר לשנות בעתיד למודל נפרד אם יש צורך)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
