**Install sphinx**

(*preferably be done on only one computer*)

  - Instlall from pip under root or a conda environment `pip install sphinx sphinx-autobuild`
  - Make dir and initialize files with sphinx-quickstart
  ```
  mkdir sphinx_doc
  
  cd sphinx_doc 
  
  sphinx-quickstart
  ```
  now `sphinx_doc` should have a crucial file `Makefile` in it and that is all we want
  
  
**Pull from github and edit it**

  - After pulling from github, find the files needed to be edited, for example, `installaiton.txt` or `testing.txt`
  - Use syntax introduced on http://www.sphinx-doc.org/en/stable/rest.html#rst-primer and modify contents at files needed to be edited
  
**Build html and push to github.io**

(*preferably be done on only one computer*)

  - Navigate to the directory with all `.txt` files. Use command `make html` at the same level of `Makfile` file
  - Command prompt will tell you where those `html` files are built to. 
  Now we can push these files to certain `github.io` repo and publish this website.
