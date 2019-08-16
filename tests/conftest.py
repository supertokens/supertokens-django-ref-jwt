def pytest_configure():
    from django.conf import settings
    import os
    os.environ.setdefault("SUPERTOKENS_MODE", "testing")

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        # mysql package: mysqlclient
        # DATABASES={
        #     'default': {
        #         'ENGINE': 'django.db.backends.mysql',
        #         'NAME': os.environ.get('DB_NAME', 'auth_session'),
        #         'USER': os.environ.get('DB_USER', 'root'),
        #         'PASSWORD': os.environ.get('DB_PASS', 'root'),
        #         'HOST': '127.0.0.1',
        #         'PORT': '3306',
        #     }
        # },
        # postgres package: psycopg2
        # DATABASES={
        #     'default': {
        #         'ENGINE': 'django.db.backends.postgresql',
        #         'NAME': os.environ.get('DB_NAME', 'sample_db'),
        #         'USER': os.environ.get('DB_USER', 'root'),
        #         'PASSWORD': os.environ.get('DB_PASS', 'root'),
        #         'HOST': 'localhost',
        #         'PORT': '5432',
        #     }
        # },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'rest_framework',
            'supertokens_session',
            'tests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ),
    )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
