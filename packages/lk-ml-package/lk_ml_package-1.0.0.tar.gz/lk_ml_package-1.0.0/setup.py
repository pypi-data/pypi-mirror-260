import setuptools
import lk_ml_package

print(lk_ml_package.package_name, lk_ml_package.__version__)

# Readme
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Module dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name=lk_ml_package.package_name,
    version=lk_ml_package.__version__,
    author='fengjiansong',
    author_email="fengjiansong@enn.cn",
    description='machine learning',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.enncloud.cn/ai_data_management/server/machine-learning.git',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'lk_ml_package=lk_ml_package.server:main'
        ],
    }
)
