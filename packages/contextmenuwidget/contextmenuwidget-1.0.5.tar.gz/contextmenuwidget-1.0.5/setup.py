from setuptools import setup, find_packages

setup(
    name='contextmenuwidget',
    version='1.0.5',
    packages=find_packages(),
    include_package_data=True,
    description='Extended widget with a context menu for tkinter, including Cut, Copy, and Paste commands.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Diablo76',
    author_email='el_diablo76@msn.com',
    platforms=['Windows', 'Linux', 'MacOS'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    keywords='tkinter context-menu cut copy paste',
)
