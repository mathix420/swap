<p align="center"><img height="120px" width="120px" src="docs/logo.png"></p>
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

# Documentation

## Swapfile

`swap.yaml` example:
```yaml
git@github.com:mathix420/pylone.git:
    # name: local_path:remote_path@optionnal_branch_or_commitID
    pylone_utils: utils:pylone/utils

git@github.com:vuejs/ui.git:
    vue_ui: components/vue_ui:src/components
```


## Commands

- `swp init` Will guide you for creating a new config file.
- `swp tree` Will show you the path structure of remotes.
- `swp sync` Will by directionnal update of tracked modules/files.
- `swp add` Will add the specified path to the swapfile.
- `swp rm` Will remove the specified path from the swapfile.
- `swp get` Will pull a module/file from a specified remote URL and add it to the swapfile.

**More detailed documentation is available [here](/docs/guide.md)**

> As `swp sync` will push local updates to remote, I recommand you to fork repositories like `vuejs/ui` to have write rights on thems.