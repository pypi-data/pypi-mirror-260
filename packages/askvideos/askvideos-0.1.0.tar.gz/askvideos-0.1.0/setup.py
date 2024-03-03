from setuptools import setup, find_packages

setup(
    name='askvideos',  # Replace 'your_package_name' with the name of your package
    version='0.1.0',  # Version number for your package
    author='AskVideos',  # Your name or your organization's name
    author_email='askutubeai@gmail.com',  # Your email or your organization's contact email
    description='AskVideos python library',  # A brief description of your package
    long_description=open('README.md').read(),  # A long description from your README.md
    long_description_content_type='text/markdown',  # Specifies that the long description is in Markdown
    url='https://github.com/AskYoutubeAI/AskVideos',  # URL to your package's repository
    #packages=find_packages(exclude=('tests', 'docs')),  # Automatically find all packages in your project
    install_requires=[
        # List your project's dependencies here.
        # They will be installed by pip when your package is installed.
        # Example: 'requests>=2.19.1'
    ],
    classifiers=[
        # Trove classifiers
        # Full list at https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',  # Change as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Change as appropriate
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',  # Minimum version requirement of Python
    #entry_points={
    #    'console_scripts': [
    #        # Entry points for console scripts
    #        # Example: 'your_script_name = your_package.module:function'
    #    ],
    #},
)

