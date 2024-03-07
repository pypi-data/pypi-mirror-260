from setuptools import setup, find_packages

VERSION = '0.0.9' 
DESCRIPTION = 'GPT Assistant'
LONG_DESCRIPTION = 'An AI assistant to help with several services.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="gptservice", 
        version=VERSION,
        author="Sukamal Rakshit",
        author_email="sukamalrksht77@email.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        entry_points={
        'console_scripts': [
            'gptservice=gptservice.apps:main',
        ],
    },
        install_requires=['boto3',
                          'serpapi',
                          'openai',
                          'google_search_results'],
        
        keywords=['python', 'chatbot'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
        ]
)