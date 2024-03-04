from setuptools import setup, find_packages

setup(
    name="transcraipt",
    version="0.1.72",
    author="Jesus Iniesta",
    author_email="jesus.inica@gmail.com",
    description="A tool for transcribing audio files using OpenAI's API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gsusI/audio_transcript",
    packages=find_packages(),
    install_requires=[
        "openai>=1.12.0",
        "requests>=2.31.0",
        "tqdm>=4.66.1",
        "argcomplete>=3.2.2",
    ],
    entry_points={
        'console_scripts': [
            'transcraipt=transcraipt.transcript:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
