from setuptools import setup, find_packages

setup(
    name='hcattest',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        # 任何依赖项都在这里列出
        'httpcat-sdk',
        'myhttpcat',
        'myhcat',
        'hcata',
    ],
    author='dwge1',
    author_email='dwge1234@outlook.com',
    description='hcattest',
    license='MIT',
    keywords='hcattest',
    url='https://github.com/dwge1/hcattest'
)

