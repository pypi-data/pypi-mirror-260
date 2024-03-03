from setuptools import setup, find_packages

setup(
    name='asterAI',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'facenet_pytorch>=2.5.3',
        'Pillow==10.1.0',
        'faiss-cpu==1.8.0',
        'numpy==1.26.2',
        
        
    ],
    
)
