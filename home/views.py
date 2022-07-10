from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Member
from .library.validate.validate import Validate
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urljoin

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('member-list')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('member-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('member-list')
        return super(RegisterPage, self).get(*args, **kwargs)


class ListPage(LoginRequiredMixin, ListView):
    model = Member
    context_object_name = 'members'
    template_name = 'list.html'
  
    
class AddPage(LoginRequiredMixin, TemplateView):
    template_name = 'add.html'
    
    def post(self, request):
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        phoneNumber = request.POST['phone_number']
        email = request.POST['email']
        v = Validate()
        
        if not v.isString(firstName) or \
            not v.isString(lastName) or \
            not v.isEmail(email) or \
            not v.isPhoneNumber(phoneNumber):
                return render(request, self.template_name, {'error':True})
        
        userName = request.POST['first_name']+request.POST['last_name']
        
        try:
            user = User.objects.create(
                first_name=firstName,
                last_name=lastName,
                username=userName,
                email=email,
            )
        except Exception as e:
            print(e)
            return render(request, self.template_name, {'error':True})
        

        Member.objects.create(
            phone_number=phoneNumber,
            user_id=user.id,
        )
        
        return redirect('member-list')
    
    
class EditPage(LoginRequiredMixin, TemplateView):
    template_name = 'edit.html'
    
    def get_context_data(self, *arg, **kwargs):
        context = super(EditPage, self).get_context_data(*arg, **kwargs)
        context['error'] = self.request.GET.get('error',False)
        
        try:
            memberRecord = Member.objects.get(id=self.kwargs.get('memberId'))
            context['member'] = memberRecord
        except:
            pass

        return context
    
    def post(self, request, **kwargs):
        try:
            memberRecord = Member.objects.get(id=self.kwargs.get('memberId'))
        except Exception as e:
            return redirect('customer_profile', pk=order.customer_id)
        
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        phoneNumber = request.POST['phone_number']
        email = request.POST['email']
        v = Validate()
        
        if not v.isString(firstName) or \
            not v.isString(lastName) or \
            not v.isEmail(email) or \
            not v.isPhoneNumber(phoneNumber):
                return HttpResponseRedirect('/edit/'+str(self.kwargs.get('memberId'))+'?error=True')
        

        memberRecord.phone_number = phoneNumber
        memberRecord.save()
        
        userRecord = User.objects.get(id=memberRecord.user_id)
        userRecord.first_name = firstName
        userRecord.last_name = lastName
        userRecord.email = email
        userRecord.save()
        

        return redirect('member-list')
    
    
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    context_object_name = 'member'
    success_url = reverse_lazy('member-list')
    template_name = 'delete.html'

    def get_context_data(self, *arg, **kwargs):
        context = super(DeleteView, self).get_context_data(*arg, **kwargs)
        context['memberId'] = self.kwargs.get('pk')
        
        return context
    
    def post(self, *arg, **kwargs):
        try:
            record = Member.objects.select_related('user').get(id=self.kwargs.get('pk'))
            record.user.delete()
            record.delete()
        except Exception as e:
            print(e)
        
        return redirect('member-list')