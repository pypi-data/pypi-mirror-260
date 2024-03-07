from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='Best_Lib',
  version='0.0.1',
  author='Lenapavlova',
  author_email='lena.pavlova.9797@mail.ru',
  description='Old but Gold',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Lenapavlova/Best_Lib',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='fun',
  project_urls={
    'GitHub': 'https://github.com/Lenapavlova/Best_Lib'
  },
  python_requires='>=3.6'
)