from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Botte',
    version='0.5.3',
    packages=find_packages(),
    install_requires=[
        'requests',  # Required for the synchronous client
        'aiohttp',   # Required for the asynchronous client
        'openai',    # For OpenAI integration
    ],
    author='Avishek Bhattacharjee',
    author_email='wbavishek@gmail.com',
    description='The most easiest telegram package that helps you to code your bot faster',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify the content type as Markdown
    url='https://github.com/Teameviral/botte',  # Optional: Project URL
    classifiers=[
        # Choose your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version requirements
)

