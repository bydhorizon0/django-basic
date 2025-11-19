from django.urls import path

from blog.views import post_view, comment_view

app_name = "blog"

urlpatterns = [
    path("", post_view.PostListView.as_view(), name="post_list"),
    path("<int:post_id>", post_view.PostDetailView.as_view(), name="post_show"),
    path("create", post_view.PostCreateView.as_view(), name="post_create"),
    path(
        "update/<int:post_id>", post_view.PostUpdateView.as_view(), name="post_update"
    ),
    path(
        "delete/<int:post_id>", post_view.PostDeleteView.as_view(), name="post_delete"
    ),
    # Comment
    path(
        "create/comment/<int:post_id>",
        comment_view.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "<int:post_id>/update/comment/<int:comment_id>",
        comment_view.CommentUpdateView.as_view(),
        name="comment_update",
    ),
    path(
        "create/delete/<int:comment_id>",
        comment_view.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
