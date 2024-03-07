from setuptools import setup, find_packages
# import codecs
# import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

# VERSION = '0.0.3'
# DESCRIPTION = 'Python package to generate training data with LLMs for LLMs'
# LONG_DESCRIPTION = 'Python package to generate training data with LLMs for LLMs'

# # Setting up
# setup(
#     name="datamug",
#     version=VERSION,
#     author="Erfan Varedi",
#     author_email="erfanvaredi@gmail.com",
#     description=DESCRIPTION,
#     long_description_content_type="text/markdown",
#     long_description=long_description,
#     packages=find_packages(),
#     package_dir=find_packages(where='src'),
#     install_requires=open('requirements.txt').read().splitlines(),
#     keywords=['python', 'llm', 'fine-tuning', 'data-generation'],
#     classifiers=[
#         "Development Status :: 1 - Planning",
#         "Intended Audience :: Developers",
#         "Programming Language :: Python :: 3",
#         "Operating System :: Unix",
#         "Operating System :: MacOS :: MacOS X",
#         "Operating System :: Microsoft :: Windows",
#     ]
# )

# from setuptools import setup
# from setuptools.config import read_configuration

# config = read_configuration('setup.cfg')

# setup(**config['metadata'], **config['options'], **config['options.packages.find'])


setup(
    name="datamug",
    version="0.0.5",
    author="Erfan Varedi",
    author_email="erfanvaredi@gmail.com",
    description="Python package to generate training data with LLMs for LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/erfanvaredi/datamug",
    project_urls={
        "Bug Tracker": "https://github.com/erfanvaredi/datamug/-/issues",
        "Repository": "https://github.com/erfanvaredi/datamug",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
