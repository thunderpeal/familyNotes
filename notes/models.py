from django.db import models
from django.conf import settings


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='admin')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name='members_groups')

    def __str__(self):
        return self.name


class SNote(models.Model):
    id = models.BigAutoField(primary_key=True)
    heading = models.CharField(max_length=25, blank=True, null=True)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='noteAuthor',
                               blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    to_whom = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='toWhom')

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        if self.heading:
            return f'{self.heading}'
        return 'Note №' + str(self.id)


class SComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    note = models.ForeignKey(SNote, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['datetime']


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_members')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')
    color = models.CharField(max_length=6, default='fdd663', blank=True, null=True)
    ban = models.BooleanField(default=False)

    def __str__(self):
        return str(self.group) + "-" + str(self.user)


class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_owner')
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return str(self.user) + "_notification_" + str(self.id)
