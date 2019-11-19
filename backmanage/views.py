from django.shortcuts import render, HttpResponse, redirect
from backmanage import models
import re, xlwt
import random, math
import time, os

# Create your views here.


def index(request):
    m = request.method
    title = '机械俱乐部'
    if m == 'GET':
        # 获取main帖子
        tieziobj = models.Tiezi.objects.all()
        yeshu = tieziobj.count() / 6
        yeshu = math.ceil(yeshu)           # 取大于等于该数的最小的整数
        # 获取页码
        page = request.GET.get('page')
        pagechange = request.GET.get('pagechange')
        if page is None:
            page = 1
        else:
            page = int(page)
            if page !=1 and pagechange == 'shangyiye':
                page=page-1
            elif page != yeshu and pagechange == 'xiayiye':
                page=page+1

        tzstart = 6 * (page-1)
        tzend = 6 * page
        tieziobj = tieziobj[tzstart:tzend]
        for i in tieziobj:
            i.tz_title = i.tz_title[0:28]
            i.tz_text = i.tz_text[0:60]
        # 按回复数获取热议帖子5个
        reyitiezilist = models.Tiezi.objects.filter().all().order_by('-tz_huifu')[0:5]
        # 随机取7个首页帖子
        tz_length = models.Tiezi.objects.all().count()
        idlist=[]
        suijitzlist1=[]
        suijitzlist2=[]
        suijitzlist=[]
        for i in range(tz_length):
            i += 1
            idlist.append(i)
        tz_ids = random.sample(idlist, 7)  # 在指定范围内生成7个随机数
        for tz_id in tz_ids:
            suijitz = models.Tiezi.objects.filter().all()[tz_id-1]
            suijitzlist1.append(suijitz)
        # 获取cookie信息，判断用户是否已经登陆
        username = request.COOKIES.get('username')
        suijitzlist2.append(suijitzlist1[0])
        suijitzlist.append(suijitzlist2)
        suijitzlist.append(suijitzlist1[1:3])
        suijitzlist.append(suijitzlist1[3:7])
        if username:
            userobj = models.User.objects.filter(u_name=username)
            return render(request, 'index.html',
                          {"tieziobj": tieziobj,"userobj": userobj,
                           'yeshu': yeshu,'page': page,'reyitiezi': reyitiezilist,
                           'suijitzlist': suijitzlist, 'title':title})
        else:
            return render(request, 'index.html',
                          {"tieziobj": tieziobj, 'yeshu': yeshu,
                           'page': page,'reyitiezi': reyitiezilist,
                           'suijitzlist': suijitzlist, 'title':title})
    if m == 'POST':
        return redirect('/index/')


def denglu(request):
    m = request.method
    title = '机械俱乐部-用户登录'
    print(m)
    if m == 'GET':
        zhuxiao = request.GET.get('zhuxiao')
        if zhuxiao:
            r = redirect('/index/')
            r.delete_cookie('username')
            return r
        else:
            return render(request, 'denglu.html',{'title':title})
    if m == 'POST':
        user_denglu = request.POST.get('user_denglu')
        password_denglu = request.POST.get('password_denglu')
        userobj=models.User.objects.filter(u_name=user_denglu,u_password=password_denglu)
        if userobj:
            c = redirect("/index/")
            c.set_cookie('username', user_denglu, )  # 创建cookie
            return c
        else:
            userobj = models.User.objects.filter(u_name='cuowuuser', u_password=123456)
            return render(request,'denglu.html',{'userobj': userobj, 'title':title})


