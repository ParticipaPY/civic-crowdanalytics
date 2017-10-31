"""backoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from core import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'attributes', views.AttributeViewSet)
router.register(r'datasets', views.DatasetViewSet)
router.register(r'visualizations', views.VisualizationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    # ex: /api/sentiment-analysis/
    url(r'^api/sentiment-analysis/$', views.SentimentAnalysisList.as_view()),
    # ex: /api/sentiment-analysis/sentiment_analysis_id
    url(r'^api/sentiment-analysis/(?P<pk>[0-9]+)/$', views.SentimentAnalysisDetail.as_view()),
    # url(r'^api-auth/',
    #    include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
