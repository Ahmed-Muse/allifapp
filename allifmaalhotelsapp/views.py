from django.shortcuts import render

# Create your views here.
def hotelsHome(request,*allifargs,**allifkwargs):
  
    title="Hotel Home Page "
    context={
        "title":title,
    }
    return render(request,"allifmaalhotelsapp/home/home.html",context)
    