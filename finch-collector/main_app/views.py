from django.shortcuts import render, redirect
from .models import Finch, Toy, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm, PhotoForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def finch_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {
        'finches': finches    
    })



@login_required
def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    photo_form = PhotoForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'feeding_form': feeding_form,
        'photo_form': photo_form,
        'toys': toys_finch_doesnt_have
    })





class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/finches/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    # main-app/views.py



class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']


class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'


@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('finch-detail', finch_id=finch_id)



class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'



class ToyList(LoginRequiredMixin, ListView):
    model = Toy



class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy    



class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']



class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'    

@login_required
def associate_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('finch-detail', finch_id=finch_id)


@login_required
def remove_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('finch-detail', finch_id=finch_id)



@login_required
def add_photo(request, finch_id):
    form = PhotoForm(request.POST)
    if form.is_valid():
        new_photo = form.save(commit=False)
        new_photo.finch_id = finch_id
        finch_photo = Photo.objects.filter(finch_id=finch_id)
        if finch_photo.first():
            finch_photo.first().delete()
        new_photo.save()
    return redirect('finch-detail', finch_id=finch_id)



def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('finch-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )