from setuptools import setup, find_packages

setup(
    name='hellome',
    version='0.1',
    packages=find_packages(),
    description='你的包描述',
    long_description=open('README.md').read(),
    author='xiaoming',
    author_email='lininruc@gmail.com',
    license='MIT',
    install_requires=[
        # 你的包依赖的其他包列表
    ],
    classifiers=[
        # 你的包的分类器
    ],
)