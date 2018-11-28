import click
import yaml
import io
import os

@click.command()
@click.option('--source', '-s', help='Provide the path to the folder where the gitlab CI, .gitlab-ci.yml, file resides.')
@click.option('--destination', '-d', help='Optionally: Provide the path where you want to save the Bitbucket Pipeline, bitbucket-pipelines.yml, file. By default it will use the same source path.')
def main(source, destination):
  if source is None:
    click.echo('--source or -s is required, you need to specify a file to export.')
    return

  gitlab_ci_file = source
  if os.path.isdir(gitlab_ci_file):
    gitlab_ci_file = os.path.join(source, '.gitlab-ci.yml')

  with open(gitlab_ci_file, 'r') as stream:
    gitlab_ci_data = yaml.load(stream)
    # Remove everything but jobs, more info https://docs.gitlab.com/ee/ci/yaml/README.html#jobs
    reserved_keywords = [
      'image',
      'services',
      'stages',
      'types',
      'before_script',
      'after_script',
      'variables',
      'cache',
    ]
    jobs_data = { key:gitlab_ci_data[key] for key in gitlab_ci_data if key not in reserved_keywords }
    print(jobs_data)

if __name__ == '__main__':
  main()
