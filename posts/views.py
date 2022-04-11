from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != self.request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["POST"])
    def like(self, request, pk):
        post = self.get_object()
        post.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def unlike(self, request, pk):
        post = self.get_object()
        post.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
