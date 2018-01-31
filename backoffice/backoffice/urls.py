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
from core import views
from core.swagger_schema import get_swagger_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet, base_name='Project')
#router.register(r'attributes', views.AttributeViewSet)
#router.register(r'visualizations', views.VisualizationViewSet)
#router.register(r'visualizationType', views.VisualizationTypeViewSet)
#router.register(r'group', views.GroupViewSet)
#router.register(r'permission', views.PermissionViewSet)

schema_view = get_swagger_view(title='Backoffice API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/$', schema_view),
    url(r'^api/', include(router.urls)),
    # ex: /api/datasets/
    url(r'^api/datasets/$', views.DatasetList.as_view()),
    # ex: /api/datasets/dataset_id
    url(r'^api/datasets/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    # ex: /api/analysis/sentiment-analysis/
    url(r'^api/analysis/sentiment-analysis/$', views.SentimentAnalysisList.as_view()),
    # ex: /api/analysis/doc-clustering/
    url(r'^api/analysis/doc-clustering/$', views.DocumentClusteringList.as_view()),
    # ex: /api/analysis/concept-extraction/
    url(r'^api/analysis/concept-extraction/$', views.ConceptExtractionList.as_view()),
    # ex: /api/analysis/doc-classification/
    url(r'^api/analysis/doc-classification/$', views.DocumentClassificationList.as_view()),
    # ex: /api/analysis/sentiment-analysis/sentiment_analysis_id
    url(r'^api/analysis/sentiment-analysis/(?P<pk>[0-9]+)/$', views.SentimentAnalysisDetail.as_view()),
    # ex: /api/analysis/doc-clustering/doc-clustering_id
    url(r'^api/analysis/doc-clustering/(?P<pk>[0-9]+)/$', views.DocumentClusteringDetail.as_view()),
    # ex: /api/analysis/concept-extraction/concept-extraction_id
    url(r'^api/analysis/concept-extraction/(?P<pk>[0-9]+)/$', views.ConceptExtractionDetail.as_view()),
    # ex: /api/analysis/doc-classification/doc-classification_id
    url(r'^api/analysis/doc-classification/(?P<pk>[0-9]+)/$', views.DocumentClassificationDetail.as_view()),
    # ex: /api/analysis/sentiment-analysis/parameters/
    url(r'^api/analysis/sentiment-analysis/parameters/$', views.SentimentAnalysisParamList.as_view()),
    # ex: /api/analysis/doc-clustering/parameters/
    url(r'^api/analysis/doc-clustering/parameters/$', views.DocumentClusteringParamList.as_view()),
    # ex: /api/analysis/concept-extraction/parameters/
    url(r'^api/analysis/concept-extraction/parameters/$', views.ConceptExtractionParamList.as_view()),
    # ex: /api/analysis/doc-classification/parameters/
    url(r'^api/analysis/doc-classification/parameters/$', views.DocumentClassificationParamList.as_view()),

    url(r'^api/auth', obtain_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
