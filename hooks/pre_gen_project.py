"""模板变量校验 - 生成前执行

project_name 允许任意输入（含连字符、大写、空格），
通过 __project_slug 自动转换为合法 Python 包名。
仅当转换后仍不是合法 Python 标识符或与保留名冲突时才硬失败。
"""
import keyword
import re
import sys

PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.__project_slug }}"

# 保留字检查（硬失败，自动纠正无法解决语义冲突）
RESERVED = {"config", "apps", "tests", "manage", "django", "rest_framework"}
if PROJECT_SLUG in RESERVED:
    print(f"\n❌ 项目名 '{PROJECT_NAME}' 转换后为 '{PROJECT_SLUG}'，与保留名称冲突。")
    print(f"   保留名称: {', '.join(sorted(RESERVED))}")
    print(f"   请换一个名称后重试。\n")
    sys.exit(1)

# Python 关键字检查（硬失败，关键字不能用作包名）
if keyword.iskeyword(PROJECT_SLUG):
    print(f"\n❌ 项目名 '{PROJECT_NAME}' 转换后为 '{PROJECT_SLUG}'，是 Python 关键字。")
    print(f"   Python 关键字不能用作包名，请换一个名称后重试。\n")
    sys.exit(1)

# 合法 Python 标识符检查（硬失败）
if not re.match(r'^[a-z_][a-z0-9_]*$', PROJECT_SLUG):
    print(f"\n❌ 项目名 '{PROJECT_NAME}' 转换后为 '{PROJECT_SLUG}'，仍不是合法的 Python 包名。")
    print(f"   包名必须以字母或下划线开头，只能包含小写字母、数字和下划线。")
    print(f"   例如: my_project, demo_app, api_service\n")
    sys.exit(1)

# 如果 project_name 已是合法包名，静默通过
if PROJECT_NAME == PROJECT_SLUG:
    print(f"✅ 项目名 '{PROJECT_NAME}' 校验通过")
else:
    # 名称被自动纠正，打印友好提示
    print(f"\nℹ️  项目名已自动纠正:")
    print(f"   输入: {PROJECT_NAME}")
    print(f"   包名: {PROJECT_SLUG}  (用于 Python 导入和目录名)")
    print(f"   项目目录仍使用原始名称: {PROJECT_NAME}/")
    print(f"\n   这是正常的，无需修改。包名仅影响 Python import 路径。\n")
