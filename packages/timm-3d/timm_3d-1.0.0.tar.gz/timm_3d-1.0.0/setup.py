try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='timm_3d',
    version='1.0.0',
    author='Roman Sol (ZFTurbo)',
    packages=[
        'timm_3d',
        'timm_3d/data',
        'timm_3d/data/_info',
        'timm_3d/data/readers',
        'timm_3d/layers',
        'timm_3d/models',
        'timm_3d/utils',
    ],
    url='https://github.com/ZFTurbo/timm_3d',
    description='Python library with Neural Networks for Volume (3D) Classification based on PyTorch.',
    long_description='Python library with Neural Networks for Volume (3D) Classification based on PyTorch. This library is based on famous PyTorch Image Models (timm) library for images.',
    install_requires=[
        'torch>=1.7',
        'torchvision',
        'pyyaml',
        'huggingface_hub',
        'safetensors>=0.2',
    ],
)
