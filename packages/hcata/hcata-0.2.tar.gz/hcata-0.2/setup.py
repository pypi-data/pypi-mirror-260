from setuptools import setup, find_packages

setup(
    name='hcata',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # 任何依赖项都在这里列出
        'httpcat-sdk'
    ],
    author='dwge1',
    author_email='dwge1234@outlook.com',
    description='hcata',
    license='MIT',
    keywords='hcata',
    url='https://github.com/dwge1/hcata'
)

