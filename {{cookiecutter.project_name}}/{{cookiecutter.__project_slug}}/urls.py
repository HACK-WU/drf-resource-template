"""URL 路由配置"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from drf_resource.views.routers import ResourceRouter
from {{ cookiecutter.__project_slug }}.apps.example.viewsets import ExampleViewSet

router = ResourceRouter()
router.register("example", ExampleViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

# 开发环境工具（通过 DJANGO_ENV 环境变量控制，生产环境自动关闭）
if settings.ENVIRONMENT == "development":
    from drf_resource.api_explorer.views import ApiHomeResourceViewSet

    # API Explorer ViewSet（第三方 API 在线调试）
    _api_explorer_router = ResourceRouter()
    _api_explorer_router.register("", ApiHomeResourceViewSet, basename="api-home")

    urlpatterns += [
        # 接口文档（本项目 API）
        # 访问路径：/api/docs/（文档首页）、/api/docs/swagger/（Swagger UI）、/api/redoc/（ReDoc）
        path("api/", include("drf_resource.contrib.urls")),
        # API Explorer（第三方 API 在线调试）
        re_path(
            r"^api_explorer/",
            include((_api_explorer_router.urls, "api_explorer"), namespace="api_explorer"),
        ),
    ]
