from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='astrocubelib',
      version='1.2.0',
      description='Utilities to handle astronomy data cube.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='J. A. Hernandez-Jimenez',
      author_email='joseaher@gmail.com',
      url = "https://gitlab.com/joseaher/astrocubelib",
      packages=['astrocubelib'],
      scripts = ['scripts/cube.py', 'scripts/cube_fig.py',
                 'scripts/cube_channelvel.py', 'scripts/guimask.py',
                 'scripts/mask.py', 'scripts/guisplot.py',
                 'scripts/plot_spec.py', 'scripts/cube_manga.py'],
      package_data = {'astrocubelib':['functions.py']},
      include_package_data =  True

      )
