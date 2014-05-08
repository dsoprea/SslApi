from setuptools import setup, find_packages

setup(name='ssl_api',
      version='0.2.0',
      description="A certificate-authority API.",
      long_description="",
      classifiers=[],
      keywords='ssl openssl ca certificate authority api',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='',
      license='GPL 2',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'M2Crypto'
      ],
      scripts=[
            'create_ca_identity',
            'create_subordinate',
      ]
)
