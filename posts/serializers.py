from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "context", "user", "likes"]

        extra_kwargs = {
            "likes": {
                "required": False,
                "read_only": True
            }
        }
