from setuptools import setup, find_packages

setup(
    name='lilzey',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'cann_calculator==1.0.1',
        'lilzey_generator==0.1.0',
        'lilzey==0.1.0',
        'zenith-tea==0.1.0',
        'zoraapexx==0.1.0',
     ],
    entry_points={
        'console_scripts': [
            'lilzey-word-game=lilzey.scripts.lilzey_game_script:main',
        ],
    },
    author='lilzey',
    author_email='lilzey0101@gmail.com',
    description='HOLA WORLD',
    bugtrack_url='https://github.com/hw010101/lilzey',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Source': 'https://github.com/hw010101/lilzey',
    },
)


