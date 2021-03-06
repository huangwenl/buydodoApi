# -*- coding: UTF-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from testenvData.models import envdata, serverdata, mobileInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import datetime
from utils.commonTool.httpUtil import HttpUtil
from utils.commonTool.mySqlUtil import MysqlUtil
from utils.log.mylog import MyLogger

log = MyLogger()


# Create your views here.
def testenv(request):
    testdata = envdata.objects.all()
    log.info("查询数据库数据testdata为%s" % testdata)
    datalist = []
    for i in testdata:
        data = {"id": "", "env": "", "channle": "", "role": "", "phone": "", "password": ""}
        data["id"] = i.id
        data["env"] = i.env
        data["channle"] = i.channle
        data["role"] = i.role
        data["phone"] = i.phone
        data["password"] = i.password
        datalist.append(data)
    return render(request, "testenv.html", {"data": datalist})


# 分页功能
def data_manage(request):
    # data_list = envdata.objects.all()
    data_list = envdata.objects.get_queryset().order_by('id')
    log.info("查询所有测试账号信息%s" % data_list)
    paginator = Paginator(data_list, 10)
    page = request.GET.get("page")
    log.info("请求分页数据,请求页码为%s" % page)
    try:
        data = paginator.page(page)
        log.info("请求第%s页数据为%s" % (page, data))
    except PageNotAnInteger:
        data = paginator.page(1)
        log.info("页码不为数字,强制转成1")
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        log.info("EmptyPage")
    return render(request, "testenv.html", {"data": data})


def fixedAssets(request):
    datas = mobileInfo.objects.get_queryset().order_by('id')
    log.info("查询所有测试机信息%s" % datas)
    paginator = Paginator(datas, 10)
    page = request.GET.get("page")
    log.info("请求分页数据,请求页码为%s" % page)
    try:
        data = paginator.page(page)
        log.info("请求第%s页数据为%s" % (page, data))
    except PageNotAnInteger:
        data = paginator.page(1)
        log.info("页码不为数字,强制转成1")
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        log.info("EmptyPage")
    return render(request, "fixedAssets.html", {"data": data})


def addenvdata(request):
    datas = envdata()
    data = request.POST["data"]
    log.info("请求添加测试账号信息,请求数据为%s" % data)
    if len(data) < 0:
        log.info("请求数据为空，直接返回")
        return HttpResponse(0)
    try:
        list = data.split("&")
        l = []
        for i in list[2:]:
            l.append(i.split("=")[1])
        datas.env = l[0]
        datas.channle = l[1]
        datas.role = l[2]
        datas.phone = l[3]
        datas.password = l[4]
        datas.save()
        log.info("添加保存成功")
    except Exception as e:
        log.info("保存测试账号信息异常,直接返回")
        return HttpResponse(0)
    else:
        return HttpResponse(200)


def update(request):
    data = request.POST.get("data")
    log.info("请求更新测试账号信息,请求数据为%s" % data)
    if len(data) <= 0:
        log.info("请求数据为空，直接返回")
        return HttpResponse(0)
    try:
        list = data.split("&")
        l = []
        for i in list[1:]:
            l.append(i.split("=")[1])
        # for i in l:
        #     print(i)
        id = l[0]
        env = l[1]
        channle = l[2]
        role = l[3]
        phone = l[4]
        password = l[5]
        data = envdata.objects.get(id=id)
        data.env = env
        data.channle = channle
        data.role = role
        data.phone = phone
        data.password = password
        data.save()
        log.info("更新保存成功")
    except Exception as e:
        log.info("更新保存测试账号信息异常,直接返回")
        return HttpResponse(0)
    else:
        return HttpResponse(200)


def delSelect(request):
    arr = request.GET.get("arr")
    log.info("删除测试账号数据,请求删除数据为%s" % arr)
    arrlist = arr.split(",")
    try:
        for i in arrlist:
            if len(i) <= 0:
                pass
            else:
                d = envdata.objects.get(id=i)
                d.delete()
                log.info("删除成功")
    except Exception as e:
        log.info("删除测试账号信息异常,直接返回%s" % e)
        return HttpResponse(0)
    else:
        return HttpResponse(200)


def query(request):
    phone_num = request.GET.get("input_phone", "")
    log.info("查询账号信息，输入的要查询的手机号码为%s" % phone_num)
    if len(phone_num) <= 0 or len(phone_num) >= 11:
        log.info("查询账号信息，输入的要查询的手机号码为太短或是太长")
        return HttpResponseRedirect("/testenvData/data_manage/")
    datas = envdata.objects.filter(phone__contains=phone_num)
    log.info("数据库查询的匹配输入的手机号码信息为%s" % datas)
    if len(datas) <= 0:
        return render(request, "testenv.html")
    list = []
    for d in datas:
        data = {"id": "", "env": "", "channle": "", "role": "", "phone": "", "password": ""}
        data["id"] = d.id
        data["env"] = d.env
        data["channle"] = d.channle
        data["role"] = d.role
        data["phone"] = d.phone
        data["password"] = d.password
        list.append(data)
    return render(request, "testenv.html", {"data": list})


