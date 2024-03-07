# MLVault py-pkg

How to install 

```
pip install mlvault
```

## CLI commands
provides utility commands.
You can access with 
```
mlvcli [namespace] [*args]
```

namespaces are introduced below.

### Auth

First, you need to set up your Hugging face auth token.
We need both of write and read token.

In interactive way:

```
mlvcli config
```

In one-line command:

```
mlvcli -r {read_token} -w {write_token}
```

This saves `config.ini` file in mlvault path.

### Data

Data namespace provides `Datapacks`

If you want to upload with dataset config file:

```
mlvcli data up {configfile.yml}
```

And if you want to export from dataset repo:

```
mlvcli data down {repo_id}
```

To pack dynamic datapack
```
mlvcli data pack --d <base_dir> -r <repo_id> [--f <filter_token>]
```

To extract 
