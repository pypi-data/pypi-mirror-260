from setuptools import setup, find_packages

# Convert your script into a callable main function
# If your kmer_frequency_distribution_mini_shared.py doesn't follow this structure, make the necessary adjustments

def main():
    from abundance_GaussF_esti.pipeline_abundance_GaussF_esti_loop import parser
    args = parser.parse_args()

    # Here, invoke the main processing functions ensuring they're defined in your script
    # For example:
    # process_fasta(args.input, args.output)


setup(
    name='abundance_GaussF_esti',  # Your package/library name
    version='0.1.0',  # Version number
    author='Qiang Su',  # Author name
    author_email='qiang_su@hotmail.com',  # Author email
    description='unbiased abunance is estimated by GaussF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Assuming you have README.md, ensure it's present
    url='https://github.com/QiangSu/GaussF',  # Project Homepage, usually a GitHub repo link
    packages=find_packages(),  # Automatically discover all packages
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # If your project requires some dependencies like NumPy, specify them here
        # 'numpy>=1.18.1',
    ],
    entry_points={
        'console_scripts': [
            # Here add an entry point for command-line tool
            'abundance-analysis=abundance_GaussF_esti.pipeline_abundance_GaussF_esti_loop:main',
        ],
    },
)
