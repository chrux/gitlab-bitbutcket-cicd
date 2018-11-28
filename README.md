# Gitlab CI to Bitbucket Pipeline

The purpose of this utility is to be able to migrate the .gitlab-ci.yml file to bitbucket-pipelines.yml

## Dependencies

- PyYAML
- click
- PyInquirer

To intall them all, run:

`pip install -r requirements.txt`

## Run

`python export.py -s {source-path} is`

Replace {source-path} for the directory where the .gitlab-ci.yml file is.
