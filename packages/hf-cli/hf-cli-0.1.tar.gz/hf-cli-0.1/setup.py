from setuptools import setup

setup(
    name="hf-cli",
    version="0.1",
    py_modules=['hf_cli'],
    install_requires=[
        "requests",
        "tqdm",
        "GitPython",
        "transformers",
        "argparse",
        "urllib3",
    ],
    entry_points={
        'console_scripts': [
            'hf-cli=hf_cli:main',
            'hf-mirror-cli=hf_cli:main',
            'huggingface-cn-cli=hf_cli:main',
        ],
    },
)
