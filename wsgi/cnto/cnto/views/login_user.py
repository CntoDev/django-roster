from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf


def login_user(request):
    state = "Please log in..."
    username = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('scrape-selection')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    context = {'state': state, 'username': username}
    context.update(csrf(request))

    return render_to_response('login.html', context)
