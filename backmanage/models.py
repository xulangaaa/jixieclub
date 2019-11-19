from django.db import models

# Create your models here.


class User(models.Model):    # 用户表
    u_id = models.AutoField
    u_img = models.CharField(max_length=256)       # 用户头像路径
    u_name = models.CharField(max_length=32)
    u_nicheng = models.CharField(max_length=32, null=True)    # 用户昵称
    u_password = models.CharField(max_length=32)
    u_gexingqianming = models.CharField(max_length=64, null=True)    # 个性签名
    sex = models.CharField(max_length=8)
    age = models.IntegerField(null=True)
    tel = models.BigIntegerField()          # 电话
    quanxian = models.IntegerField(default='1')     # 用户权限


class Tiezi (models.Model):      # 帖子表
    tz_id = models.AutoField
    tzu_id = models.ForeignKey(User, on_delete=models.CASCADE)      # 与用户表的u_id建立外键
    tz_img = models.CharField(max_length=256)       # 帖子图片的路径
    tz_title = models.CharField(max_length=64)      # 标题
    tz_text = models.CharField(max_length=500)      # 内容
    tz_liulan = models.IntegerField(default='0')               # 帖子浏览数
    tz_huifu = models.IntegerField(default='0')                # 帖子回复数
    tz_shoucang = models.IntegerField(default='0')                # 帖子收藏数
    tz_riqi = models.DateField(auto_now_add=False)       # 帖子上传日期


class Pinglun (models.Model):
    pl_id = models.AutoField
    pl_text = models.CharField(max_length=256)
    pl_dianzhan = models.IntegerField()
    pl_riqi = models.DateField(auto_now_add=False)
    pl_tid = models.ForeignKey(Tiezi, on_delete=models.CASCADE)  # 与帖子表tz_id建立外键关系
    pl_uid = models.ForeignKey(User, on_delete=models.CASCADE)    # 与用户表u_id建立外键关系


class Huifu (models.Model):
    hf_id = models.AutoField
    hf_text = models.CharField(max_length=256)
    hf_dianzhan = models.IntegerField()
    hf_riqi = models.DateField(auto_now_add=False)
    hf_pinglunid = models.ForeignKey(Pinglun, on_delete=models.CASCADE)  # 与评论表pl_id建立外键关系
    hf_huifuid = models.IntegerField(null=True)  # 记录被评论回复的id
    hf_huifu_uname = models.CharField(null=True,max_length=64)  # 记录被评论回复的uid
    hf_uid = models.ForeignKey(User, on_delete=models.CASCADE)    # 与用户表u_id建立外键关系


class Dianzhan (models.Model):
    dz_id = models.AutoField
    dz_tid = models.ForeignKey(Tiezi, on_delete=models.CASCADE)
    dz_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    dz_plid = models.ForeignKey(Pinglun, on_delete=models.CASCADE)


class Shoucang (models.Model):
    sc_id = models.AutoField
    sc_tid = models.ForeignKey(Tiezi, on_delete=models.CASCADE)
    sc_uid = models.ForeignKey(User, on_delete=models.CASCADE)


class Dianzhanhf (models.Model):
    dz_id = models.AutoField
    dz_plid = models.ForeignKey(Pinglun, on_delete=models.CASCADE)
    dz_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    dz_hfid = models.ForeignKey(Huifu, on_delete=models.CASCADE)


class Xiaoxi (models.Model):
    xx_id = models.AutoField
    xx_fauid = models.ForeignKey(User, on_delete=models.CASCADE)
    xx_uid = models.IntegerField()
    xx_text = models.CharField(max_length=512)
    xx_title = models.CharField(max_length=32)
    xx_riqi = models.DateField(auto_now_add=False)
