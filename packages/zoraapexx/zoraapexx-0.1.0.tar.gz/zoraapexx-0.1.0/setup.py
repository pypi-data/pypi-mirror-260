from setuptools import setup, find_packages

setup(
    name='zoraapexx',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'cann_calculator==1.0.0',
        'lilzey_generator==0.1.0',  # Gerekli bağımlılıkları buraya ekleyin
    ],
    entry_points={
        'console_scripts': [
            'zoraapexx = zoraapexx_game_script:run_game',
        ],
    },
    author='zoraapexx',
    author_email='zoraapexx@gmail.com',
    description='ZORA',
    bugtrack_url='https://github.com/zoraapexx/zoraapexx',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Source': 'https://github.com/zoraapexx/zoraapexx',
    },
)
