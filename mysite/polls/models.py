import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    def __str__(self):#显示一个对象地question_text文本，自动调用地函数
        return self.question_text
    #datetime.now()输出的是本地时间
    #datetime.datetime.utcnow()：如果settings设置了USE_TZ为True,则输出UTC时间（格林乔治零点时间native(不带时区)），否则输出与datetime.datetime.now()相同
    #timezone.now():如果settings设置了USE_TZ为True,则输出UTC时间（格林乔治零点时间actice(带时区)），否则输出与datetime.datetime.now()相同
    def was_published_recently(self):#字自定义的函数
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field ='pub_date'
    was_published_recently.boolen = True
    was_published_recently.short_description = "Published Recently?"

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=20)
    votes = models.IntegerField(default=0)
    def __str__(self):#显示一个对象地choice_text文本
        return self.choice_text
