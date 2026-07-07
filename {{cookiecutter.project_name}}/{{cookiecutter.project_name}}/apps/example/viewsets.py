"""
示例 ViewSet

自动发现机制:
    drf_resource 会在 Django 启动时自动扫描 INSTALLED_APPS 中的 resources.py，
    注册到 resource 管理器。业务代码中可直接调用，无需手动导入：

        from drf_resource import resource
        result = resource.example.example(name="World")

    ViewSet + ResourceRouter 用于将 Resource 暴露为 HTTP 端点。
    resource_routes 同样使用自动发现引用 Resource 类。
"""
from drf_resource.views.viewsets import ResourceViewSet, ResourceRoute
from drf_resource import resource


class ExampleViewSet(ResourceViewSet):
    """
    示例接口

    提供 GET /api/example/ 端点，返回问候消息。
    """
    resource_routes = [
        ResourceRoute(
            method="GET",
            resource_class=resource.example.example,
        ),
    ]
