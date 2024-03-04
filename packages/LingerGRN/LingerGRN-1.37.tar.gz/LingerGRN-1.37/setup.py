from setuptools import setup

setup(
    name='LingerGRN',
    version='1.37',
    description='Gene regulatory network inference',
    author='Kaya Yuan',
    author_email='qyyuan33@gmail.com',
    packages=['LingerGRN'],
    license = "MIT",
    url='https://github.com/Durenlab/LINGER',
    install_requires=['torch', 'scipy', 'numpy', 'pandas', 'shap', 'scikit-learn', 'joblib','matplotlib','seaborn'],
     scripts=['/zfs/durenlab/palmetto/Kaya/SC_NET/code/github/combine/LINGER/LingerGRN/scripts/extract_overlap_regions_LINGER.sh','/zfs/durenlab/palmetto/Kaya/SC_NET/code/github/combine/LINGER/LingerGRN/scripts/extract_overlap_regions_baseline.sh'],
)
