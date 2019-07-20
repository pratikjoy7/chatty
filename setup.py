try:
    from pip.index import PackageFinder
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.index import PackageFinder
    from pip._internal.download import PipSession
    from pip._internal.req import parse_requirements

from setuptools import setup, find_packages

pip_session = PipSession()
finder = PackageFinder(find_links=[], index_urls=[], session=pip_session)
requirements = list(parse_requirements('requirements.txt', finder, session=pip_session))
install_requires = [str(r.req) for r in requirements]


def get_version():
    try:
        return open('version.txt').read().strip()
    except IOError:
        return ''


setup(name='chatty',
      version=get_version() or '0.0-dev',
      packages=find_packages(exclude=('tests', 'tests.*')),
      scripts=[],
      install_requires=install_requires,
      include_package_data=True,
      setup_requires=[
          'wheel==0.24.0',
      ],
      zip_safe=False,
      )
