# s3compress

Cli tool to compress an existing s3 bucket or prefix, compression format is bz2

## Installation :

Use pip to install s3compress

```
pip install s3compress
```

#### Alternate installation

You can also compile from source, just clone the repo and run the command below:

```
python setup.py install
```

## Getting Started :


To get started, start with --help
```
$ s3compress --help
Usage: s3compress [OPTIONS]

Options:
  -a, --access_key TEXT          aws access_key
  -s, --secret_key TEXT          aws secret_key
  -b, --bucket_name TEXT         s3 bucket name
  -d, --destination_bucket TEXT  destination s3 bucket name
  -p, --prefix TEXT              s3 prefix
  -w, --workers INTEGER          number of workers
  --help                         Show this message and exit.
 ```

Check the example usage to get started

## Example Usage :

```
$ s3compress -a xxxxxxxxxxxxxxx -s xxxxxxxxxxxxxxxxxxxxxx -b bucket1 -d bucket2 -p "/prefix/path"
Downloading file api_cluster/terraform.tfstate locally
Downloading file backend/backend.tfstate.bz2.bz2 locally
Downloading file backend/backend.tfstate locally
Downloading file elasticsearch/backend.tfstate locally
api_cluster/terraform.tfstate downloaded in /tmp
/tmp/terraform.tfstate.bz2 successfully created.
backend/backend.tfstate.bz2.bz2 downloaded in /tmp
/tmp/backend.tfstate.bz2.bz2.bz2 successfully created.
backend/backend.tfstate downloaded in /tmp
/tmp/backend.tfstate.bz2 successfully created.
elasticsearch/backend.tfstate downloaded in /tmp
/tmp/backend.tfstate.bz2 successfully created.
uploading part 1 of 1
uploading part 1 of 1
uploading part 1 of 1
uploading part 1 of 1
Successfully uploaded to s3://terraform-wynk/backend/backend.tfstate.bz2, removing local files
/tmp/backend.tfstate.bz2 uploaded
Successfully uploaded to s3://terraform-wynk/backend/backend.tfstate.bz2.bz2.bz2, removing local files
/tmp/backend.tfstate.bz2.bz2.bz2 uploaded
```

## Contributing
if your code doesn't follow the contribution guidelines it won't be merged

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. stage your feature: `git add <changed_file>`
4. Commit your changes: `git commit -m 'feat: add new feature' -m 'add my-new-feature, use it as: my-new-feautre(args)' -m 'closes #26'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request :D
