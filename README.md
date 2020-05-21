<p align="center"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/236/black-universal-recycling-symbol_267b.png"></p>
<h1 align="center">SWAP</h1>
<h3 align="center">Simple components sharing tool</h3>


# Installation

```bash
pip install swp
```

## Optionnal dependencies

```bash
# Linux
apt install tree

# MacOS
brew install tree
```

# Usage

swap.yaml example
```yaml
components:
  components: components/shared
remote: git@github.com:vuejs/ui.git
remote-directory: ./src
version: 1
```
This config example will create a directory on your project called `shared` in the `components` subfolder.

In this folder will apear all the files from the [`vuejs/ui` repository](https://github.com/vuejs/ui/tree/master/src/components).


## Commands

- `swp init` Will guide you for creating a new config file.
- `swp tree` Will show you the path structure of the repo.
- `swp pull` Will git pull the remote repository and apply the config to copy files into your project.
- `swp push` Will commit and push the changes you made on all **swapped files/folders**, we recommand you to Fork repositories like `vuejs/ui` to have write rights.
- `swp add` Will create a new shared path.
- `swp rm` Will delete a shared path.
- `swp get` Will get a new path from dist repo.