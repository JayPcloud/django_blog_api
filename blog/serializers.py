from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import BlogPost, BlogMedia, Comment, Like, Tag, BookMark, Notification
       

class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(read_only=True, view_name="user-detail")
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_bookmarked = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField(read_only=True,)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())

    def get_media(self, obj):
        request = self.context.get('request')
        return [
            media.file.url for media in obj.media.all()
        ]
    

    def get_likes_count(self, obj,):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_has_liked(self, obj,):
        user = self.context['request'].user
        return obj.likes.filter(user=user).exists() if user.is_authenticated else False
    
    def get_bookmark_count(self, obj):
        return obj.bookmarks.count()
    
    def get_has_bookmarked(self, obj):
        user = self.context['request'].user
        return obj.bookmarks.filter(user=user).exists() if user.is_authenticated else False
    
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags',[])
        blog_post = BlogPost.objects.create(**validated_data)
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            blog_post.tags.add(tag)
        return blog_post
    
    def update(self, instance, validated_data):
        tag_data = validated_data.pop('tags', [])

        if tag_data is not None:
            instance.tags.clear
            for tag_name in tag_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
            
        return super().update(instance, validated_data)
    

    class Meta():
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['id','author', 'media', 'created_at', 'updated_at',]
        
    



class BlogMediaSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    blog_post = serializers.HyperlinkedRelatedField(read_only=True, view_name="blogpost-detail", many=False)

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse(
            viewname='blogpost-media-detail',
            kwargs={
                'blogpost_pk': obj.blog_post.pk,
                'pk': obj.pk
            },
            request=request
        )

    class Meta():
        model = BlogMedia
        fields = '__all__'
        read_only_fields = ['id','created_at','blog_post',]
        



class CommentSerializer(serializers.ModelSerializer):
    blog = serializers.HyperlinkedRelatedField(read_only=True, view_name="blogpost-detail", many=False)
    author = serializers.HyperlinkedRelatedField(read_only=True, view_name="user-detail")
    # replies = serializers.SerializerMethodField()
    
    
    # def validate_parent(self, value):
    #     if self.parent is not None:
    #         raise serializers.ValidationError("You can only reply to top-level comments.")
    #     return value
    

    class Meta():
        model = Comment
        fields = '__all__'
        read_only_fields = ['id','created_at','blog', 'author', 'parent',]
        
        
    
    # def get_replies(self, obj):
    #     if self.context.get('depth', 1) > 1:
    #         return []
    #     return CommentSerializer(
    #         obj.replies.all(),
    #         many=True,
    #         context={'request': self.context['request'], 'depth': 2}
    #     ).data

    


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name="user-detail",)
    blog = serializers.PrimaryKeyRelatedField(read_only=True,)

    class Meta():
        model = Like
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta():
        model = Tag
        fields = '__all__'
        
        
        
class BookMarkSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name="user-detail",)
    blog = serializers.HyperlinkedRelatedField(read_only=True, view_name="blogpost-detail")

    class Meta():
        model = BookMark
        fields = '__all__'
        
        
# serializers.py
class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField()
    actor = serializers.StringRelatedField()
    blog = serializers.StringRelatedField()
    comment = serializers.StringRelatedField()
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'blog', 'comment', 'verb', 'created_at', 'is_read', 'is_active',]




        
