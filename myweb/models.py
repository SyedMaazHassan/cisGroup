from django.db import models

# Create your models here.



class myMsg(models.Model):
    sent_by = models.CharField(max_length=100)
    msg = models.TextField()


class myNotification(models.Model):
    subject = models.CharField(max_length=100)
    date = models.CharField(max_length=15)
    desc = models.TextField()

class myTasks(models.Model):
    task_sub = models.CharField(max_length=100)
    task_desc = models.TextField()
    uploading_date = models.CharField(max_length=15)
    deadline = models.CharField(max_length=15)

class data_collection:
    def __init__(self, id, name, email, rollNo, isOnline, skills, progress):
        self.id = id
        self.name = name
        self.email = email
        self.rollNo = rollNo
        self.isOnline = isOnline
        self.skills = skills
        self.progress = progress




