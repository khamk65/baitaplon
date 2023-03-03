import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Nongnghiep.models import Coso, CustomUser,Staffs, LoaiCoso, giayphep, Vungchannuoi

def staff_home(request):
    return render(request, "staff_template/staff_profile.html")
def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))

def Them_loai_co_so(request):
    return render(request, "staff_template/Quan_ly_loai_co_so.html")

def Luu_them_thong_tin_loai_co_so(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ten_co_so=request.POST.get("coso")
        try:
            coso=LoaiCoso()
            coso.tencoso=ten_co_so
            coso.save()
            messages.success(request,"Thêm thành công")
            return HttpResponseRedirect(reverse("Them_loai_co_so"))
        except:
            messages.error(request,"Thêm thất bại")
            return HttpResponseRedirect(reverse("Them_loai_co_so"))

def Them_co_so(request):
    loai = LoaiCoso.objects.all()
    return render(request,"staff_template/ThemCoso.html",{"loais": loai})

def Luu_co_so(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        tencoso=request.POST.get("tencoso")
        loai_id = LoaiCoso(id=request.POST.get("loai"))
        leader = request.POST.get("leader")
        diadiem = request.POST.get("diadiem")
        sanpham= request.POST.get("sanpham")
        startdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")
        try:
            coso=Coso()
            coso.tencoso=tencoso
            coso.nguoidungdau=leader
            coso.loaicoso_id=loai_id
            coso.tensanpham=sanpham
            coso.diadiem=diadiem
            coso.ngaybatdau=startdate
            coso.ngayhethan=enddate
            coso.save()
            messages.success(request,"Thêm thành công")
            return HttpResponseRedirect(reverse("Them_co_so"))
        except:
            messages.error(request,"Thêm thất bại")
            return HttpResponseRedirect(reverse("Them_co_so"))

def QuanLyCoSo(request):
    cosos=Coso.objects.all()
    return render(request,"staff_template/QuanlyCoso.html",{"cosos":cosos})

def Sua_co_so(request, coso_id):
    coso=Coso.objects.get(id=coso_id)
    loais=LoaiCoso.objects.all()
    return render(request,"staff_template/Suacoso.html",{"coso": coso, "loais": loais})

def Luu_sua_co_so(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        coso_id = request.POST.get("coso_id")
        tencoso = request.POST.get("tencoso")
        loai_id = request.POST.get("loai")
        loai_id = LoaiCoso.objects.get(id=loai_id)
        leader = request.POST.get("leader")
        sanpham = request.POST.get("sanpham")
        diadiem = request.POST.get("diadiem")
        startdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")
        try:
            coso = Coso.objects.get(id=coso_id)
            coso.tencoso=tencoso
            coso.loaicoso_id = loai_id
            coso.nguoidungdau=leader
            coso.tensanpham=sanpham
            coso.diadiem=diadiem
            coso.ngaybatdau=startdate
            coso.ngayhethan=enddate
            coso.save()
            messages.success(request,"Sửa thông tin thành công")
            return HttpResponseRedirect(reverse("Sua_co_so",kwargs={"coso_id":coso_id}))
        except:
            messages.error(request,"Sửa thông tin thất bại")
            return HttpResponseRedirect(reverse("Sua_co_so",kwargs={"coso_id":coso_id}))


def ThemVungChanNuoi(request):
    staffs = Staffs.objects.all()
    giaypheps = giayphep.objects.all()
    return render(request, "staff_template/ThemVungChanNuoi.html",{"staffs": staffs, "giaypheps": giaypheps})

def LuuVungChanNuoi(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        Diachi = request.POST.get("Diachi")
        leader = Staffs.objects.get(id=request.POST.get("leader"))
        dieukien = request.POST.get("dieukien")
        giayphep_ = giayphep.objects.get(id=request.POST.get("giayphep"))
        try:
            vungchannuoi = Vungchannuoi()
            vungchannuoi.diadiem = Diachi
            vungchannuoi.nguoiquanly= leader
            vungchannuoi.dieukienchannuoi= dieukien
            vungchannuoi.giayphep_id=giayphep_
            vungchannuoi.save()
            messages.success(request, "Thêm thông tin thành công")
            return HttpResponseRedirect(reverse("Them_vung_chan_nuoi"))
        except:
            messages.error(request, "Thêm thông tin thất bại")
            return HttpResponseRedirect(reverse("Them_vung_chan_nuoi"))

def QuanLyVungChanNuoi(request):
    vungchannuoi = Vungchannuoi.objects.all()
    return render(request,"staff_template/QuanLyVungChanNuoi.html",{"vungs": vungchannuoi})

def SuaVungChanNuoi(request, vung_id):
    vungchannuoi = Vungchannuoi.objects.get(id=vung_id)
    staffs = Staffs.objects.all()
    giaypheps = giayphep.objects.all()
    return render(request,"staff_template/SuaVungChanNuoi.html", {"vung": vungchannuoi, "staffs": staffs, "giaypheps": giaypheps})

def Luu_Sua_Vung_Chan_Chan_Nuoi(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        vung_id = request.POST.get("vung_id")
        print(type(vung_id))
        Diachi = request.POST.get("Diachi")
        leader = Staffs.objects.get(id=request.POST.get("leader"))
        dieukien = request.POST.get("dieukien")
        giayphep_ = giayphep.objects.get(id=request.POST.get("giayphep"))
        try:
            vungchannuoi = Vungchannuoi(id = vung_id)
            vungchannuoi.diadiem = Diachi
            vungchannuoi.nguoiquanly= leader
            vungchannuoi.dieukienchannuoi= dieukien
            vungchannuoi.giayphep_id=giayphep_
            vungchannuoi.save()
            messages.success(request, "Thêm thông tin thành công")
            return HttpResponseRedirect(reverse("Sua_vung_chan_nuoi", kwargs={"vung_id": vung_id}))
        except:
            messages.error(request, "Thêm thông tin thất bại")
            return HttpResponseRedirect(reverse("Sua_vung_chan_nuoi", kwargs={"vung_id": vung_id}))
