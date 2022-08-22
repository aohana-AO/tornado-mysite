from django.shortcuts import render
from django.views.generic import View
from .models import Post

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