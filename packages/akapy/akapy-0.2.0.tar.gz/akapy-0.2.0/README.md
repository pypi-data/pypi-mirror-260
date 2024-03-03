# akapy

Home to a Python wrapper for the Akamai API.

## How to use?

```python
import akapy as ak

cloudlet = ak.Cloudlet()
print(cloudlet.get_all())

```

<!--TODO: Go through this and add better use cases and how to use-->
Akapy has an authentication class which is passed, when needed, to other classes within Akapy. For most use cases you probably won't need to mess
around with it. The defaults for it are 

## How to can I help?

### Prerequisites
- [Ppre-commit](https://pre-commit.com/)
- [Poetry](https://python-poetry.org/)

### Pull the Repo

#### My way

```zsh
mkdir -p $HOME/repos/open-source
git clone https://github.com/RemoteRabbit/akapy.git >> $HOME/repos/open-source
tms $HOME/repos/open-source/akapy

# If you don't use tmux-session-wizard
cd $HOME/repos/open-source/akapy
```

#### Setup pre-commit

Once you have pre-commit installed and the repo pulled down to your local machine, `cd` into it. Once in run:

```sh
pre-commit install
```

After that you can continue on and when you go to commit any changes you'll see some base tests run beforehand that you'll want to make sure are in
working order before pushing the change up.

## Notes
- [ ] Make a docs site
- [ ] TESTS

## Links

- [Mkdocs material](https://squidfunk.github.io/mkdocs-material/)

## Questions
