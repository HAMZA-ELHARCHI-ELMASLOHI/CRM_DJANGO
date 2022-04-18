import email
from django.db import models

from django.db.models.signals import post_save

from account.models import User
# Create your models here.








class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='images/profile')
    name=models.CharField(max_length=20, null=True)
    email=models.EmailField(null=True)
    age=models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.user.username





def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, name=instance.username)


post_save.connect(post_user_created_signal, sender=User) 