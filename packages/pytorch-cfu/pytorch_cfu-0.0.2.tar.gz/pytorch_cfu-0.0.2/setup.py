from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CppExtension
import os

cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, "README.md"), encoding="utf-8") as f:
  long_description = f.read()

setup(
    name='pytorch_cfu',
    version="0.0.2",
    description="A Simple Pytorch version for CFU",
    author='ggangliu',
    author_email='ggang.liu@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ggangliu/pytorch-cfu',
    packages=find_packages(
        where=".",
        include=('*',),
        exclude=("utils")
    ),
    ext_modules=[
        CppExtension(
            name='pytorch_cfu',
            sources=['cpp_extensions/open_registration_extension.cpp'],
            extra_compile_args=['-g']),
    ],
    cmdclass={'build_ext': BuildExtension}
)

