**Note of building and pushing github pages**
  
  - Modify html source codes under `master` branch
  - Checkout to `gh-pages` branch after modification: `git checkout gh-pages`
  - Take modified html source codes from `master` branch to `gh-pages` branch: `git checkout master sphinx_doc\`
  - Build html files: `make html` and result html files will be in `./_build` directory
  - Add `_build` directory and then commit this change: `git add _build\` and `git commit`
  - Push to `gh-pages` branch: `git push origin gh-pages`
  - View published web site at [here](http:chiahaoliu.github.io/xpdSim)
