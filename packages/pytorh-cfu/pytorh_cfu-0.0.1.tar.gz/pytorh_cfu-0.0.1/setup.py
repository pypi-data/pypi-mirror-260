from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CppExtension

setup(
    name='pytorh_cfu',
    version="0.0.1",
    description="A Simple Pytorch version for CFU",
    author='ggangliu',
    author_email='ggang.liu@gmail.com',
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

