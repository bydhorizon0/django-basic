from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from blog.forms import PostForm
from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"  # ???
    paginate_by = 10  # 속성을 추가하면 자동으로 페이지네이션이 적용됨

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        search_type = self.request.GET.get("search_type")

        if search:
            match search_type:
                case "t":
                    queryset = queryset.filter(title__icontains=search)
                case "tc":
                    queryset = queryset.filter(
                        Q(title__icontains=search) | Q(content__icontains=search)
                    )
                    pass
                case "a":
                    queryset = queryset.filter(author__username__icontains=search)
                    pass
                case "all", _:
                    queryset = queryset.filter(
                        Q(title__icontains=search)
                        | Q(content__icontains=search)
                        | Q(author__username__icontains=search)
                    )
        return queryset.order_by("-created_at")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/show.html"
    pk_url_kwarg = "post_id"  # ???


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/create.html"
    form_class = PostForm  # ???
    login_url = "login"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = PostForm()
        return render(request, "blog/create.html", {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post_list")
        # 실패하면 form과 함께 다시 렌더링 -> 이전 값 유지
        return render(request, "blog/create.html", {"form": form})


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/update.html"
    pk_url_kwarg = "post_id"
    form_class = PostForm

    def get_success_url(self):
        return reverse("blog:post_show", kwargs={"post_id": self.object.id})


class PostDeleteView(View):
    def get(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return redirect("blog:post_list")
