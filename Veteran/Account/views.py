from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import User

from .models import HostApplication



# Create your views here.
#수정필요
def login(request):
    if request.method=="POST":
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')           
            user=auth.authenticate(
                request=request,
                username=username,
                password=password
            )
            if user is not None:
                auth.login(request,user)
                return redirect('Account:login')
        return redirect('Game:gamelist')
    else:
        form=AuthenticationForm()
        return render(request,'Account/welcome_login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('Account:login')
    

##수정필요
def signup(request):
    if request.method == "POST":
        if request.POST['pw'] == request.POST['cpw']:
            user = User.objects.create_user(username=request.POST['email'], password=request.POST['pw'], nickname=request.POST['nickname'], phone=request.POST['phone'])
            auth.login(request,user)
            return redirect('Game:gamelist')
    return render(request,'Account/join_page.html')
    
def mypage(request):
    return render(request, 'Account/myinfo.html')

def hostapply(request):
    return render(request, 'Account/Host Application.html')

def apply(request):
    host = HostApplication()
    host.host = request.Get["username"]
    host.group_name = request.Get["team_name"]
    host.court_location = request.Get["field"]
    host.intro = request.Get["intro"]
    host.save()
    return redirect('Account/myinfo.html')


   
def hostapprove(request):
    contents = HostApplication.objects.all()
    return render(request, 'Account/Host approval.html', {'host_list': contents})


from django.contrib.auth.mixins import PermissionRequiredMixin

class CreateWorkView(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'main.add_work'
    # 여러 권한
    # permission_required = ('polls.can_open', 'polls.can_edit')
    model = Work
    form_class = WorkForm
    template_name = 'main/work_form.html'

    def get_success_url(self):
        return reverse('index')
    