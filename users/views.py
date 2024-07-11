from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UserUpdateForm


class UserRegistrationView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)




class UserLoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('landing_page')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        context = {
            'form': user_update_form,
            'user': request.user
        }

        return render(request, 'users/profile.html',context)

    def post(self, request):
        user_update_form = UserUpdateForm(request.POST,
                    instance=request.user,
                    files=request.FILES)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('users:profile')

        return render(request, 'users/profile-edit.html', {'form': user_update_form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('landing_page')

