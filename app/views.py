from django.shortcuts import render,redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self,request,*args, **kwargs):
        post_data=Post.objects.order_by('-id')
        return render(request,'app/index.html',{
            'post_data':post_data
        })
class PostDetailView(View):
    def get(self,request,*args, **kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        return render(request,'app/post_detail.html',{'post_data':post_data})
class CreatePostView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        form=PostForm(request.POST or None)
        return render(request,'app/post_form.html',{
            'form':form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.address = form.cleaned_data['address']
            post_data.latitude = form.cleaned_data['latitude']
            post_data.longitude = form.cleaned_data['longitude']
            post_data.problemCategory = form.cleaned_data['problemCategory']
            post_data.peopleNum = form.cleaned_data['peopleNum']
            post_data.purpose = form.cleaned_data['purpose']
            post_data.status = form.cleaned_data['status ']
            post_data.problemSize = form.cleaned_data['problemSize']
            post_data.organization = form.cleaned_data['organization']

            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form': form
        })

class PostEditView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'content': post_data.content,
                'author': post_data.author,
                'address': post_data.address,
                'latitude': post_data.latitude,
                'longitude': post_data.longitude,
                'status': post_data.status,
                'organization': post_data.organization,
                'peopleNum': post_data.peopleNum,
                'problemCategory': post_data.problemCategory,
                'problemSize': post_data.problemSize,
                'purpose': post_data.purpose,

            }


        )
        return render(request, 'app/post_form.html',{
            'form': form
        })

    def post(self, request, *args, **kwargs):

        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.address = form.cleaned_data['address']
            post_data.latitude = form.cleaned_data['latitude']

            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {
            'form': form
        })
class PostDeleteView(View):
    def get(self,request,*args, **kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        return render(request,'app/post_delete.html',{'post_data':post_data})

    def post(self,request,*args, **kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')