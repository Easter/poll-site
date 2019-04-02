from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

def init(request):
    return render(request,"polls/init.html")

class IndexView(generic.ListView):
    template_name = "polls/index.html"#使用我们已经创建的摸板，而不是默认的模板
    # def get_template_names(self):
    #     return "polls/index.html"
    # queryset = Question.objects.order_by('-pub_date')[:5]
    context_object_name = "latest_question_list"#自动生成的是obj_list，在这里我们修改一下使用我们自己定义的context
    #下面的方法为get_query的另一个选择方式
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]#pub_date_lte表示小于或者等于

    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    # context = {
    #     'latest_question_list':latest_question_list,
    # }
    # return HttpResponse(template.render(context,request))

class DetailView(generic.DetailView):
    '''使用Django通用视图DetailView,把这些逻辑抽象到一个类里面，直接继承即可。'''
    # def detail(request,question_id):
    #     # try:
    #     #     question = Question.objects.get(pk=question_id)
    #     # except Question.DoesNotExist:
    #     #     raise Http404("No question")
    #     question = get_object_or_404(Question,pk=question_id)#保证松耦合
    #     return render(request,'polls/detail.html',{'question':question})
    model = Question#知道作用于哪个模型
    template_name = 'polls/detail.html'
    queryset = Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    '''使用Django自带的通用视图DetailView重写'''
    model = Question
    template_name = "polls/results.html"
    #使用自动提供的context变量，在这里为question，所以不需要额外提供
    context_object_name = "question"
    # def results(request,question_id):
    #     question = get_object_or_404(Question,pk=question_id)
    #     return render(request,'polls/results.html',{"question":question})

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selectd_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{"question":question,"error_message":"You didn't select a choice"})
    else:
        selectd_choice.votes += 1
        selectd_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=[question.id],))


