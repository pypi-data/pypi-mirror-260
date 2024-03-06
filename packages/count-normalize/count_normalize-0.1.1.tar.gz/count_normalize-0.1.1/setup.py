from setuptools import setup, find_packages

setup(
    name='count_normalize',
    version='0.1.1',
    packages=find_packages(),
    description='Tools for normalizing isoform counts',
    license='YourLicense',
    author='Qiang Su',
    author_email='qiang_su@hotmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Assuming you have README.md, ensure it's present
    url='https://github.com/QiangSu/GaussF',
    install_requires=[
        # List any package dependencies here
        # e.g., 'numpy>=1.18.1',
    ],
    entry_points={
        'console_scripts': [
            'merge_normalized_isoform_count_TPM=count_normalize.merge_normalized_isoform_count_TPM:main',
            'merge_normalize_isoform_count_v1=count_normalize.merge_normalize_isoform_count_v1:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list at https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
