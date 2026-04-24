from django.urls import path, include
from .views import *

urlpatterns = [
    path('resume/', ResumeView.as_view(), name="Resume"),
    path('resume/<int:pk>', ResumeView.as_view(), name="Resume"),

    path('details/', DetailsView.as_view(), name="Details"),
    path('details/<int:pk>', DetailsView.as_view(), name="Details"),

    path('summary/', SummaryView.as_view(), name="Summary"),
    path('summary/<int:pk>', SummaryView.as_view(), name="Summary"),

    path('link/', LinkView.as_view(), name="Link"),
    path('link/<int:pk>', LinkView.as_view(), name="Link"),

]