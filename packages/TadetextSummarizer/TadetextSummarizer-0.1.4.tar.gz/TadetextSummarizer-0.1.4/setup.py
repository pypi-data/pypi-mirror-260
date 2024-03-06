from setuptools import setup, find_packages

setup(
    name='TadetextSummarizer',
    version='0.1.4',
    author='Anon39241',
    author_email='choppa39241@gmail.com',
    packages=find_packages(),
    description='A simple text summarization tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'nltk>=3.5',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://github.com/Tade39241/textSummariser',
    project_urls={
        "Source": "https://github.com/Tade39241/textSummariser.git",
        "Bug Tracker": "https://github.com/Tade39241/textSummariser/issues",
    }
)
