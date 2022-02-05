from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm
from .models import Like
from .models import Post
from .models import Bookmark
from accounts.models import CustomUser
from accounts.models import Follow
from notifications.models import Notification
from config.settings import LABEL

class PostIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        # そのユーザがフォローしている人のIDを取得して代入する
        follow = Follow.objects.filter(follow_from=self.request.user).values_list('follow_to', flat=True)
        # appendできるようにリスト型にキャスト
        display_user = list(follow)
        # 自分の投稿も表示
        display_user.append(self.request.user.id)
        # display_userでfilter
        where = Q()
        where |= Q(post_category=0, user_id__in=display_user)
        where |= Q(post_category=2, user_id__in=display_user)
        posts = Post.objects.filter(where).order_by('-created_at')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommend'] = self.get_recommend_user()
        context['label'] = LABEL
        return context

    # おすすめとして表示するユーザーを取得する
    def get_recommend_user(self):
        recommend_user_num = 5 # おすすめのユーザー表示人数
        recommend_user = self.get_recent_post_user()
        # ログイン中のユーザーがフォローしている人リスト
        follow = Follow.objects.filter(follow_from=self.request.user).values_list('follow_to', flat=True)
        # フォローしている人は除外
        recommend_user = recommend_user.exclude(id__in=follow)
        # 自分は除外
        recommend_user = recommend_user.exclude(id=self.request.user.id)
        # 表示人数のみ取得
        recommend_user = recommend_user[:recommend_user_num]
        return recommend_user

    # 最近ポストしたユーザーを取得する
    def get_recent_post_user(self):
        recent_post_user = (
            Post.objects.all()
            .order_by('-created_at')
            .values_list('user_id', flat=True).order_by('user_id').distinct()
        )
        recent_post_user = CustomUser.objects.filter(id__in=recent_post_user)
        return recent_post_user

class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = "detail.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(
            related_post=self.kwargs['pk'],
            post_category=1
        ).order_by('-id')
        return context


class PostBookmarkView(LoginRequiredMixin, generic.ListView):
    template_name = 'bookmark.html'
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        bookmarks = Bookmark.objects.filter(user=self.request.user).values('post_id').order_by('id')
        posts = Post.objects.filter(id__in=bookmarks).order_by('-created_at')
        return posts


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    reply_category_no = 1

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.POST.get('action') == 'post':
            form.instance.user_id = self.request.user.id
            messages.success(self.request, '投稿が完了しました。')
            return super(PostCreateView, self).form_valid(form)
        elif self.request.POST.get('action') == 'reply':
            self.object.text = form.cleaned_data['text']
            self.object.related_post_id = self.request.POST.get('related_post_id')
            self.object.post_category = self.reply_category_no
            form.instance.user_id = self.request.user.id
            return super(PostCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました。')
        return redirect('posts:index')

    def get_success_url(self):
        if self.request.POST.get('action') == 'post':
            return reverse('posts:index')
        elif self.request.POST.get('action') == 'reply':
            return reverse('posts:detail', kwargs={'pk': self.object.related_post_id})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('posts:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            messages.success(self.request, '削除しました。')
        return super().delete(request, *args, **kwargs)


class LikeView(LoginRequiredMixin, generic.View):
    model = Like
    NOTIFICATION = '{}さんがあなたの投稿にいいねしました。'

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        user = self.request.user
        if request.path == '/like/':
            Like(user=user, post=post).save()
            like_count = Like.objects.filter(post=post).count()
            data = {
                'like_count': like_count
            }
            # お知らせ作成
            Notification(
                text=self.NOTIFICATION.format(user),
                user=post.user,
                action_user=user
            ).save()
        else:
            like = Like.objects.get(user=user, post=post).delete()
            like_count = Like.objects.filter(post=post).count()
            data = {
                'like_count': like_count
            }

        return JsonResponse(data)


class RepostView(LoginRequiredMixin, generic.View):
    model = Post
    repost_category_no = 2
    NOTIFICATION = '{}さんがあなたの投稿をリポストしました。'

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        data = {}
        if request.path == '/repost/':
            Post(
                user=user,
                related_post_id=post_id,
                post_category=self.repost_category_no
                ).save()
            # お知らせ作成
            Notification(
                text=self.NOTIFICATION.format(user),
                user=post.user,
                action_user=user
            ).save()
        else:
            Post.objects.get(
                user=user,
                related_post_id=post_id,
                post_category=self.repost_category_no
                ).delete()

        return JsonResponse(data)

class BookmarkView(LoginRequiredMixin, generic.View):
    model = Bookmark

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        user = self.request.user
        if request.path == '/bookmarking/':
            Bookmark(user=user, post=post).save()
        else:
            Bookmark.objects.get(user=user, post=post).delete()
        return JsonResponse({})

def ajax_reply(request):
    pk = request.GET.get('pk')
    post = Post.objects.get(pk=pk)
    replies = post.post_set.all().order_by('id')
    return render(request, 'posts.html', {'posts': replies})
