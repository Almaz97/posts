from django.contrib.auth.models import User
from django.urls import reverse

from auth_app.tests import BearerTokenTestCaseBase
from posts.models import Post


class TestPostView(BearerTokenTestCaseBase):

    def setUp(self):
        super().setUp()
        self.post_data = {
            "title": "My title",
            "context": "some context"
        }

        self.post = Post.objects.create(
            title=self.post_data["title"],
            context=self.post_data["context"],
            user=self.user,
        )

    @staticmethod
    def create_new_post():
        new_user = User.objects.create(
            username="test_user",
            email="test@gmail.com",
        )
        post = Post.objects.create(
            title="test",
            context="test",
            user=new_user,
        )
        return post

    def test_create_post(self):
        posts_url = reverse("posts-list")
        res = self.client.post(
            posts_url, self.post_data, **self.bearer_token
        )

        self.assertEqual(res.status_code, 201)
        post = Post.objects.get(id=res.data["id"])

        self.assertEqual(post.title, res.data["title"])
        self.assertEqual(post.context, res.data["context"])
        self.assertEqual(post.user.id, res.data["user"])

    def test_list_posts(self):
        posts_url = reverse("posts-list")
        self.create_new_post()
        res = self.client.get(
            posts_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 2)

    def test_retrieve_post(self):
        posts_url = reverse("posts-detail", args=[self.post.id])
        res = self.client.get(
            posts_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["title"], self.post.title)

    def test_update_post(self):
        posts_url = reverse("posts-detail", args=[self.post.id])
        post_data = self.post_data
        post_data["title"] = "updated title"
        post_data["context"] = "updated context"

        res = self.client.patch(
            posts_url, post_data, **self.bearer_token
        )
        self.assertEqual(res.status_code, 200)
        post = Post.objects.get(id=res.data["id"])
        self.assertEqual(post.title, res.data["title"])
        self.assertEqual(post.context, res.data["context"])

    def test_update_foreign_post(self):
        post = self.create_new_post()

        posts_url = reverse("posts-detail", args=[post.id])
        post_data = self.post_data
        post_data["title"] = "updated title"
        post_data["context"] = "updated context"

        res = self.client.patch(
            posts_url, post_data, **self.bearer_token
        )
        self.assertEqual(res.status_code, 404)

    def test_delete_post(self):
        post_id = self.post.id
        posts_url = reverse("posts-detail", args=[post_id])
        res = self.client.delete(
            posts_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 204)
        is_exists = Post.objects.filter(id=post_id).exists()
        self.assertEqual(is_exists, False)

    def test_delete_foreign_post(self):
        post = self.create_new_post()
        post_id = post.id
        posts_url = reverse("posts-detail", args=[post_id])
        res = self.client.delete(
            posts_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 404)
        is_exists = Post.objects.filter(id=post_id).exists()
        self.assertEqual(is_exists, True)

    def test_like_post(self):
        posts_url = reverse("posts-like", args=[self.post.id])
        res = self.client.post(
            posts_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.likes.first().id, self.user.id)

    def test_unlike_post(self):
        self.post.likes.add(self.user)
        posts_url = reverse("posts-unlike", args=[self.post.id])
        res = self.client.post(
            posts_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.post.likes.count(), 0)
