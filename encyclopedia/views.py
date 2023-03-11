import markdown2
import re

from random import choice
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
# Display content
def content(request, title):
    
    # Get .md file or return error page if not found
    file = util.get_entry(title)
    if not file:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "entries": util.list_entries()
        })
        
    # Convert .md file to .html and return
    file = markdown2.markdown(file)
    return render(request, "encyclopedia/page.html", {
        "file": file,
        "title": title,
        "entries": util.list_entries()
    })

# Make search work and/or save
def search(request):
    
    # Get the search query and redirect
    q = request.GET.get('q')
    content = request.GET.get('content')
    title = request.GET.get('title')
    
    # Check content for any alphabet to count as content
    if not content == None and not q == None:
        test = re.search('[a-zA-Z]',content)
        q = q.strip
        content = content.strip()

    entries = util.list_entries()
    if q in entries and content == None:
        return HttpResponseRedirect(q)
        
    # If q not in entries and no content, display search page
    elif content == None:
        arr = []
        for entry in entries:
            if q.lower() in entry.lower():
                arr.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "arr": arr
        })
    
    # Save edited content
    elif title in entries:
        # if content is empty display err
        if content.strip() == '':
            return render(request, "encyclopedia/err2.html", {
                "q": "error for edit"
            })
        
        # Else save and display page
        else:
            util.save_entry(title,content)
            return HttpResponseRedirect(title)
    
    # If not and content, then save
    else:
        # Check if title exists
        if q in entries:
            return render(request, "encyclopedia/err2.html", {
                "q": q
            })
            
        # Check for valid content
        if test == None:
            return render(request, "encyclopedia/err2.html", {
                "q": "test for test"# Put in a proper err msg
            })
    
        # Save and redirect
        util.save_entry(q, content)
        return HttpResponseRedirect(q)

# Create new page
def newpage(request):
    return render(request, "encyclopedia/newPage.html")
    
# Create edit feature
def edit(request):
    title = request.GET.get('title')
    return render(request, "encyclopedia/edit.html", {
        "file": util.get_entry(title),
        "title": title
    })
    
# Create random feature
def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect("content", title = entry)