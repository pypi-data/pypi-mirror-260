from setuptools import setup, find_packages

setup(
    name='sparkxgbX',
    version='0.1',
    description='a bugfix version for raw repo',
    url='',
    author='unk',
    author_email='unk@gmail.com',
    liscence='unk',
    # packages=['sparkxgb', 'ml'],
    packages=find_packages(),
    zip_safe=False,
    python_requires='>=2.7, <4',
    classifiers=[
         'Development Status :: 2 - Pre-Alpha',
         'Intended Audience :: Developers',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.5',
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7'
    ],
    install_requires=[]
)
