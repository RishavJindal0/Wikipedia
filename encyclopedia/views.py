from django.shortcuts import render
import markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

class NewSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={"class":"search","placeholder":"Search Encyclopedia","autocomplete":"off"}))

#TODO
class EditForm(forms.Form):
    title = forms.CharField(label="Edit Title")
    body = forms.CharField(label="Edit Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))

#TODO
class CreateNewForm(forms.Form):
    title = forms.CharField(label='Add Title',widget = forms.TextInput(attrs={'autocomplete':'off'})) 
    body =  forms.CharField(label='', widget = forms.Textarea(attrs={'row':1,'cols':10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request,"encyclopedia/error.html",{
            "form": NewSearchForm()
        })
    else:
        html_content = markdown.markdown(util.get_entry(title))
        return render(request,"encyclopedia/entry.html", {
            "title": title,
            "html": html_content,
            "form": NewSearchForm()
        })

def search(request):
    if request.method == "POST":
        present = False
        form  = NewSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("query")
            for entry in util.list_entries():
                if data == entry:
                    html_content = markdown.markdown(util.get_entry(data))
                    present = True
                    break
            if present:
                return render(request,"encyclopedia/entry.html", {
                    "title": data,
                    "html": html_content,
                    "form": form
                    })
            else:
                l = []
                for entry in util.list_entries():
                    if data in entry:
                        l.append(entry)
                if len(l) == 0:
                    return render(request,"encyclopedia/error.html",{
                    "form": NewSearchForm()
                    })
                else:
                    return render(request,"encyclopedia/index.html", {
                        "entries": l,
                        "form": form
                    })
    else:
        return render(request,"encyclopedia/error.html",{
            "form": NewSearchForm()
        })        

def create(request):
    if request.method == "POST":
        cform = CreateNewForm(request.POST)
        if cform.is_valid():
            title = cform.cleaned_data["title"]
            body = cform.cleaned_data["body"]
            present = False
            for entry in util.list_entries():
                if title == entry:
                    present = True
                    break
            if present:
                return render(request,"encyclopedia/create_error.html",{
                    "form":NewSearchForm()
                })
            else:
                util.save_entry(title,body)
                html_content = markdown.markdown(util.get_entry(title))
                return render(request,"encyclopedia/entry.html",{
                    "title": title,
                    "html": html_content,
                    "form": NewSearchForm()
                }) 
                
    else:
        return render(request,"encyclopedia/create.html", {
            "form":NewSearchForm(),
            "cform":CreateNewForm()
        })

def edit(request, title):
    if request.method == "POST":
        editform = EditForm(request.POST)
        if editform.is_valid():
            title = editform.cleaned_data.get("title")
            body = editform.cleaned_data.get("body")
            # saving the new content
            util.save_entry(title, body)
            html_content = markdown.markdown(util.get_entry(title))
            return render(request,"encyclopedia/entry.html",{
                "title": title,
                "html": html_content,
                "form": NewSearchForm()
            })
    else:
        editform = EditForm({"title": title, "body": util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {"form": NewSearchForm(), "editform": editform})
 
def randoms(request):
    entries = util.list_entries()
    num = len(entries)
    # generating a random number for the entry
    entry = random.randint(0, num-1)
    title = entries[entry]
    html_content = markdown.markdown(util.get_entry(title))
    return render(request,"encyclopedia/randoms.html",{
        "form": NewSearchForm(),
        "title": title,
        "content": html_content
    })