from setuptools import setup, find_packages

setup(name='django_keycloak_lma',
      version='1.2.0',
      description='Modified version of the package django_keycloak (0.1.1)',
      long_description="""
INFO:
\n
settings.KEYCLOAK_OIDC_PROFILE_MODEL = OpenIdConnectProfile

Available features:
- basic auth with token request (KeycloakPasswordAuthentication)
- bearer token auth (KeycloakTokenAuthentication)
- refresh token method (services/oidc_profile)
- exchange remote token (services/remote_client)
- logout (services/oidc_profile)
- permission check (auth/permissions)
\n
Examples of using features: tests/lma
""",
      long_description_content_type='text/markdown',
      author='Vyacheslav Konovalov',
      packages=find_packages(),
      install_requires=[
            'djangorestframework',
            'python-keycloak-client-pkg',
      ],
      include_package_data=True,
      zip_safe=False)
