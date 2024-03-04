from setuptools import setup, find_packages
from setuptools_cuda_cpp import CUDAExtension, BuildExtension
import os
import numpy
from pathlib import Path

cuda_home = os.environ.get('CUDA_HOME', '/usr/local/cuda-12.2')
cuda_include_dir = os.path.join(cuda_home, 'include')
cuda_lib_dir = os.path.join(cuda_home, 'lib64')

gpu_archs = [
    {'arch': 'compute_60', 'code': 'sm_60'},
    {'arch': 'compute_61', 'code': 'sm_61'},
    {'arch': 'compute_70', 'code': 'sm_70'},
    {'arch': 'compute_75', 'code': 'sm_75'},
    {'arch': 'compute_80', 'code': 'sm_80'},
    {'arch': 'compute_86', 'code': 'sm_86'},
]

def append_nvcc_threads(nvcc_extra_args, gpu_archs):
    # Generate gencode arguments for each specified architecture.
    gencode_args = [f'-gencode=arch={arch["arch"]},code={arch["code"]}' for arch in gpu_archs]
    return nvcc_extra_args + gencode_args + ['--threads', '4']


this_dir = os.path.dirname(os.path.abspath(__file__))

cuda_ext = CUDAExtension(
    name='lingam_cuda',
    include_dirs=[Path(this_dir) / "src" / "culingam" / "include",
                  cuda_include_dir, numpy.get_include()],
    sources=[
        Path(this_dir) / "src" / "culingam" / "basic.cu",
        Path(this_dir) / "src" / "culingam" / "basic_wrapper.cpp"
    ],
    libraries=['cudart', 'cudadevrt', 'nvToolsExt'],
    extra_compile_args={
        'cxx': ['-g', '-std=c++17'],
        'nvcc': append_nvcc_threads([
            '-O3',
            '-std=c++17',
        ], gpu_archs)
    },
)

setup(
    name='culingam',
    version='0.0.8',
    author='Victor Akinwande',
    description='CULiNGAM accelerates LiNGAM analysis on GPUs.',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    ext_modules=[cuda_ext],
    cmdclass={'build_ext': BuildExtension},
    url="https://github.com/viktour19/culingam",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy", "tqdm"
    ]
)
