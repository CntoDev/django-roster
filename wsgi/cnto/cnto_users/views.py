from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.template.context_processors import csrf
from cnto_users.forms import EditPasswordForm


class EditUserView(LoginRequiredMixin, TemplateView):
    template_name = "cnto_users/edit.html"
    login_url = "/login"


    def post(self, request):
        form = EditPasswordForm(request.POST)

        if request.POST.get("cancel"):
            return redirect('home')
        elif form.is_valid():
            username = request.user.username
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]
            user = authenticate(username=username, password=current_password)
            user.set_password(new_password)
            user.save()

            return redirect('edit-user')

        context = {}
        context.update(csrf(request))

        context['form'] = form

        return self.render_to_response(context)

    def get(self, request):
        form = EditPasswordForm(initial={
            "username": request.user.username
        })

        context = {}
        context.update(csrf(request))

        context['form'] = form

        return self.render_to_response(context)
