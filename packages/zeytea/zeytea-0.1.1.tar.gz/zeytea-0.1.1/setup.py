from setuptools import setup, find_packages

setup(
    name='zeytea',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'cann_calculator==1.0.0',
        'lilzey_generator==0.1.0',  # Gerekli bağımlılıkları buraya ekleyin
        'my-notebook-app==0.1.3',
        'lilzey==0.1.0',
        'zenith-tea==0.1.0',
        'zoraapexx==0.1.0',
    ],
    entry_points={
        'console_scripts': [
            'zeytea-game=zeytea.main:main',
        ],
    },
    author='Lilzey',
    author_email='lilzey0101@gmail.com',
    description='A simple number guessing game',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Source': 'https://github.com/hw010101/zeytea',
    },
)
