import tempfile

import click

from src.snpkit import generate_bedfile, generate_fasta, generate_snp_reference


@click.group()
def snpkit():
    """SNP kit to help process snps."""
    pass


@snpkit.command()
@click.option('--snp-list', required=True, help='Snp list file')
@click.argument('output')
def bedfile(snp_list: str, output: str):
    """Create bed file from snp list."""
    generate_bedfile(snp_list, output)


@snpkit.command()
@click.option('--snp-list', required=True, help='Snp list file')
@click.option('--fasta', required=True, help='Tabbed fasta file')
@click.option('--limit', is_flag=True, help='Limit to unknow SNPs')
def gen_fromfasta(snp_list: str, fasta: str, limit: bool):
    """Generate snp reference file from fasta bed."""
    generate_snp_reference(snp_list, fasta, limited=limit)


@snpkit.command()
@click.option('--snp-list', required=True, help='Snp list file')
@click.option('--fasta', required=True, help='Build37 Fasta reference')
@click.argument('output')
def getfasta(snp_list: str, fasta: str, output: str):
    """Generate fasta from reference."""
    with tempfile.NamedTemporaryFile() as f_bed:
        generate_bedfile(snp_list, f_bed.name)
        generate_fasta(f_bed.name, fasta, output)


if __name__ == '__main__':
    snpkit()
