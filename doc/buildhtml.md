**Install sphinx**

  - Install from pip under root or a conda environment `pip install sphinx sphinx-autobuild`
  
**Pull xpdSim from github and edit it**

  - After pulling from github, find the files needed to be edited. So far we take files with two extentions: `.txt` and `.md`, represents Markup and Markdown syntax respectively.
    - Markup syntax can be found at http://www.sphinx-doc.org/en/stable/rest.html#rst-primer
    - Markdown syntax can be found at https://help.github.com/articles/github-flavored-markdown
  
  - Currently the document structure is orgnized as:
    - sphinx_doc/installation.md
    - sphinx_doc/test.md
    - sphinx_doc/functionality.txt
  
**Build html and push to github.io**

(*Need to test on Windows system about building process*)

  - Navigate to the directory with all `.txt` and `.md` files. Use command `make html` at the same level of `Makfile` file
  - Command prompt will tell you where those `html` files are built to. Now we can view it locally and if we are satisfied with the look, we can push these `html` files to certain `github.io` repo and publish this website.
