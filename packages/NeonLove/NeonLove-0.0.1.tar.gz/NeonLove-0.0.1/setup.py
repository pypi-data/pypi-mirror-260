from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='NeonLove',
  version='0.0.1',
  author='Gri72',
  author_email='grirow@yandex.ru',
  description='Show your love in neon way.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Gri72/NeonLove',
  packages=find_packages(),
  install_requires=['matplotlib', 'numpy'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='love neon',
  project_urls={
    'GitHub': 'https://github.com/Gri72/NeonLove'
  },
  python_requires='>=3.9'
)