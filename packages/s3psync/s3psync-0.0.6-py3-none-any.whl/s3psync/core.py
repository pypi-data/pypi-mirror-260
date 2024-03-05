import click
from .s3cli import S3CLI


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    from . import __version__

    click.echo("Version " + __version__)
    ctx.exit()


@click.command()
@click.option("--version", is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option("--aws-profile", required=True, help="AWS profile name")
@click.option("--parent-dir", required=True, help="Parent directory to sync")
@click.option("--s3-bucket", required=True, help="S3 bucket to sync to")
@click.option(
    "--parallel-instances",
    default=1,
    help="Number of parallel instances for aws s3 sync, default is 1",
)
def main(**kwargs):
    aws_profile = kwargs["aws_profile"]
    parent_dir = kwargs["parent_dir"]
    s3_bucket = kwargs["s3_bucket"]
    parallel_instances = kwargs["parallel_instances"]

    s3cli = S3CLI(aws_profile)
    s3cli.sync(parent_dir, s3_bucket, parallel_instances)
