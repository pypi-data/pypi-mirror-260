### dekcli

```shell
# Add site, then adding local ssh token to the site settings
dekcli gitea site https://sample.com

dekcli gitea index /path/to/git/dirs/tree

# Add secrets according to index.yaml

dekcli gitea push /path/to/git/dirs/tree
dekcli gitea pull /path/to/git/dirs/tree
```
