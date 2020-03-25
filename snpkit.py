import click


@click.group()
def snpkit():
    """SNP kit to help process snps."""
    pass


@snpkit.command()
@click.argument('file')
@click.argument('output')
def bedfile(file: str, output: str):
    """Create bed file from snp list."""
    pass


if __name__ == '__main__':
    snpkit()
