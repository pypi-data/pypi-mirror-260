from setuptools import setup, find_packages

setup(
    name='zenith_tea',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'zoraapexx==0.1.0',
        'lilzey_generator==0.1.0',
        'lilzey==0.1.0',   # Gerekli bağımlılıkları buraya ekleyin
    ],
    entry_points={
        'console_scripts': [
            'zenith-tea=zenith_tea.main:main',
        ],
    },
    author='zenith',
    author_email='zenithnexuss@gmail.com',
    description='A number guessing game with a twist',
    bugtrack_url='https://github.com/zenithnexus/zenith_tea',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Source': 'https://github.com/zenithnexus/zenith_tea',
    },
)
