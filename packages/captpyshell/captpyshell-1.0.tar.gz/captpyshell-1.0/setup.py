from distutils.core import setup
setup(
  name = 'captpyshell',         # How you named your package folder (MyLib)
  packages = ['captpyshell'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'python debugger, inject code into python prosses',   # Give a short description about your library
  author = 'kapten-kaizo',                   # Type in your name
  author_email = 'cyber2687@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/kapten-kaizo/pyshell/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kapten-kaizo/captpyshell/archive/refs/tags/V1.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',      #Specify which pyhton versions that you want to support
  ],
)
