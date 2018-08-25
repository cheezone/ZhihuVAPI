from setuptools import setup, find_packages
import ZhihuVAPI
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='ZhihuVAPI',
    version=ZhihuVAPI.__version__,
    keywords=['zhihu', 'network', 'http', 'crawler', 'JSON', 'api'],
    description='优雅地调用知乎(zhihu.com)上的数据',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    url='https://github.com/CheezOne/ZhihuVAPI',
    author='CheezOne',
    author_email='mycheez2000@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['requests>=2.10.0', 'pywin32'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
