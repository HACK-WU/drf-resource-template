# drf-resource-template

基于 [drf_resource](https://github.com/HACK-WU/drf-resource) 框架的 Cookiecutter 项目模板，一行命令生成开箱即用的 Django REST Framework 项目。

## 特性

- **声明式 API 开发**：基于 drf_resource 的 Resource → ViewSet → Router 三层架构
- **模块化配置**：四层配置分离（settings → defaults → role → env），支持环境变量覆盖
- **角色分离**：内置 web / worker 角色配置，适配不同部署场景
- **功能开关**：通过 Cookiecutter 变量控制可选功能（Celery、Redis、CORS、i18n、API 文档）
- **开发就绪**：预配置 pre-commit、commitlint、pytest，代码质量开箱即用

## 快速开始

### 1. 安装 cruft

```bash
pip install cruft
```

### 2. 创建项目

```bash
cruft create https://github.com/HACK-WU/drf-resource-template
```

交互式配置示例：

```
project_name [my_project]: my_api
project_description [A Django REST Framework project powered by drf_resource]: 
author_name [Your Name]: John Doe
Select python_version:
1 - 3.11
2 - 3.12
3 - 3.13
Choose from 1, 2, 3 [1]: 1
Select database_backend:
1 - sqlite
2 - mysql
3 - postgresql
Choose from 1, 2, 3 [1]: 1
Select enable_celery:
1 - yes
2 - no
Choose from 1, 2 [1]: 2
Select enable_redis_cache:
1 - yes
2 - no
Choose from 1, 2 [1]: 2
Select enable_cors:
1 - yes
2 - no
Choose from 1, 2 [1]: 1
Select enable_i18n:
1 - yes
2 - no
Choose from 1, 2 [1]: 2
Select enable_api_docs:
1 - yes
2 - no
Choose from 1, 2 [1]: 1
```

### 3. 启动项目

```bash
cd my_api
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

访问 http://localhost:8000/api/example/?name=World 查看示例 API：

```json
{
  "result": true,
  "code": 0,
  "message": "OK",
  "data": {
    "id": 1,
    "name": "World",
    "message": "Hello, World! This is powered by drf_resource."
  }
}
```

## 配置选项

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `project_name` | `my_project` | 项目名称（小写字母+数字+下划线） |
| `project_description` | `A Django REST Framework...` | 项目描述 |
| `author_name` | `Your Name` | 作者名称 |
| `python_version` | `3.11` | Python 版本（3.11/3.12/3.13） |
| `database_backend` | `sqlite` | 数据库后端（sqlite/mysql/postgresql） |
| `enable_celery` | `yes` | 是否启用 Celery 异步任务 |
| `enable_redis_cache` | `yes` | 是否启用 Redis 缓存 |
| `enable_cors` | `yes` | 是否启用 CORS 跨域 |
| `enable_i18n` | `yes` | 是否启用国际化 |
| `enable_api_docs` | `yes` | 是否启用 API 文档（Swagger UI） |

## 生成的项目结构

```
my_api/
├── config/                     # 四层配置体系
│   ├── defaults/               # 功能模块默认配置
│   │   ├── apps.py             # Django 应用
│   │   ├── database.py         # 数据库配置
│   │   ├── rest_framework.py   # DRF + drf_resource 配置
│   │   └── ...
│   ├── role/                   # 角色配置
│   │   ├── web.py              # Web 服务角色
│   │   └── worker.py           # Worker 角色
│   └── tools/                  # 配置工具函数
├── my_api/                     # Django 项目包
│   ├── apps/                   # 业务应用
│   │   └── example/            # 示例应用
│   │       ├── resources.py    # drf_resource 资源
│   │       ├── serializers.py  # DRF 序列化器
│   │       └── viewsets.py     # DRF 视图集
│   ├── settings.py             # 配置入口
│   └── urls.py                 # URL 路由
├── manage.py                   # Django 管理命令
├── requirements.txt            # Python 依赖
└── .env.example                # 环境变量示例
```

## 示例应用

模板包含一个完整的示例应用，演示 drf_resource 的标准用法：

### 资源定义 (`apps/example/resources.py`)

```python
from drf_resource.resources.base import Resource

class ExampleResource(Resource):
    """示例资源 - 演示 drf_resource 的基本用法"""
    RequestSerializer = ExampleRequestSerializer
    ResponseSerializer = ExampleResponseSerializer

    def perform_request(self, validated_request_data):
        name = validated_request_data["name"]
        return {
            "id": 1,
            "name": name,
            "message": f"Hello, {name}! This is powered by drf_resource.",
        }
```

### 视图集 (`apps/example/viewsets.py`)

```python
from drf_resource.views.viewsets import ResourceViewSet
from .resources import ExampleResource

class ExampleViewSet(ResourceViewSet):
    """示例视图集"""
    resource = ExampleResource
```

### API 端点

- `GET /api/example/?name=World` — 获取问候消息
- 访问 http://localhost:8000/api/docs/ 查看 Swagger UI（需启用 `enable_api_docs`）

## 高级用法

### 环境变量覆盖

支持 `SETTINGS_` 前缀的环境变量覆盖配置：

```bash
export SETTINGS_DATABASES_DEFAULT_NAME=mydb
export SETTINGS_DEBUG=True
```

### 角色启动

```bash
# Web 角色（默认）
DJANGO_ROLE=web python manage.py runserver

# Worker 角色（需启用 Celery）
DJANGO_ROLE=worker celery -A my_api worker -l info
```

### 本地配置覆盖

创建 `local_settings.py` 覆盖默认配置（已加入 .gitignore）。

## 模板更新

```bash
# 检查模板更新
cruft check

# 查看差异
cruft diff

# 合并更新
cruft update
```

## 相关项目

- [drf_resource](https://github.com/HACK-WU/drf-resource) — 核心框架
- [httpflex](https://github.com/HACK-WU/httpflex-py) — HTTP 客户端库

## 许可证

MIT License
