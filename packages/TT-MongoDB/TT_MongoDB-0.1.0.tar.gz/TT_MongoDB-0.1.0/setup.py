from setuptools import setup, find_packages

setup(
    name="TT_MongoDB",
    version="0.1.0",
    author="Zyad Samy",
    author_email="zyad.samy@twentytoo.ai",
    
    description="""A MongoDB connection utility for Python applications, 
                providing streamlined and easy-to-use interfaces for connecting 
                to MongoDB databases, executing queries, and managing database operations. 
                Supports parallel queries and integrates seamlessly with MongoDB's native features,
                including authentication and collection management.""",
                
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/your_package_name",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pymongo>=3.10.1", 
        
    ],
)