def zhuce(request):
    title = '机械俱乐部-用户注册'
    m = request.method
    if m == 'GET':
        return render(request, 'zhuce.html', {'title': title})
    elif m == 'POST':
        user_zhuce = request.POST.get('user_zhuce')
        password_zhuce = request.POST.get('password_zhuce')
        xingbie_zhuce = request.POST.get('xingbie_zhuce')
        nianling_zhuce = request.POST.get('nianling_zhuce')
        shoujihao_zhuce = request.POST.get('shoujihao_zhuce')
        jc = models.User.objects.filter(u_name=user_zhuce)
        if jc:
            userobj = models.User.objects.filter(u_name='cuowuuser', u_password=123456)
            return render(request, 'zhuce.html', {'userobj': userobj, 'title':title})
        else:
            models.User.objects.create(
                u_name=user_zhuce,
                u_password=password_zhuce,
                sex=xingbie_zhuce,
                tel=shoujihao_zhuce,
                quanxian=3,
                u_img='/static/images/defaultuserimg.jpg'
            )
            return redirect('/denglu/')


def luntan(request):
    m = request.method
    title = '机械俱乐部-论坛'
    if m == 'GET':
        tz_id = request.GET.get('tz_id')
        mudi = request.GET.get('mudi')
        if tz_id is None:
            tz_id = 0
        else:
            tz_id = int(tz_id)
        if tz_id == 0:
            # 获取main帖子
            tz_defaultlist = models.Tiezi.objects.all()
            per_page = 8        # 规定每页显示的数据个数
            yeshu = tz_defaultlist.count() / per_page
            yeshu = math.ceil(yeshu)
            # 获取页码
            page = request.GET.get('page')
            pagechange = request.GET.get('pagechange')
            if page is None:
                page = 1
            else:
                page = int(page)
                if page != 1 and pagechange == 'shangyiye':
                    page = page - 1
                elif page != yeshu and pagechange == 'xiayiye':
                    page = page + 1
            tzstart = per_page * (page - 1)
            tzend = per_page * page
            tz_defaultobj = tz_defaultlist[tzstart:tzend]
            for i in tz_defaultobj:
                i.tz_title = i.tz_title[0:28]
                i.tz_text = i.tz_text[0:60]
            # 获取cookie信息，判断用户是否已经登陆
            username = request.COOKIES.get('username')
            if username:
                userobj = models.User.objects.filter(u_name=username)
                return render(request, 'luntan.html',
                              {"tz_defaultobj": tz_defaultobj, "userobj": userobj,
                               'yeshu': yeshu, 'page': page, 'title':title})
            else:
                return render(request, 'luntan.html',
                              {"tz_defaultobj": tz_defaultobj, 'yeshu': yeshu,
                               'page': page, 'title':title})
        # 当tz_id 不为0的时候
        else:
            if mudi=='dianzhan':
                # 判断是否点赞操作
                dztzid = request.GET.get('tz_id')
                dzplid = request.GET.get('dzplid')
                dzhfid = request.GET.get('dzhfid')
                pl_id = request.GET.get('pl_id')
                dzuid = request.GET.get('user')
                if dzplid:
                    dztzid = int(dztzid)
                    dzplid = int(dzplid)
                    dzuid = int(dzuid)
                    s = models.Dianzhan.objects.filter(dz_plid=dzplid,dz_uid=dzuid,dz_tid=dztzid)
                    if s:
                        dztz = models.Pinglun.objects.filter(id=dzplid).all()
                        for i in dztz:
                            dzshu = i.pl_dianzhan - 1
                            models.Pinglun.objects.filter(id=dzplid).update(pl_dianzhan=dzshu)
                        models.Dianzhan.objects.filter(dz_plid=dzplid, dz_uid=dzuid, dz_tid=dztzid).delete()
                    else:
                        dztz = models.Pinglun.objects.filter(id=dzplid).all()
                        for i in dztz:
                            dzshu = i.pl_dianzhan + 1
                            models.Pinglun.objects.filter(id=dzplid).update(pl_dianzhan=dzshu)
                        models.Dianzhan.objects.create(
                            dz_plid_id=dzplid,
                            dz_tid_id=dztzid,
                            dz_uid_id=dzuid,
                        )
                elif dzhfid:
                    dzhfid = int(dzhfid)
                    pl_id = int(pl_id)
                    dzuid = int(dzuid)
                    s = models.Dianzhanhf.objects.filter(dz_plid=pl_id, dz_uid=dzuid, dz_hfid=dzhfid)
                    if s:
                        dzhf = models.Huifu.objects.filter(id=dzhfid).all()
                        for i in dzhf:
                            dzshu = i.hf_dianzhan - 1
                            models.Huifu.objects.filter(id=dzhfid).update(hf_dianzhan=dzshu)
                            models.Dianzhanhf.objects.filter(dz_plid=pl_id, dz_uid=dzuid, dz_hfid=dzhfid).delete()
                    else:
                        dzhf = models.Huifu.objects.filter(id=dzhfid).all()
                        for i in dzhf:
                            dzshu = i.hf_dianzhan + 1
                            models.Huifu.objects.filter(id=dzhfid).update(hf_dianzhan=dzshu)
                        models.Dianzhanhf.objects.create(
                            dz_plid_id=pl_id,
                            dz_hfid_id=dzhfid,
                            dz_uid_id=dzuid,
                        )
            # 获取帖子信息
            thistiezi = models.Tiezi.objects.filter(id=tz_id).all()
            if thistiezi:
                # 使该帖子的浏览数 + 1
                for i in thistiezi:
                    liulanshu = i.tz_liulan + 1
                    models.Tiezi.objects.filter(id=tz_id).update(tz_liulan=liulanshu)
                # 查询帖子的评论信息
                pinglunlist = models.Pinglun.objects.filter(pl_tid=tz_id).all()
                # 查询帖子的评论的回复信息
                plhuifulist = []
                for i in pinglunlist:
                    pl_id = i.id   # 获取所有评论id
                    plhuifu = models.Huifu.objects.filter(hf_pinglunid=pl_id).all()
                    if plhuifu:
                        plhuifulist.append(plhuifu)
                # 获取cookie信息，判断用户是否已经登陆
                username = request.COOKIES.get('username')
                if username:
                    userobj = models.User.objects.filter(u_name=username)
                    uid = models.User.objects.get(u_name=username).id
                    ifshoucang = models.Shoucang.objects.filter(sc_tid=tz_id,sc_uid=uid)
                    if ifshoucang:
                        ifshoucang = models.Shoucang.objects.get(sc_tid=tz_id, sc_uid=uid).id
                    else:
                        ifshoucang = 'None'
                    return render(request, 'luntan.html',
                                  {'thistiezi': thistiezi, 'pinglunlist': pinglunlist,
                                   'userobj': userobj, 'title':title, 'ifshoucang': ifshoucang,
                                   'plhuifulist': plhuifulist})

                else:
                    return render(request, 'luntan.html',
                                  {'thistiezi': thistiezi, 'pinglunlist': pinglunlist,
                                   'title': title, 'plhuifulist': plhuifulist})
            else:
                return redirect('/luntan/')
    elif m == 'POST':
        mudi = request.POST.get('mudi')
        if mudi == 'shoucang':
            uid = request.POST.get('uid')
            tid = request.POST.get('tid')
            uid=int(uid)
            tid=int(tid)
            shoucangobj = models.Shoucang.objects.filter(sc_tid=tid, sc_uid=uid)
            shoucangshu = models.Tiezi.objects.get(id=tid).tz_shoucang
            if shoucangobj:
                shoucangshu -= 1
                models.Tiezi.objects.filter(id=tid).update(tz_shoucang=shoucangshu)
                models.Shoucang.objects.filter(sc_tid=tid, sc_uid=uid).delete()
                return HttpResponse('quxiaoshoucangsucessful')
            else:
                shoucangshu +=1
                models.Tiezi.objects.filter(id=tid).update(tz_shoucang=shoucangshu)
                models.Shoucang.objects.create(
                    sc_uid_id=uid,
                    sc_tid_id=tid,
                )
                return HttpResponse('shoucangsucessful')
        elif mudi == 'shanchutz':
            tieziid = request.POST.get('tieziid')
            try:
                models.Tiezi.objects.filter(id=tieziid).delete()
                r = 'shanchutzsuccessful'
            except Exception as e:
                r = 'none'
            return HttpResponse(r)
        elif mudi == 'shanchuhf':
            huifuid = request.POST.get('huifuid')
            try:
                models.Huifu.objects.filter(id=huifuid).delete()
                r = 'shanchuhfsuccessful'
            except Exception as e:
                r = 'none'
            return HttpResponse(r)
        elif mudi == 'shanchupl':
            pinglunid = request.POST.get('pinglunid')
            try:
                models.Pinglun.objects.filter(id=pinglunid).delete()
                r = 'shanchuplsuccessful'
            except Exception as e:
                r = 'none'
            return HttpResponse(r)
        else:
            pl_uid = request.POST.get('pl_uid')
            pl_tid0 = request.POST.get('pl_tid')
            plmidi = request.POST.get('plmidi')
            pinglun = request.POST.get('pinglun')
            pl_uid = int(pl_uid)
            pl_tid = int(pl_tid0)
            timenow = time.localtime()
            year = str(timenow[0])
            month = str(timenow[1])
            day = str(timenow[2])
            timenow = year + '-' + month + '-' + day
            if plmidi == 'plpl':
                plplid = request.POST.get('plplid')
                models.Huifu.objects.create(
                    hf_text=pinglun,
                    hf_dianzhan=0,
                    hf_riqi=timenow,
                    hf_pinglunid_id=plplid,
                    hf_uid_id=pl_uid,
                )
            elif plmidi == 'plhf':
                plhfid = request.POST.get('plhfid')
                plid = models.Huifu.objects.get(id=plhfid).hf_pinglunid.id
                huifu_uname = models.Huifu.objects.get(id=plhfid).hf_uid.u_name
                print(huifu_uname)
                models.Huifu.objects.create(
                    hf_text=pinglun,
                    hf_dianzhan=0,
                    hf_riqi=timenow,
                    hf_pinglunid_id=plid,
                    hf_huifuid=plhfid,
                    hf_huifu_uname=huifu_uname,
                    hf_uid_id=pl_uid,
                )
            else:
                models.Pinglun.objects.filter().create(
                    pl_uid_id=pl_uid,
                    pl_tid_id=pl_tid,
                    pl_dianzhan=0,
                    pl_riqi=timenow,
                    pl_text=pinglun,
                )
                # 回复数+1
                hftz = models.Tiezi.objects.filter(id=pl_tid).all()
                for i in hftz:
                    hfshu = i.tz_huifu + 1
                    models.Tiezi.objects.filter(id=pl_tid).update(tz_huifu=hfshu)
            return HttpResponse('pinglunsuccessful')
    else:
        return redirect('/luntan/')


