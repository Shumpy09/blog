from typing import ContextManager
from blogs.models import BlogPost
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404


from .models import BlogPost
from .forms import BlogPostForm
# Create your views here.

def index(request):
    """Strona główna dla aplikacji Blog"""
    #posts = BlogPost.objects.order_by('date_added')

    #context = {'posts': posts}
    return render(request, 'blogs/index.html')

def posts(request):
    """Strona główna z postami"""
    posts = BlogPost.objects.order_by('date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

@login_required
def new_post(request):
    """Dodaj nowy post"""

    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = BlogPostForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user

            if new_post.owner != request.user:
                raise Http404
            else:
                new_post.save()
                #form.save()
                return redirect('blogs:posts')
                #return redirect('blogs:index')

    # wyświetlenie pustego formularza
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edycja istniejącego posta"""
    post = BlogPost.objects.get(id=post_id)
    
    if post.owner != request.user:
        raise Http404
        
    if request.method != 'POST':
        # Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu
        form = BlogPostForm(instance=post)
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = BlogPostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            #return redirect('blogs:index')
            return redirect('blogs:posts')

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

