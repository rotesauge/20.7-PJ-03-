from django.shortcuts import render
from .models import Post,Message,BaseRegisterForm,OneTimeCode
from django.views.generic import (ListView, DetailView, CreateView,UpdateView,DeleteView)
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .forms import PostForm,MessageForm,LoginForm,CodeForm
from django.urls import reverse_lazy,reverse
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
import secrets
import string

# в декоратор передаётся первым аргументом сигнал,
# на который будет реагировать эта функция,
# и в отправители надо передать также модель
#
@receiver(post_save, sender=Message)
def notify_message_create(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject        = 'Отклик на объявление '+ f'{instance.post.caption}',
            message        = instance.text,  # сообщение с кратким описанием проблемы
            from_email     = 'rotesauge@aiq.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list = [instance.post.author.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

def create_code():
    digits = string.digits
    pwd_length = 6
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(digits))
    return pwd

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # Проверяем учетные данные
            if user is not None:
                request.session['pk'] = user.pk
                return redirect('/login_code/')  # Перенаправляем на главную страницу
    return render(request, 'sign\login.html', {'form': form})

def login_code_view(request):
    form = CodeForm(data=request.POST or None)
    if request.method == 'POST':
       # if form.is_valid():
        pk = request.session.get('pk')
        user = User.objects.get(pk=pk)
        code = form.data['code']
        codeobj =  OneTimeCode.objects.filter(user=user, code=code)
        if codeobj:
            login(request, user)  # Выполняем вход
            codeobj.delete()
            return redirect('/')  # Перенаправляем на главную страницу
    else:
        pk = request.session.get('pk')
        user = User.objects.get(pk=pk)
        code = create_code()
        OneTimeCode.objects.create(user=user, code=code)
        send_mail(subject='Аутентификация ',
              message='одноразовый пароль ' + f'{code}',
              from_email='rotesauge@aiq.ru',
              recipient_list=[user.email])
    return render(request, 'sign\login_veryfy.html', {'form': form})
###########################################################
############################################################
############################################################
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
############################################################
############################################################
############################################################
class Posts(ListView):
    model = Post
    ordering = 'datetime'
    template_name = 'Posts.html'
    context_object_name = 'news'

class PostV(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = (self.request.user == self.object.author)
        return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'Post_Edit.html'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'Post_Edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
##################################################################
##################################################################
##################################################################
class Messages(ListView):
    #queryset = Message.objects.filter(author=self.user)
    model = Message
    template_name = 'Messages.html'
    context_object_name = 'messages'
    def get_initial(self):
        self.queryset = Message.objects.filter(post__author=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['res'] = self.request.user
        return context

class MessageV(DetailView):
    model = Message
    template_name = 'Message.html'
    context_object_name = 'message'

class MessageCreate(CreateView):
    form_class = MessageForm
    model = Message
    template_name = 'Message_Edit.html'
    vpostid = 0
    def get_initial(self):
        postid = self.request.GET.get("postid", None)
        if postid:
            self.vpostid = postid
    def form_valid(self, form):
        message = form.save(commit=False)
        message.post = Post.objects.get(id=self.vpostid)
        message.sender = self.request.user
        return super().form_valid(form)

class MessageUpdate(UpdateView):
    form_class = MessageForm
    model = Message
    template_name = 'Message_Edit.html'


class MessageDelete(DeleteView):
    model = Message
    template_name = 'Message_delete.html'
    success_url = reverse_lazy('news')

def accept_message(request):
    msgid = request.GET.get("msgid", None)
    postid = request.GET.get("postid", None)
    if msgid:
#        msg = Message.objects.filter(id=msgid).first()
        msg = Message.objects.get(id=msgid)
        msg.accepted = True
        msg.save()
        pst = Post.objects.get(id=postid)
        send_mail(
            subject        = 'Ваш отклик на объявление принят',
            message        = 'Текст  '
                             + f'{msg.text}'
                             + '\n Пост'
                             + f'{pst.text}',
            from_email     = 'rotesauge@aiq.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list = [msg.sender.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
                 )
    return redirect('/content/posts/'+postid)