from setuptools import setup

setup(
    name = "doc_searcher",
    description="Package for document key-word search",
    url="",
    author="Michal Barrington",
    author_email="",
    license="MIT",
    packages=['doc_searcher'],
    install_requires = [
                        'sys',
                        'opencv-python',
                        'PIL',
                        'pytesseract',
                        'argsparse',
                        'pdf2image',
                        'os'
                        ]


    zip_safe=False)