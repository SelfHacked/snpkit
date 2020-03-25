import click

from src.snpkit import generate_bedfile


@click.group()
def snpkit():
    """SNP kit to help process snps."""
    pass


@snpkit.command()
@click.argument('snp-list')
@click.argument('output')
def bedfile(snp_list: str, output: str):
    """Create bed file from snp list."""
    generate_bedfile(output, snp_list)


if __name__ == '__main__':
    snpkit()
