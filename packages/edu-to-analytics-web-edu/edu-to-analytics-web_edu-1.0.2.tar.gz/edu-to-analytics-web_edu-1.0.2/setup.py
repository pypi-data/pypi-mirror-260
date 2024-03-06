import codecs
from os.path import abspath
from os.path import dirname
from os.path import join
from pkg_resources import Requirement
import re
from setuptools import setup


_COMMENT_RE = re.compile(r'(^|\s)+#.*$')


def _get_requirements(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = _COMMENT_RE.sub('', line)
            line = line.strip()
            if line.startswith('-r '):
                for req in _get_requirements(
                    join(dirname(abspath(file_path)), line[3:])
                ):
                    yield req
            elif line:
                req = Requirement(line)
                req_str = req.name + str(req.specifier)
                if req.marker:
                    req_str += '; ' + str(req.marker)
                yield req_str


def _read(file_name):
    with codecs.open(file_name, 'r', encoding='utf-8') as infile:
        return infile.read()


def main():
    setup(
        namespace_packages=(
            'edu_to_analytics',
        ),
        name='edu-to-analytics-web_edu',
        version='1.0.2',
        author='БАРС Груп',
        author_email='education_dev@bars-open.ru',
        description=_read('readme.txt'),
        url='https://stash.bars-open.ru/projects/EDUBASE/repos/edu_to_analytics',
        packages=['edu_to_analytics.data'],
        include_package_data=True,
        install_requires=tuple(_get_requirements('requirements.txt')),
    )


if __name__ == '__main__':
    main()
