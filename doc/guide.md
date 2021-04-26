# Guide

> This can be used as a component as well.
>
> And it's the case if you are seeing this file in your project after
> running the `swp init` command!


# `SWP SYNC`

```yaml
usage: swp sync [-h] [-m COMMIT_MSG] [-f] [NAME [NAME ...]]

positional arguments:
  NAME                  component(s) to sync

optional arguments:
  -h, --help            show this help message and exit
  -m COMMIT_MSG, --commit-msg COMMIT_MSG
                        commit message
  -f, --force           force pushing updates
```

### Pulling

If this file got modified over time on the remote
and if you run the command `swp sync`,
SWAP will update this file to it's latest version.

### Pushing

If you modified this file locally and have push right
to the remote, you can also run `swp sync` to automatically
update the remote version of this file.


# `SWP ADD`

```yaml
usage: swp add [-h] [-n [NAME]] PATH [DEST] REMOTE

positional arguments:
  PATH                  path of the component
  DEST                  path of the remote component
  REMOTE                git remote url

optional arguments:
  -h, --help            show this help message and exit
  -n [NAME], --name [NAME]
                        name of the component
```

To sync a new component (which do not exist on remote), you can use the command `swp add` or you can update the swapfile (`swap.yaml`) manually.

### Example

Original `swap.yaml`:
```yaml
git@github.com:example/test.git:
  readme: readme.md:README.md
```
Running:
```bash
swp add my-new-file git@github.com:example/test.git
```

Will update the swapfile like so:
```yaml
git@github.com:example/test.git:
  readme: readme.md:README.md
  my-new-file: my-new-file:my-new-file
```


# `SWP GET`

```yaml
usage: swp get [-h] [-n [NAME]] PATH [DEST] REMOTE

positional arguments:
  PATH                  remote path of the component
  DEST                  local path of the component
  REMOTE                git remote url

optional arguments:
  -h, --help            show this help message and exit
  -n [NAME], --name [NAME]
                        name of the component
```

To pull an existing component from remote and sync it, you can use `swp get`. This command is working just like `swp add` but pull the file instead of pushing it to remote.


# `SWP RM`

```yaml
usage: swp rm [-h] NAME

positional arguments:
  NAME        path of the component

optional arguments:
  -h, --help  show this help message and exit
```

To stop syncing a component, just run `swp rm MY-COMPONENT`
to remove it from the swapfile.


### Example

Original `swap.yaml`:
```yaml
git@github.com:example/test.git:
  readme: readme.md:README.md
  my-new-file: my-new-file:my-new-file
```

To stop syncing `my-new-file`:
```bash
swp rm my-new-file
```

And the swapfile will now look like this:
```yaml
git@github.com:example/test.git:
  readme: readme.md:README.md
```


# `SWP TREE`

```yaml
usage: swp tree [-h]

optional arguments:
  -h, --help  show this help message and exit
```

With this command you can view all files in all remotes present in the swapfile.


# `SWP INIT`

```yaml
usage: swp init [-h] [--remote REMOTE] [--folder FOLDER]

optional arguments:
  -h, --help            show this help message and exit
```

The `swp init` command can be used to generate a blank swapfile with comments and help to get started.