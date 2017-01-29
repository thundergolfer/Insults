from distutils.core import setup
from support.commands.py_test import UnitTest

setup(
  name = 'insults',
  packages = ['insults'], # this must be the same as the name above
  version = '0.1',
  description = 'Identify insulting comments and users on social media',
  author = 'Jonathon Belotti',
  author_email = 'jonathon.bel.melbourne@gmail.com',
  url = 'https://github.com/thundergolfer/Insults', # use the URL to the github repo
  download_url = 'https://github.com/thundergolfer/Insult/tarball/0.1', # I'll explain this in a second
  keywords = ['machine-learning', 'social-media', 'community', 'data-science'], # arbitrary keywords
  classifiers = [],
  cmdclass = {'unit': UnitTest }
)

## FOR download_url
# The download_url is a link to a hosted file with your repository's code.
# Github will host this for you, but only if you create a git tag.
# In your repository, type:
# git tag 0.1 -m "Adds a tag so that we can put this on PyPI.".
# Then, type git tag to show a list of tags — you should see 0.1 in the list.
# Type git push --tags origin master to update your code on Github with the latest tag information. Github creates tarballs for download at https://github.com/{username}/{module_name}/tarball/{tag}.
