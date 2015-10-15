from django.shortcuts import render, redirect


def scrape(request):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}
    return render(request, 'scrape.html', context)
