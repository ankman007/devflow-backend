from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = models.TextField()
    seo_description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seo_slug = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='articles')

    def save(self, *args, **kwargs):
        if not self.seo_slug:
            self.seo_slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} commented {self.comment_content} on article {self.article}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articles')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_user_article_like')
        ]
    
    def __str__(self):
        return f"{self.user} liked the article {self.article}"

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name