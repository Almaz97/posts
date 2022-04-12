from django.http import Http404
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "context", "user", "likes", "created_at"]

        extra_kwargs = {
            "user": {
                "required": False
            },
            "likes": {
                "read_only": True
            },
            "created_at": {
                "read_only": True
            }
        }

    def validate(self, attrs):
        request = self.context["request"]
        if request.method in ["PUT", "PATCH"] and self.instance.user != request.user:
            raise Http404

        return super().validate(attrs)
