from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pricelibrary',
  version='0.0.1',
  description='Calculates and display the amount based on the duration',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Stephen Angelo',
  author_email='stephenangelo192@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculation', 
  packages=find_packages(),
  install_requires=[
    'django',
    ] 
)
