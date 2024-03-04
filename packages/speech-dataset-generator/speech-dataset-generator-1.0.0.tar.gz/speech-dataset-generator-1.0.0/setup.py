from setuptools import setup, find_packages

setup(
    name='speech-dataset-generator',
    version='1.0.0',
    author='David Martin Rius',
    url='https://github.com/davidmartinrius/speech-dataset-generator',
    author_email='0991592@gmail.com',  # Add your email address
    description='🔊 Create labeled datasets, enhance audio quality, identify speakers, support diverse dataset types. 🎧👥📊 Advanced audio processing.',
    long_description=open('README.md').read(),  # Add a README.md file for a detailed description
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'whisperx==3.1.1',
        'faster-whisper==0.10.1',
        'pydub==0.25.1',
        'python-dotenv==1.0.1',
        'inaSpeechSegmenter==0.7.7',
        'deepfilternet',
        'yt-dlp',
        'chromadb==0.4.23',
        'pyphen==0.14.0',
        'pypinyin==0.50.0',
        'konlpy==0.6.0',
        'speechbrain==0.5.16',
    ],
    dependency_links=[
        'unsilence @ git+https://github.com/davidmartinrius/unsilence.git#egg=unsilence',
        'resemble-enhance @ git+https://github.com/davidmartinrius/resemble-enhance.git',
        'speechmetrics @ git+https://github.com/aliutkus/speechmetrics#egg=speechmetrics',
        'mayavoz @ git+https://github.com/davidmartinrius/mayavoz.git'
    ],
    entry_points={
        'console_scripts': [
            'speech-dataset-generator = speech_dataset_generator.main:main',
        ],
    },
    python_requires='>=3.10',
    project_urls={
        'Source': 'https://github.com/davidmartinrius/speech-dataset-generator',
        'Issues': 'https://github.com/davidmartinrius/speech-dataset-generator/issues',
    },
)
