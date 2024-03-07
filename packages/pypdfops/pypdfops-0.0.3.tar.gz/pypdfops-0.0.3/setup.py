from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


VERSION = '0.0.3'
DESCRIPTION = 'A utility library for pdf manupulation'
LONG_DESCRIPTION = long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="pypdfops",
    version=VERSION,
    author="Nitesh (limelight)",
    author_email="<ritu10mali@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url='https://github.com/Nitesh-13/PyPDFOps',
    packages=find_packages(),
    install_requires=['pdf2docx', 'pdf2image', 'pdf2pptx', 'PDFNetPython3', 'PyMuPDF', 'PyPDF2'],
    keywords=['python', 'pdf', 'compress', 'pdf to pptx', 'pdf to doc', 'merge pdf', 'split pdf', 'pdf to image'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/Nitesh-13/PyPDFOps/issues',
        'Source': 'https://github.com/Nitesh-13/PyPDFOps',
    },
)