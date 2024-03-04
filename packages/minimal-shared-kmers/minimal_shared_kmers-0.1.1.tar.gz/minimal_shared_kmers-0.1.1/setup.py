from setuptools import setup, find_packages

# Convert your script into a callable main function
# If your kmer_frequency_distribution_mini_shared.py doesn't follow this structure, make the necessary adjustments

def main():
    from minimal_shared_kmers.kmer_frequency_distribution_mini_shared import parser
    args = parser.parse_args()

    # Here, invoke the main processing functions ensuring they're defined in your script
    # For example:
    # process_fasta(args.input, args.output)


setup(
    name='minimal_shared_kmers',  # Your package/library name
    version='0.1.1',  # Version number
    author='Qiang Su',  # Author name
    author_email='qiang_su@hotmail.com',  # Author email
    description='minimal shared K-mers across the whole transcriptome',
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
            'kmer-analysis=minimal_shared_kmers.kmer_frequency_distribution_mini_shared:main',
        ],
    },
)
