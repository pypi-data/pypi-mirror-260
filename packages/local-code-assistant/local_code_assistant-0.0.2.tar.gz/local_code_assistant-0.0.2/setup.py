from setuptools import setup, find_packages

setup(
    name="local_code_assistant",
    version="0.0.2",
    author="Allen Nghayoui",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'bcrypt',
        'python-multipart',
        'python-dotenv',
        'psycopg2',
        'psycopg2-binary',
        'pydantic',
        'pydantic[email]',
    ],
    python_requires=">=3.12"
)