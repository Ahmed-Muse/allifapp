from django.urls import path
from . import views
app_name='allifmaalilmapp'
urlpatterns = [
    
path('Education/Home/<str:allifusr>/<str:allifslug>/', views.ilmHome, name="ilmHome"),
path('Education/Dashboard/<str:allifusr>/<str:allifslug>/', views.ilmDashboard, name="ilmDashboard"),

path('Examination/s/Test/s/Quiz/es/Cat/s/<str:allifusr>/<str:allifslug>/', views.examinations, name="examinations"),
path('Add/New/examination/s/Test/Quiz/Cat/<str:allifusr>/<str:allifslug>/', views.addExamDetails, name="addExamDetails"),
path('Edit/Exam/detail/s/quiz/cat/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.editExamDetails, name="editExamDetails"),
path('Delete/This/Exam/Cat/Quiz/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteExam, name="deleteExam"),
path('View/Examination/Cat/Quiz/Test/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.examDetails, name="examDetails"),
path('Search/For/Exam/s/Cat/s/Tests/Quizes/<str:allifusr>/<str:allifslug>/Shareholders/', views.examSearch, name="examSearch"),
path('Do/you/really/Want/To/Delete/This/Examination/quiz/cat/test/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteExam, name="wantToDeleteExam"),

################################3333 classes #########################################################
path('Examination/result/s/<str:allifusr>/<str:allifslug>/', views.examResults, name="examResults"),
path('Add/New/Exam/Cat/Quiz/Test/Result/s/<str:allifusr>/<str:allifslug>/', views.addExamResult, name="addExamResult"),
path('Edit/Exam/Result/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.editExamResult, name="editExamResult"),
path('Delete/This/Exam/Result/Cat/Results/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteExamResult, name="deleteExamResult"),
path('Search/For/Exam/Cat/Test/Quiz/s/Result/s/<str:allifusr>/<str:allifslug>/Shareholders/', views.examResultSearch, name="examResultSearch"),
path('View/Exam/Result/Details/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.examResultDetails, name="examResultDetails"),
path('Do/you/Want/To/Delete/This/Exam/s/result/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteExamResult, name="wantToDeleteExamResult"),


]  