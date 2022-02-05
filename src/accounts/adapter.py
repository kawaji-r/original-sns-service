from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        allauthでの登録処理によりコール
        サインアップでの登録データを追加した場合にオーバーライドする
        """
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        user.nickname = form.cleaned_data.get('nickname')
        user.username = form.cleaned_data.get('username')
        user.save()