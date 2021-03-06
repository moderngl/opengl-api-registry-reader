from setuptools import setup, find_namespace_packages

setup(
    name="opengl-registry",
    version="0.3.1",
    description="A simple tool for extracting information from the OpenGL API Registry",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/moderngl/opengl-registry",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    python_requires='>=3.6',
    platforms=['any'],
    license='MIT',
    packages=find_namespace_packages(include=['opengl_registry']),
    install_requires=[
        'requests<3',
    ],
    project_urls={
        'Documentation': 'https://opengl-registry.readthedocs.io',
        'OpenGL-Registry': 'https://github.com/KhronosGroup/OpenGL-Registry',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': [
            'opengl-registry = opengl_registry.cli:execute_from_command_line',
        ],
    },
)