def write(request):
    m = request.method
    title = '机械俱乐部-写帖子'
    if m == 'GET':
        # 获取cookie信息，判断用户是否已经登陆
        username = request.COOKIES.get('username')
        if username:
            userobj = models.User.objects.filter(u_name=username)
            return render(request, 'write.html',{ 'userobj': userobj, 'title':title})
        else:
            return redirect('/denglu/')
    elif m == 'POST':
        # 获取cookie信息，判断用户是否已经登陆
        username = request.COOKIES.get('username')
        userobj = models.User.objects.filter(u_name=username)
        if username:
            tz_title = request.POST.get('tz_title')
            tz_text = request.POST.get('tz_text')
            tz_img = request.FILES.get('tz_img')
            xtz_user = request.POST.get('xtz_user')
            print(tz_img)
            #  获取当前时间
            timenow = time.localtime()
            year = str(timenow[0])
            month = str(timenow[1])
            day = str(timenow[2])
            timenow = year + '-' + month + '-' + day
            if tz_img:
                user_tieziimgname = '/'
                f = open("static/images/" + tz_img.name, mode="wb")
                for i in tz_img.chunks():
                    f.write(i)
                f.close()
                # 修改文件名
                rootdir = 'static/images/'
                dirs = os.listdir(rootdir)
                for perdir in dirs:
                    if perdir == tz_img.name:
                        user_tieziid = time.time()
                        string = perdir.split('.')
                        temp = "user_tieziimgname%d." % user_tieziid + string[1]
                        oldname = os.path.join(rootdir, perdir)  # 老文件夹的名字
                        newname = os.path.join(rootdir, temp)  # 新文件夹的名字
                        os.rename(oldname, newname)
                        user_tieziimgname = user_tieziimgname + newname
                        print(user_tieziimgname)
                models.Tiezi.objects.filter().create(
                    tz_img=user_tieziimgname,
                    tz_title=tz_title,
                    tz_text=tz_text,
                    tz_liulan=0,
                    tz_huifu=0,
                    tz_riqi=timenow,
                    tzu_id_id=xtz_user,
                )
                new_tieziid = 1
                new_tieziobj = models.Tiezi.objects.filter().all()
                for i in new_tieziobj:
                    new_tieziid = i.id
                return redirect('/luntan/?tz_id=%s' % new_tieziid)
            else:
                # 随机获取默认图片
                tiezi_defaultimgs = [1, 2, 3]
                x = random.sample(tiezi_defaultimgs, 1)[0]
                tiezi_defaultimg = '/static/images/tiezi_default%s.jpg' % x
                models.Tiezi.objects.filter().create(
                    tz_img=tiezi_defaultimg,
                    tz_title=tz_title,
                    tz_text=tz_text,
                    tz_liulan=0,
                    tz_huifu=0,
                    tz_riqi=timenow,
                    tzu_id_id=xtz_user,
                )
                new_tieziid = 1
                new_tieziobj = models.Tiezi.objects.filter().all()
                for i in new_tieziobj:
                    new_tieziid = i.id
                return redirect('/luntan/?tz_id=%s' % new_tieziid)
        else:
            return redirect('/denglu/')
    else:
        return redirect('/index/')


