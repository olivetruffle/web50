from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.urls import reverse
from django.http import HttpResponse
import random
from random import choice

def convert(title):
    markdowner = Markdown()
    mrkdn = util.get_entry(title)
    converted = markdowner.convert(mrkdn)
    return converted

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert(title)
    if html_content is not None:
        return render(request, "encyclopedia/wiki.html", {
            "entry": html_content,
            "title": title
        })
    else:
        return HttpResponse("Page not found")

def search(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        # form = NewSearchForm(request.POST)
        form = request.POST['q']
        try:
            converted = convert(form)
        except:
            t = list(util.list_entries())
            print(t)
            print(type(form))
            #entries = list(filter(lambda entry: form in entry, t))
            print(form)
            entries = []
            for i in t:
                if form.lower() in i.lower():
                    entries.append(i)
            print(entries)
            return render(request, "encyclopedia/search.html",
            {
                "entries": entries
            })
        return render(request, "encyclopedia/wiki.html", {
                "entry": converted,
                "title": form
            })
    else:
        return render(request, "encyclopedia/index.html")

def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        pageExists = util.get_entry(title)
        if pageExists is not None:
            return HttpResponse("Error: page already exists.")
        else:
            util.save_entry(title, content)
            html_content = convert(title)
            return render(request, "encyclopedia/wiki.html", {
                "title": title,
                "entry": html_content
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        entry = request.POST['entry']
        html_content = convert(title)
        util.save_entry(title, entry)
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "entry": html_content
        })

def edit_2(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": entry
    })

def random(request):
    entries = list(util.list_entries())
    random_title = choice(entries)
    html_content = convert(random_title)
    return render(request, "encyclopedia/wiki.html", {
        "title": random_title,
        "entry": html_content
    })
