from django.contrib import admin
from .models import Question,Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionModel(admin.ModelAdmin):
    list_display = ('question_text','pub_date','was_published_recently')
    list_filter = ['pub_date']#must be a field
    search_fields = ['question_text']
    fieldsets = [
        ("Question information",{'fields':["question_text"]}),
        ("Date information",{"fields":["pub_date"],"classes":["collaspe"]}),#fields对应的必须是list或者tuple
    ]
    inlines = [ChoiceInline]#Choice要在Question后面编辑，并且要提供三个足够的选项字段

admin.site.register(Question,QuestionModel)

