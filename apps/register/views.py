from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.generic import View
from django.conf import settings

from .tokens import account_activation_token
from .forms import RegisterForm

# Create your views here.
def verification(request, *args, **kwargs):
    return render(request, "register/account_verification.html")

def register(request, *args, **kwargs):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = '[Djangod] Activation du compte'
            template_url = f"register/{'debug_activation_email' if settings.DEBUG else 'account_activation_email'}.html"
            message = render_to_string(template_url, {
                'user': user,
                'domain': current_site.domain, # localhost:8000
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, '', html_message=message)
            messages.success(request, ('Pour finaliser votre inscription, vous devez confirmer votre email.'))
            return redirect("register:verification")
    else:
	    form = RegisterForm()
    return render(request, "register/register.html", {"form":form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            user.profile.save()
            login(request, user)
            messages.success(request, ('Votre compte à été confirmé.'))
            return redirect("register:verification")
        else:
            messages.warning(request, ("Le lien de confirmation n'est pas valide, ce lien a peut être déjà été utilisé."))
            return redirect("register:verification")