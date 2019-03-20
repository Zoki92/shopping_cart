from django.shortcuts import render
from .models import Profile
# Create your views here.


def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    context = {
        'my_user_profile': my_user_profile,
    }

    return render(request, 'profile.html', context)