import json

import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Nongnghiep.models import CustomUser, AdminHOD, Staffs, LoaiCoso, Coso, tochuccapphep, giayphep


def admin_home(request):
    return render(request, "hod_template/home_content.html")

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def add_staff(request):
    return render(request, "hod_template/ThemNhanVien.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/QuanLyNhanVien.html",{"staffs":staffs})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/SuaNhanVien.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def QuanLyToChucCapPhep(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/QuanLyToChucCapPhep.html", {"staffs": staffs})

def LuuToChucCapPhep(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        diadiem = request.POST.get("diadiem")
        leader = Staffs.objects.get(id=request.POST.get("leader"))
        try:
            tochuc = tochuccapphep()
            tochuc.diadiem = diadiem
            tochuc.nguoidungdau = leader
            tochuc.save()
            messages.success(request, "Thêm thông tin thành công")
            return HttpResponseRedirect(reverse("Quan_ly_to_chuc_cap_phep"))
        except:
            messages.error(request, "Thêm thông tin thất bại")
            return HttpResponseRedirect(reverse("Quan_ly_to_chuc_cap_phep"))

def QuanLyGiayPhep(request):
    tochucs = tochuccapphep.objects.all()
    return render(request, "hod_template/QuanLyGiayPhep.html", {"tochucs":tochucs})

def LuuGiayPhep(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        startday = request.POST.get("startday")
        endday = request.POST.get("endday")
        tochuc = tochuccapphep.objects.get(id=request.POST.get("tochuc"))
        try:
            giayphep_ = giayphep()
            giayphep_.ngaybatdau = startday
            giayphep_.ngayhethan = endday
            giayphep_.tochuccapphep_id = tochuc
            giayphep_.save()
            messages.success(request, "Thêm thông tin thành công")
            return HttpResponseRedirect(reverse("Quan_ly_giay_phep"))
        except:
            messages.error(request, "Thêm thông tin thất bại")
            return HttpResponseRedirect(reverse("Quan_ly_giay_phep"))