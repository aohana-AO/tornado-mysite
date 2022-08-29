import requests
import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
import openpyxl


class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        form = PostForm(request.POST or None)
        return render(request, 'app/index.html', {
            'post_data': post_data, 'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        print(1)
        print(2)
        problemcategory = request.POST["problemcategory"]
        print(problemcategory)
        purpose = request.POST["purpose"]
        print(purpose)
        status = request.POST["status"]
        print(status)
        problemsize = request.POST["problemSize"]
        print(problemsize)
        organization = request.POST["organization"]
        print(organization)
        post_data = Post.objects.filter(problemCategory=problemcategory, purpose=purpose, status=status,
                                        problemSize=problemsize, organization=organization)

        if request.FILES:
            post_data.image = request.FILES.get('image')

        return render(request, 'app/index.html', {
            'post_data': post_data, 'form': form
        })


class MapItirannView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        form = PostForm(request.POST or None)
        return render(request, 'app/MapItirann.html', {
            'post_data': post_data, 'form': form
        })
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        print(1)
        print(2)
        problemcategory = request.POST["problemcategory"]
        print(problemcategory)
        purpose = request.POST["purpose"]
        print(purpose)
        status = request.POST["status"]
        print(status)
        problemsize = request.POST["problemSize"]
        print(problemsize)
        organization = request.POST["organization"]
        print(organization)
        post_data = Post.objects.filter(problemCategory=problemcategory, purpose=purpose, status=status,
                                        problemSize=problemsize, organization=organization)

        if request.FILES:
            post_data.image = request.FILES.get('image')

        return render(request, 'app/MapView.html', {
            'post_data': post_data, 'form': form
        })


class MapView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'app/MapView.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        print(1)
        print(2)
        problemcategory = request.POST["problemcategory"]
        print(problemcategory)
        purpose = request.POST["purpose"]
        print(purpose)
        status = request.POST["status"]
        print(status)
        problemsize = request.POST["problemSize"]
        print(problemsize)
        organization = request.POST["organization"]
        print(organization)
        post_data = Post.objects.filter(problemCategory=problemcategory, purpose=purpose, status=status,
                                        problemSize=problemsize, organization=organization)

        if request.FILES:
            post_data.image = request.FILES.get('image')

        return render(request, 'app/MapItirann.html', {
            'post_data': post_data, 'form': form
        })


class JuusyoMapView(TemplateView):
    template_name = 'app/juusyomap.html'


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {'post_data': post_data, 'user': user})


class CreatePostMap2(LoginRequiredMixin, View):
    def map(request, *args, **kwargs):
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        print(lat)
        form = PostForm(
            initial={

                'latitude': lat,
                'longitude': lng,

            }

        )
        return render(request, 'app/post_form.html', {
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


class CreatePostMap(LoginRequiredMixin, View):
    def map(request, *args, **kwargs):
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        print(lat)

        # 周辺地域
        url = 'http://geoapi.heartrails.com/api/json?method=searchByGeoLocation&x=' + str(lng) + '&y=' + str(lat)
        result = requests.get(url).json()
        x = 0
        tikaku = []
        try:
            print(result['response']['location'])
        except KeyError:
            return render(request, 'app/basyodetail_error.html')
        for i in result['response']['location']:
            print('〒' + result['response']['location'][x]['postal'], end='')
            print(result['response']['location'][x]['prefecture'], end='')
            print(result['response']['location'][x]['city'], end='')
            print(result['response']['location'][x]['town'], end='')
            print(' 緯度' + result['response']['location'][x]['x'], end='')
            print(' 経度' + result['response']['location'][x]['y'])
            tikaku.append({
                'yuubin': '〒' + result['response']['location'][x]['postal'],
                'juusyo': result['response']['location'][x]['prefecture'] +
                          result['response']['location'][x]['city'] + result['response']['location'][x]['town'],
                'lat': '緯度' + result['response']['location'][x]['x'],
                'lng': '経度' + result['response']['location'][x]['y'],
            }
            )
            x += 1

        # 住所
        url2 = 'https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat=' + lat + '&lon=' + lng
        result2 = requests.get(url2).json()

        try:
            print(result2['results'])
        except KeyError:
            return render(request, 'app/basyodetail_error.html')
        print(result2['results']['lv01Nm'])

        code = result2['results']['muniCd']
        mati = result2['results']['lv01Nm']

        datefile = 'app/000730858 (3).xlsx'
        X = pd.read_excel(datefile, engine='openpyxl', sheet_name='R1.5.1現在の団体', )

        X = X.rename(columns={'都道府県名\n（漢字）': '都道府県名', '市区町村名\n（漢字）': '市区町村名'})

        for index, r in X.iterrows():
            if str(r.団体コード)[:-1] == str(code):
                print(str(r.団体コード)[:-1])
                print(str(code))
                ken2 = r.都道府県名
                si = r.市区町村名

        try:
            print(ken2 + si + mati)
        except UnboundLocalError:
            return render(request, 'app/basyodetail_error.html')
        print(result2['results']['lv01Nm'])
        juusyo = ken2 + si + mati

        form = PostForm(
            initial={

                'address': juusyo,
                'latitude': lat,
                'longitude': lng,

            }

        )

        return render(request, 'app/post_form.html', {
            'form': form, "lat": lat, "lng": lng, 'juusyo': juusyo, 'tikaku': tikaku,
        })

    def post(request, *args, **kwargs):
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
            post_data.status = form.cleaned_data['status']
            post_data.problemSize = form.cleaned_data['problemSize']
            post_data.organization = form.cleaned_data['organization']

            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form': form
        })


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {
            'form': form
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
            post_data.status = form.cleaned_data['status']
            post_data.problemSize = form.cleaned_data['problemSize']
            post_data.organization = form.cleaned_data['organization']

            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form': form
        })


class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
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
        return render(request, 'app/post_form.html', {
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
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {'post_data': post_data})

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')
