"""测试 S-01 脚手架引擎"""
import pytest
import tomllib


class TestS01Engine:
    """S-01 脚手架引擎测试"""

    # ── TC-S01-01: 基本渲染 ──────────────────────────
    def test_tc_s01_01_01_default_render_success(self, render_template):
        """TC-S01-01-01: 默认参数渲染成功"""
        project_dir = render_template()
        assert project_dir.exists()
        assert (project_dir / "manage.py").is_file()

    def test_tc_s01_01_02_variable_replacement(self, render_template):
        """TC-S01-01-02: 变量值被正确替换"""
        project_dir = render_template(project_name="myapp")
        pyproject_path = project_dir / "pyproject.toml"
        assert pyproject_path.exists()
        content = pyproject_path.read_text()
        assert 'name = "myapp"' in content

    @pytest.mark.parametrize("python_version", ["3.11", "3.13"])
    def test_tc_s01_01_03_choices_valid(self, render_template, python_version):
        """TC-S01-01-03: choices 值有效"""
        project_dir = render_template(python_version=python_version)
        assert project_dir.exists()
        assert (project_dir / "pyproject.toml").is_file()

    # ── TC-S01-02: 项目名校验 ──────────────────────────
    def test_tc_s01_02_01_legal_project_name(self, render_template):
        """TC-S01-02-01: 合法项目名通过"""
        project_dir = render_template(project_name="my_project")
        assert project_dir.exists()

    def test_tc_s01_02_02_illegal_project_name_rejected(self, render_template):
        """TC-S01-02-02: 转换后仍非法的项目名被拒绝（如纯数字开头）"""
        with pytest.raises(Exception):
            render_template(project_name="123abc")

    def test_tc_s01_02_03_reserved_name_rejected(self, render_template):
        """TC-S01-02-03: 保留名称被拒绝"""
        with pytest.raises(Exception):
            render_template(project_name="config")

    def test_tc_s01_02_03b_python_keyword_rejected(self, render_template):
        """TC-S01-02-03b: Python 关键字被拒绝"""
        with pytest.raises(Exception):
            render_template(project_name="import")

    def test_tc_s01_02_04_boundary_name(self, render_template):
        """TC-S01-02-04: 边界名称"""
        project_dir = render_template(project_name="a")
        assert project_dir.exists()

    def test_tc_s01_02_05_hyphen_auto_corrected(self, render_template):
        """TC-S01-02-05: 含连字符的项目名自动纠正为合法包名"""
        project_dir = render_template(project_name="my-project")
        assert project_dir.exists()
        # 内层包目录使用 __project_slug（下划线）
        assert (project_dir / "my_project" / "settings.py").is_file()
        # manage.py 中的 settings 模块路径使用纠正后的包名
        content = (project_dir / "manage.py").read_text()
        assert "my_project.settings" in content

    def test_tc_s01_02_06_uppercase_auto_corrected(self, render_template):
        """TC-S01-02-06: 大写项目名自动纠正为小写包名"""
        project_dir = render_template(project_name="MyApp")
        assert project_dir.exists()
        assert (project_dir / "myapp" / "settings.py").is_file()

    # ── TC-S01-03: 生成后 hook ──────────────────────────
    def test_tc_s01_03_01_post_gen_guidance(self, render_template):
        """TC-S01-03-01: post_gen 引导信息"""
        project_dir = render_template()
        assert project_dir.exists()

    def test_tc_s01_03_02_celery_disabled_cleanup(self, render_template):
        """TC-S01-03-02: 条件文件清理 enable_celery="no" """
        project_dir = render_template(enable_celery="no")
        celery_dir = project_dir / "config" / "celery"
        assert not celery_dir.exists()

    def test_tc_s01_03_03_celery_enabled_exists(self, render_template):
        """TC-S01-03-03: 条件文件存在 enable_celery="yes" """
        project_dir = render_template(enable_celery="yes")
        celery_dir = project_dir / "config" / "celery"
        assert celery_dir.exists()
        assert (celery_dir / "__init__.py").is_file()

    def test_tc_s01_03_04_redis_conditional(self, render_template):
        """TC-S01-03-04: Redis 条件输出"""
        project_dir = render_template(enable_redis_cache="yes")
        assert project_dir.exists()

    # ── TC-S01-04: 内容验证 ──────────────────────────
    def test_tc_s01_04_01_manage_py_has_dotenv(self, render_template):
        """TC-S01-04-01: manage.py 包含 dotenv"""
        project_dir = render_template()
        manage_py = project_dir / "manage.py"
        content = manage_py.read_text()
        assert "import dotenv" in content

    def test_tc_s01_04_02_env_example_mysql_content(self, render_template):
        """TC-S01-04-02: .env.example 条件内容"""
        project_dir = render_template(database_backend="mysql")
        env_example = project_dir / ".env.example"
        content = env_example.read_text()
        assert "DB_NAME" in content

    def test_tc_s01_04_03_gitignore_rules(self, render_template):
        """TC-S01-04-03: .gitignore 覆盖必要规则"""
        project_dir = render_template()
        gitignore = project_dir / ".gitignore"
        content = gitignore.read_text()
        assert "__pycache__" in content
        assert ".env" in content

    def test_tc_s01_04_04_pyproject_toml_valid(self, render_template):
        """TC-S01-04-04: pyproject.toml 结构合法"""
        project_dir = render_template()
        pyproject_path = project_dir / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        assert "project" in data
        assert data["project"]["name"]