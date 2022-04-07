# Importando a funcionalidade render do Django, para renderizar a página:
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


# Views
def frontpage(request):
    return render(request, 'core/frontpage.html')


def privacidade(request):
    return render(request, 'core/privacy.html')


def termos(request):
    return render(request, 'core/terms.html')


def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()

            userprofile = Userprofile.objects.create(user=user)

            login(request, user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})