from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()


class LoaiCoso(models.Model):
    id = models.AutoField(primary_key=True)
    tencoso = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Coso(models.Model):
    id = models.AutoField(primary_key=True)
    tencoso = models.CharField(max_length=255)
    nguoidungdau = models.TextField()
    loaicoso_id = models.ForeignKey(LoaiCoso, on_delete=models.CASCADE, default=1)
    tensanpham = models.TextField()
    diadiem = models.TextField()
    ngaybatdau = models.DateTimeField()
    ngayhethan = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class tochuccapphep(models.Model):
    id = models.AutoField(primary_key=True)
    diadiem = models.TextField()
    nguoidungdau = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    objects = models.Manager()

class giayphep(models.Model):
    id = models.AutoField(primary_key=True)
    ngaybatdau= models.DateTimeField()
    ngayhethan = models.DateTimeField()
    tochuccapphep_id = models.ForeignKey(tochuccapphep, on_delete=models.CASCADE)


class Vungchannuoi(models.Model):
    id = models.AutoField(primary_key=True)
    diadiem = models.TextField()
    nguoiquanly = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    dieukienchannuoi = models.BooleanField(default=False)
    giayphep_id = models.ForeignKey(giayphep, on_delete=models.CASCADE)

class Chicucthuy(models.Model):
    id = models.AutoField(primary_key=True)
    diadiem = models.TextField()
    Email = models.EmailField()

class Dailybanthuoc(models.Model):
    id = models.AutoField(primary_key=True)
    diadiem = models.TextField()
    loaisanpham = models.TextField()
    giayphep_id = models.ForeignKey(giayphep, on_delete=models.CASCADE)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance, address="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()