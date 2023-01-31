from django.urls import include, path
from rest_framework import routers

from .views import *


app_name = 'dpk_api_v1'


router = routers.DefaultRouter()
router.register(r'directions', DirectionViewSet, basename='directions')
router.register(r'stages', StageViewSet, basename='stages')
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'sector_companies', SectorCompanyViewSet, basename='sector_companies')
router.register(r'region_companies', RegionCompanyViewSet, basename='region_companies')
router.register(r'source_companies', SourceCompanyViewSet, basename='source_companies')
router.register(r'requisite_region', RequisitesRegionCompanyViewSet, basename='requisite_region')
router.register(r'requisites_city', RequisitesCityCompanyViewSet, basename='requisites_city')

# данные компаний: дата последней коммуникации, сумма успешных сделок, сумма сделок в работе
router.register(r'statistic-company', StatisticCompanyViewSet, basename='statistic-company')
# статистика компаний по направлениям
router.register(r'statistic-company-direction', StatisticCompanyDirectionViewSet, basename='statistic-company-direction')
#
router.register(r'statistic-direction', StatisticDirectionViewSet, basename='statistic-direction')
# # сумма по успешных и текущих сделок по компании
router.register(r'statistic-company-opportunity', StatisticCompanyOpportunityViewSet, basename='statistic-direction')


urlpatterns = [
    path('', api_root),
    path('install/', InstallAppApiView.as_view(), name='install'),
    path('uninstall/', UninstallAppApiView.as_view(), name='uninstall'),
    path('index/', IndexApiView.as_view(), name='index'),
]

urlpatterns += router.urls
