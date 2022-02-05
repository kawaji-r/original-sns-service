from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import query
from django.http.response import JsonResponse
from django.views import generic
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.urls import reverse_lazy
from .forms import ProfileForm
from .models import CustomUser, Follow
from notifications.models import Notification
from posts.models import Post, Like
from config.settings import LABEL
import base64, datetime


class ProfileEdit(
    LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    success_url = '/accounts/edit/'
    template_name = 'account/edit.html'
    success_message = 'プロフィールを更新しました。'

    def get_object(self):
        return self.request.user

# プロフィール画面表示
class ProfileDetail(
    LoginRequiredMixin, generic.UpdateView):

    model = CustomUser
    form_class = ProfileForm
    template_name = 'account/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォロー、フォロワー数
        context['follow_count'] = Follow.objects.filter(follow_from=self.kwargs.get('pk')).count()
        context['follower_count'] = Follow.objects.filter(follow_to=self.kwargs.get('pk')).count()

        # ラベル
        context['label'] = LABEL

        # 画面下部の投稿を取得
        context['posts'] = self.__get_profile_post(self.request.path)

        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        # POSTデータからbase64エンコードされた画像データを取得
        if self.request.POST.get('image_base64'):
            image_data = base64.b64decode(self.request.POST.get('image_base64').split(',')[1])
            # ファイルパス生成
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            db_photo_data = "images/" + now + ".png"
            file_path = "media/" + db_photo_data
            # ファイル生成
            with open(file_path, 'bw') as f4:
                f4.write(image_data)
            # DB登録
            post.photo = db_photo_data
        # 画像削除
        if self.request.POST.get('image_delete'):
            post.photo = None
        # コミット
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:detail_post', kwargs={'pk': self.object.pk})

    # プロフィール画面下部に表示するポストの内容をURLから決定
    def __get_profile_post(self, path):
        if  '/post/' in path:
            retval = Post.objects.filter(user_id=self.kwargs.get('pk'), post_category__in=(0,2)).order_by('-created_at')
        elif '/post_reply/' in path:
            retval = Post.objects.filter(user_id=self.kwargs.get('pk')).order_by('-created_at')
        elif '/media/' in path:
            media = Post.objects.filter(user_id=self.kwargs.get('pk'))
            retval = media.exclude(photo='').order_by('-created_at')
        elif '/like/' in path:
            like_list = Like.objects.filter(user=self.kwargs.get('pk')).values_list('post', flat=True)
            retval = Post.objects.filter(id__in=like_list)
        else:
            raise Exception
        return retval

# フォローユーザー一覧画面を表示
class FollowList(LoginRequiredMixin, generic.ListView):
    template_name = 'account/follow_list.html'
    paginate_by = 10
    model = CustomUser

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)

        # URLでフィルタリング条件を変更
        if '/accounts/follow-list/' in self.request.path:
            # follow_toユーザーリスト取得
            user_list = Follow.objects.filter(follow_from=self.kwargs.get('pk')).values_list('follow_to',flat=True)
        elif '/accounts/follower-list/' in self.request.path:
            # follow_fromユーザーリスト取得
            user_list = Follow.objects.filter(follow_to=self.kwargs.get('pk')).values_list('follow_from',flat=True)

        # CustomUserから情報取得
        queryset = CustomUser.objects.filter(id__in=user_list)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 対象ユーザー名取得
        target_user = CustomUser.objects.filter(id=self.kwargs.get('pk')).first().nickname
        if '/accounts/follow-list/' in self.request.path:
            # 見出し用
            context['heading'] = target_user + "さんがフォローしているユーザー"
        elif '/accounts/follower-list/' in self.request.path:
            # 見出し用
            context['heading'] = target_user + "さんをフォローしているユーザー"

        # ラベル
        context['label'] = LABEL

        return context

# フォローボタン押下時の処理
class FollowControl(LoginRequiredMixin, generic.View):
    model = Follow
    NOTIFICATION = '{}さんがあなたをフォローしました。'

    def post(self, request):
        follow_to_id = request.POST.get('id')
        follow_to_user = CustomUser.objects.get(id=follow_to_id)
        user = self.request.user

        # URLで挙動を変更
        if request.path == '/accounts/follow/':
            # フォローする
            Follow(follow_from=user, follow_to=follow_to_user).save()
            # 処理完了後のHTMLを設定ファイルから取得
            inner_html = LABEL['UNFOLLOW_BUTTON']
            # 処理完了後のクラス付け替えに使用
            follow_flag = True
            # フォローした相手へのお知らせを作成
            Notification.objects.create(
                text=self.NOTIFICATION.format(user),
                user_id=follow_to_id,
                action_user=user
            )
        else:
            # フォローを外す
            Follow.objects.get(follow_from=user, follow_to=follow_to_user).delete()
            # 処理完了後のHTMLを設定ファイルから取得
            inner_html = LABEL['FOLLOW_BUTTON']
            # 処理完了後のクラス付け替えに使用
            follow_flag = False

        data = {
            'innerHtml': inner_html,
            'followFlag': follow_flag,
        }

        return JsonResponse(data)


class Deactivate(LoginRequiredMixin, generic.View):

    def get(self, request, **kwargs):
        target_user = self.kwargs['pk']
        request_user = self.request.user
        if request_user.id == target_user:
            request_user.is_active = False
            request_user.save()
            return redirect('/accounts/signup/')
        else:
            return redirect('/')
