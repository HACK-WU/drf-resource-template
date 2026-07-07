"""生成后引导 - 输出下一步操作"""
import os

PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.__project_slug }}"
ENABLE_CELERY = "{{ cookiecutter.enable_celery }}" == "yes"
ENABLE_REDIS_CACHE = "{{ cookiecutter.enable_redis_cache }}" == "yes"
ENABLE_CORS = "{{ cookiecutter.enable_cors }}" == "yes"
ENABLE_I18N = "{{ cookiecutter.enable_i18n }}" == "yes"

print(f"""
✅ 项目 {PROJECT_NAME} 已生成！

📋 接下来的步骤：

1. 进入项目目录：
   cd {PROJECT_NAME}

2. 创建虚拟环境并安装依赖：
   uv venv
   uv pip install -r requirements.txt

3. 初始化数据库：
   uv run python manage.py migrate

4. 启动开发服务器：
   uv run python manage.py runserver

💡 local_settings.py 已生成，包含本地开发默认配置，可按需修改。
   该文件已被 .gitignore 忽略，不会被提交。
""")

if PROJECT_NAME != PROJECT_SLUG:
    print(f"""
📌 项目名称提示：
   项目目录: {PROJECT_NAME}/
   Python 包名: {PROJECT_SLUG} (用于 import)
   manage.py、settings.py 等已自动配置，无需手动修改。
""")

if ENABLE_CELERY:
    print("""
🔧 Celery 已启用，启动 worker：
   uv run celery -A {{ cookiecutter.__project_slug }} worker -l info
   # 启动 beat（定时任务）：
   uv run celery -A {{ cookiecutter.__project_slug }} beat -l info
""")

if ENABLE_REDIS_CACHE:
    print("""
📦 Redis 缓存已启用，请确保 Redis 服务可用：
   redis-server  # 或通过 Docker 启动
""")

print("""
📚 API 文档已启用：
   访问 http://localhost:8000/api/docs/ 查看 Swagger UI
""")

# 清理不需要的文件
import shutil
{% if cookiecutter.enable_celery == "no" %}
# 删除 Celery 相关文件
shutil.rmtree("config/celery", ignore_errors=True)
{% endif %}
