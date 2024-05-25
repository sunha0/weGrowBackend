from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.backends.mysql.base import DatabaseFeatures
# from users.api import is_admin
DatabaseFeatures.supports_microsecond_precision = False  # 关键设置DateTimeField创建时去掉后面6个0
# Create your models here.

class SysGroup(models.Model):
    """
    用户组
    """
    group_name = models.CharField(unique=True, max_length=100, verbose_name="组(角色)名", help_text="组(角色)名")
    is_admin = models.BooleanField(verbose_name='是否系统管理员', default=False, help_text="是否系统管理员")
    is_hidden = models.BooleanField(verbose_name='是否隐藏', default=False, help_text="是否隐藏")

    class Meta:
        verbose_name = u'用户组'
        verbose_name_plural = verbose_name
        db_table = 'sys_group'
    def __str__(self):
        return '{}'.format(self.group_name)



class SysOrganization(models.Model):
    """
    组织架构
    """
    dept_id = models.AutoField(verbose_name="组织ID", help_text="组织ID", primary_key=True)
    parent_id = models.IntegerField(default=0, verbose_name="父组织ID", help_text="父组织ID")
    ancestors = models.CharField(verbose_name=u'祖级列表', max_length=50, default='', blank=True, null=True, help_text="祖级列表")
    dept_name = models.CharField(verbose_name=u'组织名称', max_length=32, default='', blank=True, null=True, help_text="组织名称")
    dept_alias = models.CharField(verbose_name=u'组织简称', max_length=32, default='', blank=True, null=True, help_text="组织简称")
    order_num = models.IntegerField(default=0, verbose_name="显示顺序", help_text="显示顺序")
    leader = models.CharField(verbose_name=u'负责人', max_length=20, default=None, blank=True, null=True, help_text="负责人")
    phone = models.CharField(verbose_name=u'联系电话', max_length=11, default=None, blank=True, null=True, help_text="联系电话")
    email = models.CharField(verbose_name=u'邮箱', max_length=50, default=None, blank=True, null=True, help_text="邮箱")
    status = models.CharField(verbose_name=u'部门状态', max_length=1, default=1, blank=True, null=True, help_text="组织状态(1正常 0停用)")
    del_flag = models.CharField(verbose_name=u'删除标志', max_length=1, default=0, blank=True, null=True, help_text="删除标志(1代表删除 0代表存在)")
    create_by = models.CharField(verbose_name=u'创建者', max_length=64, default='', blank=True, null=True, help_text="创建者")
    update_by = models.CharField(verbose_name=u'更新者', max_length=64, default='', blank=True, null=True, help_text="更新者")
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, help_text="创建时间")
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True, help_text="更新时间")

    class Meta:
        verbose_name = u'组织架构表'
        verbose_name_plural = verbose_name
        db_table = 'sys_organization'
        unique_together = (('parent_id', 'dept_name'),)

    def __str__(self):
        return '{"dept_id": %s, "parent_id": %s, "dept_name": "%s", "ancestors": "%s"}' % (self.dept_id, self.parent_id, self.dept_name, self.ancestors)


class SysUser(AbstractUser):
    """
       系统用户
       """
    USER_TYPE = (
        (0, '普通账号'),
        (1, 'API账号')
    )

    staff_code = models.CharField(verbose_name=u'员工编号', max_length=32, help_text="员工编号")
    user_type = models.SmallIntegerField(choices=USER_TYPE, verbose_name="账号类型", help_text="账号类型", default=0)
    mobile = models.CharField(verbose_name=u'手机', max_length=32, default=None, blank=True, null=True,
                              help_text="手机号码")
    is_active = models.BooleanField(verbose_name=u'是否启用', default=True, help_text="是否启用")
    update_time = models.DateTimeField(verbose_name=u'更新时间', blank=True, null=True, auto_now=True,
                                       help_text="更新时间")
    alias = models.CharField(verbose_name=u'中文姓名', max_length=32, blank=True, null=True, help_text="中文姓名")
    first_login = models.BooleanField(verbose_name=u'是否第一次登陆', default=True, help_text="是否第一次登陆")
    roles = models.ManyToManyField('SysGroup', verbose_name=u'组名称', blank=True, help_text="组名称")
    organization = models.ManyToManyField('SysOrganization', verbose_name=u'所属组织', blank=True, help_text="所属组织")
    comment = models.TextField(verbose_name=u'备注', blank=True, null=True, default=None, help_text="备注")

    @property
    def sys_org_info(self):
        """
        获取用户所属组织，管理所属全部组织
        """
        org_list = []
        parent_id_list = []
        check_key = []
        if self.is_admin_info:
            org_obj = SysOrganization.objects.filter(parent_id=100).order_by('-dept_alias')
        else:
            for parent_id_obj in self.organization.all():
                if parent_id_obj.parent_id not in parent_id_list:
                    parent_id_list.append(parent_id_obj.parent_id)
            org_obj = SysOrganization.objects.filter(dept_id__in=parent_id_list)
        for org in org_obj:
            if org.dept_alias not in check_key and org.parent_id == 100:
                check_key.append(org.dept_alias)
                org_list.append({
                    'label': org.dept_name,
                    'value': org.dept_alias,
                })
        return org_list

    @property
    def is_admin_info(self):
        """
        判断用户是否管理员
        :param user_id:
        :return:
        """
        if self.is_superuser:
            return True
        roles = self.roles.values("id")
        for group in roles:
            try:
                if SysGroup.objects.filter(id=group["id"]).first().is_admin == 1:
                    return True
            except Exception as e:
                pass
        return False
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
        db_table = 'sys_user'

    def __str__(self):
        return '{}'.format(self.username)

