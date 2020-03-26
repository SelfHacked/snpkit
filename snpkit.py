import tempfile

import click

from src.snpkit import generate_bedfile, generate_fasta, generate_snp_reference


@click.group()
def snpkit():
    """SNP kit to help process snps."""
    pass


@snpkit.command()
@click.option('--snp-list', required=True, help='Snp list file')
@click.option('--limit', is_flag=True, help='Limit to unknow SNPs')
@click.argument('output')
def bedfile(snp_list: str, output: str, limit: bool):
    """Create bed file from snp list."""
    generate_bedfile(snp_list, output, skip_known=limit)


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
@click.option('--limit', is_flag=True, help='Limit to unknow SNPs')
def getref(snp_list: str, fasta: str, limit: bool):
    """Generate updated reference file."""
    with tempfile.NamedTemporaryFile(
    ) as f_bed, tempfile.NamedTemporaryFile() as f_bed_fasta:
        generate_bedfile(snp_list, f_bed.name, skip_known=limit)
        generate_fasta(f_bed.name, fasta, f_bed_fasta.name)
        generate_snp_reference(snp_list, f_bed_fasta.name, limited=limit)


if __name__ == '__main__':
    snpkit()
