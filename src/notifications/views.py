from datetime import datetime
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Notification


class notificationsView(LoginRequiredMixin, ListView):
    template_name = "notifications/notifications.html"
    context_object_name = 'notifications'
    model = Notification
    BORDER = timedelta(days=15)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notifications"] = Notification.objects.filter(
            user=self.request.user,
            created_at__gte=datetime.now() - self.BORDER,
            is_deleted=False
        ).order_by('-created_at')
        return context
