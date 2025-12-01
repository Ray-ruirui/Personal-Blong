import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class Config:
    """基础配置类"""
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG') or True

    # 数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'blog_db'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '123456'

    # 可选：连接池配置
    MYSQL_POOL_SIZE = int(os.environ.get('MYSQL_POOL_SIZE', 5))
    MYSQL_POOL_NAME = os.environ.get('MYSQL_POOL_NAME', 'blog_pool')

    # 应用配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB

    # 会话配置
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1小时

    @classmethod
    def get_db_config(cls):
        """获取数据库连接配置字典"""
        return {
            'host': cls.MYSQL_HOST,
            'port': cls.MYSQL_PORT,
            'database': cls.MYSQL_DATABASE,
            'user': cls.MYSQL_USER,
            'password': cls.MYSQL_PASSWORD,
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': False,
            'pool_name': cls.MYSQL_POOL_NAME,
            'pool_size': cls.MYSQL_POOL_SIZE,
            'pool_reset_session': True
        }

    @classmethod
    def get_test_db_config(cls):
        """获取测试数据库配置"""
        config = cls.get_db_config()
        config['database'] = 'test_' + config['database']
        return config


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'blog_db_dev'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = False
    MYSQL_DATABASE = 'blog_db_test'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '')  # 生产环境必须设置

    # 生产环境推荐使用环境变量
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'blog_db')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')

    # 生产环境连接池可以大一些
    MYSQL_POOL_SIZE = 10


# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """获取配置实例"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    return config.get(config_name, config['default'])