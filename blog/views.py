from django.shortcuts import render , HttpResponse , redirect
from .models import Post , BlogComment
from django.contrib import messages
# Create your views here.
def blogHome(request):
    post = Post.objects.all()
    content = {'post':post}
    return render(request,'blog/blogHome.html',content)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1 # for adding views
    post.save() # for saving views
    comments = BlogComment.objects.filter(post=post,parent=None) #parent=none is to not show reply in comment
    replies = BlogComment.objects.filter(post=post).exclude(parent=None) #for reply
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]

        else:
            replyDict[reply.parent.sno].append(reply) #end reply portion
    content = {'post':post , 'comments':comments , 'user':request.user, 'replyDict': replyDict} #user here is for authentication
    return render(request,'blog/blogPost.html',content)


# API for posting comment
def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno') #for reply
        if parentSno == "":
            comment = BlogComment(comment=comment,user=user, post=post)
            comment.save()
            messages.success(request,'Your message has been comment succesfully')

        else: #for reply
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, 'Your reply has been comment succesfully')

    return redirect(f"/blog/{post.slug}")
