from django.shortcuts import render


def scrape(request):
    """Return the daily process main overview page.
    """
    context = {

    }
    return render(request, 'scrape.html', context)
