from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from . import util
from django.urls import reverse
import secrets


def title(request, title):

    text = util.get_entry(title)
    if text == None:
        return render(request, "encyclopedia/error.html", {
            "entries": util.list_entries()
        })

    else:
        html = markdown2.markdown(text)
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "content": html
        })


def index(request):

    if(request.method == "POST"):
        title = request.POST.get('title')
        markdown_text = request.POST.get("markdown_text")
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {
                "titleExists": True
            })
        else:
            util.save_entry(title, markdown_text)
            return HttpResponseRedirect(title)

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def search(request):

    if request.method == "GET":

        if 'q' in request.GET:

            search_text = request.GET.get('q')
            search_results = util.get_entry(search_text)

            if search_results == None:
                entries = util.list_entries()

                search_results = list(filter(lambda k: search_text in k, entries))
                return render(request, 'encyclopedia/search_results.html', {
                    'results': search_results
                })

            else:
                return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={'title': search_text}))

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

# Add a new page:
def add(request):
    return render(request, "encyclopedia/add.html", {
        "titleExists": False
    })


def edit(request, title):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={'title': title}))

    else:
        text = util.get_entry(title)
        if text == None:
            return render(request, "encyclopedia/error.html", {
                "entries": util.list_entries()
            })

        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": text
            })


def random(request):
    entries = util.list_entries()
    title = secrets.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={'title': title}))
