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

  bitbucket_pipeline_data = {}
  bitbucket_pipeline_data['pipelines'] = {}
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
    if 'image' in gitlab_ci_data:
      bitbucket_pipeline_data['image'] = gitlab_ci_data['image']

    if 'cache' in gitlab_ci_data:
      if 'paths' in gitlab_ci_data['cache']:
        bitbucket_pipeline_data['definitions'] = {}
        bitbucket_pipeline_data['definitions']['caches'] = {}
        for path in gitlab_ci_data['cache']['paths']:
          cache_key = ''.join([i for i in path if i.isalnum()])
          bitbucket_pipeline_data['definitions']['caches'][cache_key] = path.rstrip('/')

    jobs_data = { key:gitlab_ci_data[key] for key in gitlab_ci_data if key not in reserved_keywords }
    for job_key in jobs_data:
      job = jobs_data[job_key]
      step = { key:job[key] for key in job if key in ['image', 'script'] }
      step['name'] = f'{job_key}'
      if 'before_script' in job and job['before_script']:
        step['script'] = job['before_script'] + (step['script'] if 'script' in step else [])
      if 'after_script' in job and job['after_script']:
        step['script'] = (step['script'] if 'script' in step else []) + job['after_script']
      if 'only' in job:
        if 'branches' not in bitbucket_pipeline_data['pipelines']:
          bitbucket_pipeline_data['pipelines']['branches'] = {}
        for branch in job['only']:
          bitbucket_pipeline_data['pipelines']['branches'][branch] = []
          bitbucket_pipeline_data['pipelines']['branches'][branch].append({ 'step': step })
      else:
        bitbucket_pipeline_data['pipelines']['default'] = []
        bitbucket_pipeline_data['pipelines']['default'].append({ step: step })
  
  print(bitbucket_pipeline_data)

if __name__ == '__main__':
  main()
