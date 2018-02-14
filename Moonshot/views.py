from django.shortcuts import render, redirect
frmo django.contrib.auth import authenticate, login
from django.views.generic import view
from .forms import UserForm


class UserForm(View):
    form_class = UserForm
    template_name = 'Moonshot/registration_form.html'

    #display blank form
    def get(selfself, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    #process form data
    def post(selfSelf, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #return user object if credentials are correct

            user=authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(reques, user)
                    return redirect('Moonshot/index.html')

        return render(request, self.template_name, {'form': form})