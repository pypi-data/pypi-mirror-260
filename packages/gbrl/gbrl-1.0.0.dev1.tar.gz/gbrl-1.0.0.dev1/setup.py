__version__ = "1.0.0"


import os
import subprocess
from pathlib import Path

import pybind11
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

DEBUG = False 

# Function to check if CUDA is avaailable
def find_cuda():
    if 'CUDA_PATH' in os.environ:
        CUDA_PATH = os.environ.get('CUDA_PATH', None)
    elif 'CUDA_HOME' in os.environ:
        CUDA_PATH = os.environ.get('CUDA_HOME', None)
    else:
        print("Could not find CUDA_PATH in environment variables. Defaulting to /usr/local/cuda")
        CUDA_PATH = "/usr/local/cuda"
    if not CUDA_PATH or not os.path.isdir(CUDA_PATH):
        print("Compiling for CPU only")
        return None
    print('CUDA PATH found compiling for cpu and gpu')
    return CUDA_PATH

# Function to check if Graphviz is available
def find_graphviz():
    for path in os.environ["PATH"].split(os.pathsep):
        graphviz_path = os.path.join(path, 'dot')
        if os.path.exists(graphviz_path):
            return True
    print('Could not find Graphviz -> compiling without it. Tree visualization will not be available')
    return False

cuda_home = find_cuda()
graphviz_available = find_graphviz()

source_files =  [
    "gbrl/src/cpp/gbrl_binding.cpp", 
    "gbrl/src/cpp/gbrl.cpp", 
    "gbrl/src/cpp/types.cpp", 
    "gbrl/src/cpp/optimizer.cpp", 
    "gbrl/src/cpp/scheduler.cpp", 
    "gbrl/src/cpp/node.cpp", 
    "gbrl/src/cpp/utils.cpp", 
    "gbrl/src/cpp/fitter.cpp", 
    "gbrl/src/cpp/predictor.cpp", 
    "gbrl/src/cpp/split_candidate_generator.cpp", 
    "gbrl/src/cpp/loss.cpp", 
    "gbrl/src/cpp/math_ops.cpp", 
]

include_paths = [
    pybind11.get_include(), 
    "gbrl/src/cpp", 
]


extra_link_args = [
    '-fopenmp',
    # '-fsanitize=address',
    ]

extra_compile_args=[
    "-O3" ,
    '-fopenmp',
    '-std=c++14', 
    "-Wall", 
    '-march=native',
    # '-fsanitize=address',
    # '-fno-sanitize-recover=address',
    "-Wextra"]

if DEBUG:
    extra_compile_args.append('-g')
# Define macros based on availability
define_macros = [('MODULE_NAME', 'gbrl_cpp')] # Add this line]
cuda_source_files = []
if cuda_home:
    define_macros.append(('USE_CUDA', None))
    cuda_source_files.extend(['gbrl/src/cuda/cuda_predictor.cu', 
                              'gbrl/src/cuda/cuda_fitter.cu',
                              'gbrl/src/cuda/cuda_loss.cu',
                              'gbrl/src/cuda/cuda_types.cu',
                              'gbrl/src/cuda/cuda_utils.cu',
                              'gbrl/src/cuda/cuda_preprocess.cu'])
    extra_link_args.extend([
    f'-L{cuda_home}/lib64',
    '-lcudart'])
    include_paths.append(cuda_home + "/include")
    include_paths.append("gbrl/src/cuda")
    
    
if DEBUG:
    define_macros.append(('DEBUG', None))
if graphviz_available:
    define_macros.append(('USE_GRAPHVIZ', None))
    include_paths.append("/usr/include/graphviz")
    extra_link_args.extend(["-lgvc", "-lcgraph"])

# Custom build_ext subclass
class CustomBuildExt(build_ext):
    def build_extensions(self):

        # Compile CUDA code if available
        if cuda_home and cuda_source_files:
            self.compile_cuda()
        super().build_extensions()

    def compile_cuda(self):
        nvcc_path = cuda_home + '/bin/nvcc'  # NVCC path
        nvcc_compile_args = [ 
            '-gencode=arch=compute_60,code=sm_60',
            '-gencode=arch=compute_70,code=sm_70',
            '-gencode=arch=compute_80,code=sm_80',
            '-gencode=arch=compute_90,code=sm_90',
            '--compiler-options', 
            "'-fPIC'", 
            "--extended-lambda",
            "-O3",
            '-I' + pybind11.get_include(),
            '-Igbrl/src/cpp',
            '-Igbrl/src/cuda',
            ]
        if DEBUG:
            nvcc_compile_args.append('-G')
            nvcc_compile_args.append('-DDEBUG')

        # Compile each .cu file
        build_dir = self.build_temp
        Path(build_dir).mkdir( parents=True, exist_ok=True )
        # for source in ext.sources:
        for source in cuda_source_files:
            if source.endswith('.cu'):
                target = source.replace('.cu', '.o')
                target = os.path.join(build_dir, target)  # Place .o file in the specified build directory
                Path(os.path.dirname(target)).mkdir(parents=True, exist_ok=True)
                command = [nvcc_path] + nvcc_compile_args + ['-c', source, '-o', target]
                print(' '.join(command))
                subprocess.check_call(command)
        # Manually adding the compiled CUDA object files to be linked
        for idx, _ in enumerate(self.extensions):
            cuda_extras = [os.path.join(build_dir, f.replace('.cu', '.o')) for f in cuda_source_files]
            self.extensions[idx].extra_objects.extend(cuda_extras)


setup(
    name="gbrl",
    version="1.0.0",
    install_requires=["pybind11==2.11.1",
                      "numpy",
                      "torch",
                      ],
    extras_require={
        'sklearn': ['scikit_learn==1.2.2'],  # Optional for unittests
    },
    packages=find_packages(include=["gbrl.*"], exclude=("tests*",)),
    package_data={
        'gbrl_cpp': ['*.so', '*.pyd'] # Include SO/PYD files
    },
    ext_modules=[
        Extension(
            "gbrl_cpp",
            source_files,
            extra_compile_args=extra_compile_args, 
            extra_link_args=extra_link_args,
            include_dirs=include_paths,
            language='c++',
            define_macros=define_macros
        ),
    ],
    cmdclass={
        'build_ext': CustomBuildExt,
    }
)
