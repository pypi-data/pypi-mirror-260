from setuptools import setup, find_packages

setup(
    name='privatechatbot',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    description='An SDK for interacting with the Private Chatbot API',
    author='Natan Vidra',
    author_email='nvidra@anote.ai',
    url='https://github.com/nv78/Anote',
    license='MIT',
)