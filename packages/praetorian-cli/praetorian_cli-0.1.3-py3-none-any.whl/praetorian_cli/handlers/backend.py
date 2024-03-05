import click

from functools import wraps

from praetorian_cli.sdk.chaos import Chaos


def handle_api_error(func):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            click.secho(e.args[0], fg='red')
    return handler


@click.group()
@click.pass_context
def chaos(ctx):
    """ Chaos API access """
    ctx.obj = Chaos(account=ctx.obj)


@chaos.command('my-assets')
@click.pass_obj
@handle_api_error
def my_assets(controller):
    """ Fetch up to 1000 assets """
    result = controller.my_assets()
    for hit in result['items']:
        print(f"{hit['composite']}")


@chaos.command('my-jobs')
@click.pass_obj
@handle_api_error
def my_jobs(controller):
    """ Fetch up to 1000 jobs """
    result = controller.my_jobs()
    for hit in result['items']:
        print(f"{hit['composite']}")


@chaos.command('my-risks')
@click.pass_obj
@handle_api_error
def my_risks(controller):
    """ Fetch up to 1000 risks """
    result = controller.my_risks()
    for hit in result['items']:
        print(f"{hit['composite']}")


@chaos.command('my-files')
@click.pass_obj
@handle_api_error
def my_files(controller):
    """ Fetch all file names """
    for hit in controller.my_files():
        print(hit)


@chaos.command('upload')
@click.pass_obj
@handle_api_error
@click.argument('name')
def upload(controller, name):
    """ Upload a file and analyze it for risks """
    if controller.upload(name):
        print('[+] File uploaded successfully')
    else:
        click.secho('[-] File failed to upload', fg='red')


@chaos.command('download')
@click.pass_obj
@handle_api_error
@click.argument('key')
def download(controller, key):
    """ Download any previous uploads """
    if controller.download(key):
        print('[+] File downloaded successfully')
    else:
        click.secho('[-] File failed to download', fg='red')


@chaos.command('trigger')
@click.pass_obj
@handle_api_error
@click.argument('capability', type=click.Choice(['nmap', 'screenshot', 'nuclei']))
@click.option('-asset', '--asset', required=True, help="Asset to trigger the capability on.")
def trigger(controller, asset, capability):
    """ Invoke a capability """
    job = controller.trigger(capability, {"asset": asset})
    print(f"Job {job['id']} initiated")
