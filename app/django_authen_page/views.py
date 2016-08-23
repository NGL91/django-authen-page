from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'base.html')
	if request.user.is_authenticated():
	    return render(request, 'base.html')
	else:
	    return render(request, 'django_authen_page/login.html')