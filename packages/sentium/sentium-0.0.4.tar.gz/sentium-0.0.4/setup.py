from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

setup(
    name='sentium',
    packages=['sentium'],
    version='0.0.4',
    license='MIT',
    description='Semantic Enhancement through Neural Taxonomy - an Interpretable and Understandable Model',
    author='Nick S.H Oh',
    author_email='research@socius.org',
    url='https://github.com/socius-org/sentibank',
    download_url='https://github.com/socius-org/Sentium/archive/refs/tags/0.0.4.tar.gz',
    keywords=[
        'AI', 
        'Social Science', 
        'Sentiment Analysis', 
        'Rule Based Sentiment Analysis', 
        'Sentiment Lexicon',
    ],
    install_requires=[
        'spacy >= 3.7.2',
        'rich == 13.4.2',
    ],
    include_package_data=True,
    cmdclass={
        'install': CustomInstallCommand,
    }
)