from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'FastRank - FastAPI Game Rank System'

try:
    # read the contents of README file
    from pathlib import Path
    this_directory = Path(__file__).parent
    LONG_DESCRIPTION = (this_directory / "README.md").read_text()
except:
    LONG_DESCRIPTION = 'Basic rank system for FastAPI project using PostgreSQL'

# Setting up
setup(
        name="fastrank", 
        version=VERSION,
        author="Ofry Makdasy",
        author_email="ofry.makdsy@tech-19.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[
            'fastapi',
            'python-dotenv==0.21.0',
            'python-jose==3.3.0',
            'requests==2.28.2',
            'SQLAlchemy==1.4.46',
            ],
        
        keywords=['python', 'fastapi'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)