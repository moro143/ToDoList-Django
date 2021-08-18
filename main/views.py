from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList


# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():
        print(ls.time_created)
        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c"+str(item.id))=="clicked":
                        item.complited = True
                    else:
                        item.complited = False
                    item.text = response.POST.get("t"+str(item.id))
                    item.save()
                ls.name = response.POST.get("lsn"+str(ls.id))
                ls.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complited=False)
                else:
                    print("invalid")
            elif response.POST.get("deleteItem"):
                id = int(response.POST["deleteItem"])
                Item.objects.filter(id=id).delete()

        return render(response, "main/list.html", {"ls":ls,'response':response})
    return render(response, "main/view.html", {'response':response})

def home(response):
    print(response.user.is_authenticated)
    return render(response, "main/home.html", {'response':response})

def create(response):
    if response.user.is_authenticated:
        if response.method == "POST":
            form = CreateNewList(response.POST)
            if form.is_valid():
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
                response.user.todolist.add(t)

            return HttpResponseRedirect("/%i" %t.id)
        else:
            form = CreateNewList()
        return render(response, "main/create.html", {"form": form,'response':response})
    else:
        return redirect("/login")

def view(response):
    if response.method == "POST":
        if response.POST.get("deleteList"):
            id = int(response.POST["deleteList"])
            ToDoList.objects.filter(id=id).delete()
    return render(response, "main/view.html", {'response':response})