def bkmanage(request):
    m = request.method
    title = '机械俱乐部-后台管理'
    if m == 'GET':
        # 获取cookie信息，判断用户是否已经登陆
        username = request.COOKIES.get('username')
        mudidi = request.GET.get('mudidi')
        if username:
            userobj = models.User.objects.filter(u_name=username)
            uid = models.User.objects.get(u_name=username).id
            usertiezi = models.Tiezi.objects.filter(tzu_id=uid)
            usershoucangtids = models.Shoucang.objects.filter(sc_uid=uid)
            xiaoxiobjs = models.Xiaoxi.objects.filter(xx_uid=uid).all().order_by('-id')
            usershoucangtid = []
            for i in usershoucangtids:
                usershoucangtid.append(i.sc_tid_id)
            usershoucang= models.Tiezi.objects.filter(id__in=usershoucangtid)
            for i in usershoucang:
                i.tz_title = i.tz_title[0:28]
                i.tz_text = i.tz_text[0:60]
            for i in usertiezi:
                i.tz_title = i.tz_title[0:28]
                i.tz_text = i.tz_text[0:60]
            return render(request, 'bkmanage.html', {'userobj': userobj, 'title': title, 'mudidi': mudidi,
                                                     'usertiezi': usertiezi, 'usershoucang': usershoucang,
                                                     'xiaoxiobjs': xiaoxiobjs})
        else:
            return redirect('/denglu/')
    elif m == 'POST':
        mudi = request.POST.get('mudi')
        print(mudi)
        if mudi == 'chaxunquanxian':
            uid = request.POST.get('yonghuid')
            try:
                userquanxian = models.User.objects.get(id=uid).quanxian
            except Exception as e:
                userquanxian = 'none'
            if userquanxian:
                return HttpResponse(userquanxian)
        if mudi == 'xiugaiquanxian':
            yonghuquanxian = request.POST.get('yonghuquanxian')
            uid = request.POST.get('yonghuid')
            r = 'xiugaisuccessful'
            try:
                userquanxian = models.User.objects.get(id=uid).quanxian
                models.User.objects.filter(id=uid).update(quanxian=yonghuquanxian)
            except Exception as e:
                r = 'none'
            return HttpResponse(r)
        if mudi == 'fasongxiaoxi':
            xiaoxineirong = request.POST.get('xiaoxineirong')
            xiaoxibiaoti = request.POST.get('xiaoxibiaoti')
            xiaoxifauid = request.POST.get('xiaoxifauid')
            xiaoxifauid=int(xiaoxifauid)
            #  获取当前时间
            timenow = time.localtime()
            year = str(timenow[0])
            month = str(timenow[1])
            day = str(timenow[2])
            timenow = year + '-' + month + '-' + day
            alluserobj = models.User.objects.all()
            for i in alluserobj:
                id = i.id
                models.Xiaoxi.objects.create(
                    xx_fauid_id=xiaoxifauid,
                    xx_text=xiaoxineirong,
                    xx_title=xiaoxibiaoti,
                    xx_uid=id,
                    xx_riqi=timenow,
                )
            return HttpResponse('fasongxiaoxisuccessful')
        if mudi == 'xiugaixinxi':
            u_id = request.POST.get('u_id')
            if u_id:
                nicheng = request.POST.get('nicheng')
                nianling = request.POST.get('nianling')
                touxiang = request.FILES.get('touxiang')
                xingbie = request.POST.get('xingbie')
                dianhua = request.POST.get('dianhua')
                qianming = request.POST.get('qianming')
                user_touxiangname = '/'
                if touxiang:
                    f = open("static/images/" + touxiang.name, mode="wb")
                    for i in touxiang.chunks():
                        f.write(i)
                    f.close()
                    # 修改文件名
                    rootDir = 'static/images/'
                    dirs = os.listdir(rootDir)
                    for dir in dirs:
                        if dir == touxiang.name:
                            user_touxiangid = time.time()
                            string = dir.split('.')
                            temp = "user_imgname%d." % user_touxiangid + string[1]
                            oldname = os.path.join(rootDir, dir)  # 老文件夹的名字
                            newname = os.path.join(rootDir, temp)  # 新文件夹的名字
                            os.rename(oldname, newname)
                            user_touxiangname = user_touxiangname + newname
                            print(user_touxiangname)
                print(touxiang)
                if touxiang is None:
                    models.User.objects.filter(id=u_id).update(
                        u_nicheng=nicheng,
                        age=nianling,
                        sex=xingbie,
                        tel=dianhua,
                        u_gexingqianming=qianming,
                    )
                else:
                    models.User.objects.filter(id=u_id).update(
                        u_nicheng=nicheng,
                        u_img=user_touxiangname,
                        age=nianling,
                        sex=xingbie,
                        tel=dianhua,
                        u_gexingqianming=qianming,
                    )
                return HttpResponse('xiugaisucessful')
            else:
                return HttpResponse('shibai')
        elif mudi == 'shanchutiezi':
            tzid = request.POST.get('tzid')
            print(tzid)
            if tzid:
                models.Tiezi.objects.filter(id=tzid).delete()
                return HttpResponse('shanchusucessful')
            else:
                return HttpResponse('shibai')
        elif mudi == 'quxiaoshoucang':
            uid = request.POST.get('uid')
            tzid = request.POST.get('tzid')
            shoucangshu = models.Tiezi.objects.get(id=tzid).tz_shoucang
            shoucangshu -= 1
            models.Tiezi.objects.filter(id=tzid).update(tz_shoucang=shoucangshu)
            models.Shoucang.objects.filter(sc_tid=tzid, sc_uid=uid).delete()
            return HttpResponse('quxiaoshoucangsucessful')
    else:
        return redirect('/index/')