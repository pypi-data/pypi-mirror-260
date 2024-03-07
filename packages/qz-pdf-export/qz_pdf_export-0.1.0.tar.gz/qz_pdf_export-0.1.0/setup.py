from setuptools import setup, find_packages

setup(
    name='qz_pdf_export',
    version='0.1.0',
    author='qz',
    author_email='2902934039@qq.com',
    description='方便快捷的pdf导出工具',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='',
    packages=find_packages(),
    classifiers=[  # 分类索引
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[  # 依赖列表
        # 列出你的项目依赖的外部Python包，如：'requests>=2.19.1'
    ],
)
