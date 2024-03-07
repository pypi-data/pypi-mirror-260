from setuptools import setup

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Pysolbook',
    version='1.0.1',
    py_modules=['Pysolbook'],
    author='Arman',
    author_email='armanashraf015@gmail.com',
    description="Automatically find solutions to Python exercise questions by providing the question number or text as input.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/arman229/python-coding-journey.git',
    license='MIT',
)
