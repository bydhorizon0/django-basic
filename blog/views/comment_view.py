from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from blog.forms import CommentForm
from blog.models import Comment, Post


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request: Any, post_id: int, *args: Any, **kwargs: Any):
        post = get_object_or_404(Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment: Comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

        return redirect("blog:post_show", post_id=post_id)


class CommentUpdateView(LoginRequiredMixin, View):
    def post(
        self, request: Any, post_id: int, comment_id: int, *args: Any, **kwargs: Any
    ):
        comment = get_object_or_404(Comment, pk=comment_id)

        # 작성자 검증
        if comment.author != request.user:
            return redirect("blog:post_show", post_id=post_id)

        # POST 데이터 업데이트
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

        return redirect("blog:post_show", post_id=post_id)


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request: Any, comment_id: int, *args: Any, **kwargs: Any):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return redirect("blog:post_show", post_id=comment.post.id)
