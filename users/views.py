import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке, чтобы подтвердить почту: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    return redirect(reverse("user:login"))

class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("mailshot:home")

def view_profile(request):
    user = request.user
    context = {'user':user}
    return render(request, context, template_name = 'mailshot/profile.html')

class UserListView(ListView):
    model = User
    template_name = "mailshot/user_list.html"