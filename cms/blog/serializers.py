from rest_framework import serializers
from .models import Article, Comment, Like, Tag

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  
    seo_slug = serializers.ReadOnlyField()  
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)  
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'seo_description', 'created_at', 'updated_at', 'seo_slug', 'tags', 'like_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_like_count(self, obj):
        return Like.objects.filter(article=obj).count()
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment_content', 'created_at', 'article']
        read_only_fields = ['created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Like
        fields = ['id', 'user', 'article']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag 
        fields = ['id', 'name']