def server_data(request):
    return render(request, "serverdata.html")


def query_serverdatas(request):
    data_list = []
    serverdatas = serverdata.objects.get_queryset().order_by("id")
    for d in serverdatas:
        data_json = {"id": "", "env": "", "ip": "", "port": "",
                     "user": "", "password": "", "isAvailable": "", "time": ""}
        data_json["id"] = d.id
        data_json["env"] = d.env
        data_json["ip"] = d.ip
        data_json["port"] = d.port
        data_json["user"] = d.user
        data_json["password"] = d.password
        data_json["isAvailable"] = d.isAvailable
        t = datetime.datetime.strftime(d.time, "%Y-%m-%d %H:%M:%S")
        data_json["time"] = t
        data_list.append(data_json)

    return JsonResponse({"data": data_list})


def update_serverdatas(request):
    methods = request.method
    if methods == "GET":
        return HttpResponseRedirect("/query_serverdatas/")
    if methods == "POST":
        params = request.POST.get("data")
        """params = 1&port&6666"""
        if params:
            param_list = params.split("&")
            data = serverdata.objects.get(id=param_list[0])
            data.setattr(param_list[1], param_list[2])
            data.save()
            return JsonResponse({"code": 200, "status": "success"})
        else:
            return JsonResponse({"code": 400, "status": "fail"})
    else:
        return JsonResponse({"code": 400, "status": "fail"})


def datastation(request):
    return render(request, "data_station.html")


def register(request):
    methods = request.method
    if methods == "GET":
        return JsonResponse({"code": 400, "status": "fail"})
    if methods == "POST":
        params = request.POST.get("data")
        if params:
            params_list = params.split("&")
            phone = params_list[1].split("=")[1]
            env = int(params_list[2].split("=")[1])
            role = int(params_list[3].split("=")[1])
            status = int(params_list[4].split("=")[1])
            print(phone, env, role, status)
            sms_data = "client=iOS&clientVersion=1.0&d_model=iPhone&mobile=" + phone + "&networkType=WiFi&osVersion=11.0.3&type=1"
            try:
                if env == 0:
                    pass
                if env == 1:
                    if role == 0:
                        confFile = "\\config\\buydodoInterface.yml"
                        response_sms = HttpUtil.post(confSection="SendMessage-Interface", confFile=confFile,
                                                     data=sms_data)
                        print(response_sms)
                        mysql = MysqlUtil()
                        sql_Str = "SELECT * from t_sms_short_message WHERE mobile = %s;" % (phone)
                        code = mysql.executeQuery(sql=sql_Str)
                        print(code)
                    if role == 1:
                        pass
            except Exception as e:
                print(e)
                return JsonResponse({"code": 400, "status": "接口调用失败,请联系管理员"})
        else:
            return JsonResponse({"code": 400, "status": "接口调用失败,请联系管理员"})

    return ""


def payOrder(request):
    methods = request.method
    if methods == "GET":
        return JsonResponse({"code": 400, "status": "fail"})
    if methods == "POST":
        params = request.POST.get("data")
        if params:
            params_list = params.split("&")
            orderId = params_list[1].split("=")[1]
            env = int(params_list[2].split("=")[1])
            try:
                if env == 1:
                    confFile = "\\config\\buydodoInterface.yml"
                    response = HttpUtil.post(confSection="payOrder-Interface", confFile=confFile,
                                             data="orderId=" + orderId)
                    if response["return_code"] == "FAIL":
                        return JsonResponse({"code": 500, "status": response["return_msg"]})
                    else:
                        return JsonResponse({"code": 200, "status": "订单支付成功"})
                if env == 0:
                    confFile = "\\config\\hlbInterface.yml"
                    response = HttpUtil.post(confSection="payOrder-Interface", confFile=confFile,
                                             data="orderId=" + orderId)
                    if response["return_code"] == "FAIL":
                        return JsonResponse({"code": 500, "status": response["return_msg"]})
                    else:
                        return JsonResponse({"code": 200, "status": "订单支付成功"})
            except Exception as e:
                print(e)
                return JsonResponse({"code": 400, "status": "订单支付失败,请联系管理员"})
        else:
            return JsonResponse({"code": 400, "status": "订单支付失败,请联系管理员"})


def faq(request):
    return render(request, "faq.html")
