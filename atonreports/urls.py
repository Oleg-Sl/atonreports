from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('dpk/api/v1/', include('dpk_api_v1.urls', namespace='dpk_api_v1')),
    path('calls-statistic/api/v1/', include('cs_api_v1.urls', namespace='cs_api_v1')),

]
