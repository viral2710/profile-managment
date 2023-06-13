from django.db import models



class Profile(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    password = models.CharField(max_length=30, null=False)


class UserPermission(models.Model):
    is_super_user = models.BooleanField(default=False)
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=255,null=True)
