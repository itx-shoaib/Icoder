from django.shortcuts import render , HttpResponse , redirect
from .models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# HTML file functions
def home(request):
    post = Post.objects.all()
    content = {'post':post}
    return render(request,'home/home.html',content)

def contact(request):
    if request.method == 'POST':
        # name in [ ] is name from contact form
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<2 or len(phone)<5 or len(content)<4:
            messages.error(request,"PLease addd your form corectly")

        else:
            contact = Contact(name = name , email=email, phone=phone , content=content)
            contact.save()
            messages.success(request, "Your form has been successfully submit.")
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        post = Post.objects.none()
    else:
        postTitle = Post.objects.filter(title__icontains = query)
        postContent = Post.objects.filter(content__icontains = query)
        postAuthor = Post.objects.filter(author__icontains = query)
        post = postTitle.union(postContent,postAuthor)
    if post.count() == 0:
        messages.warning(request,"No search found.Please search relevant query.")
    content = {'post':post,'query':query}
    return render(request,'home/search.html',content)

# Authentication APIS

def handleSignUp(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

#         Check for errorneous input
        if len(username)<10:
            messages.error(request,' Your user name must be under 10 characters')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, ' User name should only contain letters and numbers')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, ' Password must be match.')
            return redirect('home')

#         Create the user
        myuser = User.objects.create_user(username,pass1,email)
        myuser.fname = fname
        myuser.lname = lname
        myuser.save()
        messages.success(request,'You have sign up.')
        return redirect('home')

    else:
        return HttpResponse("404 - user not found")


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username = loginusername , password = loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully login.')
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials! Please try again')
            return redirect('home')
    # return HttpResponse("This is log in")

def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully logout.')
    return redirect('home')
    # return HttpResponse("This is log out")

