from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.urls import reverse_lazy,reverse
# Create your models here.

tanks         = 'TN'
healers       = 'HL'
damagedealers = 'DD'
merchants     = 'MC'
guildmasters  = 'GM'
questgivers   = 'QG'
blacksmiths   = 'BS'
tanners       = 'TR'
potionmakers  = 'PM'
spellmasters  = 'SM'

CATEGORY = [(tanks,         'Танки'),
            (healers,       'Хилы'),
            (damagedealers, 'ДД'),
            (merchants,     'Торговцы'),
            (guildmasters,  'Гилдмастеры'),
            (questgivers,   'Квестгиверы'),
            (blacksmiths,   'Кузнецы'),
            (tanners,       'Кожевники'),
            (potionmakers,  'Зельевары'),
            (spellmasters,  'Мастера заклинаний')]

class Post(models.Model):
    #id = models.IntegerField(default=1, primary_key = True)
    author   = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                blank=True,
                                default = 1,related_name="author")
    likers   = models.ManyToManyField(User, null=True, blank=True,related_name="likers")
    caption  = models.CharField(null=True, max_length=64, blank=True)
    text     = models.CharField(null=True, max_length=1024, blank=True)
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    сategory = models.CharField(max_length=2,
                                choices=CATEGORY,
                                default=tanks)
    def GetMessages(self):
        return Message.objects.filter(post = self)



class Message(models.Model):
    post     = models.ForeignKey(Post, on_delete=models.CASCADE, default=1, blank=True)
    sender   = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=True, default=1,related_name="sender")
    receiver = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 blank=True, default=1,related_name="receiver")
    text     = models.CharField(null=True, max_length=1024, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('message', args=[str(self.id)])

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class OneTimeCode(models.Model):
    user   = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                blank=True,
                                 default = 1)
    code  = models.CharField(null=True, max_length=64, blank=True)
