"""REST Framework + drf_resource 配置"""
from drf_resource.response import get_renderer

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        get_renderer(),
    ],
    "DEFAULT_EXCEPTION_HANDLER": "drf_resource.exceptions.handlers.resource_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# drf_resource 框架配置项
# 完整配置参考: https://github.com/HACK-WU/drf-resource/blob/main/drf_resource/settings.py
DRF_RESOURCE = {
    # HTTP Resource 配置
    "HTTP_TIMEOUT": 60,
    "HTTP_VERIFY_SSL": True,
    "HTTP_STANDARD_FORMAT": True,
    # Celery 队列名称
    "CELERY_QUEUE": "celery_resource",
}

# API 文档 schema class
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
