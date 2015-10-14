from distutils import log
from setuptools import setup

try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names

setup(name='dumbserver',
      version='0.4',
      description='Mock several REST services in one go!',
      url='http://github.com/storborg/funniest',
      author='Varun Mulloli',
      author_email='mulloli@me.com',
      license='MIT',
      packages=['dumbserver','twisted.plugins'],
      install_requires=['PyYAML','treelib','Twisted']
)

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))