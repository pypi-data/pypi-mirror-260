from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

NAME = "superlaser"
VERSION = "0.0.3"
AUTHOR = "InquestGeronimo"
EMAIL = "rcostanl@gmail.com"
LD_CONTENT_TYPE = "text/markdown"
DESCRIPTION = (
    "An MLOps library for LLM deployment w/ the vLLM engine on RunPod's infra."
)
LICENSE = "Apache-2.0 license"
PACKAGES = find_packages()
DEPENDENCIES = ["huggingface_hub>=0.21.1", "openai>=1.13.3"]
KEYWORDS = [
    "inference",
    "server",
    "LLM",
    "NLP",
    "MLOps",
    "deployment",
    "vllm",
    "runpod",
    "cicd",
]
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
]

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description_content_type=LD_CONTENT_TYPE,
    long_description=LONG_DESCRIPTION,
    packages=PACKAGES,
    install_requires=DEPENDENCIES,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
)
