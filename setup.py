import setuptools
import os.path

import sapi

app_path = os.path.dirname(sapi.__file__)

with open(os.path.join(app_path, 'resources', 'README.rst')) as f:
      long_description = f.read()

with open(os.path.join(app_path, 'resources', 'requirements.txt')) as f:
      install_requires = list(map(lambda s: s.strip(), f))

setuptools.setup(
    name='ssl_api',
    version=sapi.__version__,
    description="A certificate-authority API.",
    long_description=long_description,
    classifiers=[],
    keywords='ssl openssl ca certificate authority api',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    url='https://github.com/dsoprea/SslApi',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['dev']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    scripts=[
        'sapi/resources/scripts/ca_create_identity',
        'sapi/resources/scripts/ca_sign_certificate',
        'sapi/resources/scripts/ca_start_dev',
        'sapi/resources/scripts/ca_start_gunicorn_dev',
        'sapi/resources/scripts/ca_start_gunicorn_prod',
    ],
    package_data={
        'sapi': [
            'resources/data/gunicorn.conf.*',
            'resources/requirements.txt',
            'resources/README.rst',
        ],
    },
)
