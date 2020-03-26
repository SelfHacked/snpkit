import csv
import gzip
import subprocess


def generate_bedfile(snp_list, output):
    snps = _extract_bedable_snps(snp_list)
    snps = _sort_snps_by_chrom_pos(snps)
    _output_to_bedfile(output, snps)


def generate_fasta(bed_file, fasta_file, output_file):
    subprocess.run(
        [
            'bedtools',
            'getfasta',
            '-fi',
            fasta_file,
            '-bed',
            bed_file,
            '-name',
            '-tab',
            '-fo',
            output_file,
        ],
    )


def generate_snp_reference(snp_list, fasta_file, limited=False):
    with gzip.open(snp_list, mode='rt') as fin:
        reader = csv.reader(fin, delimiter='\t')
        next(reader)  # skip header

        snps = {}
        for rsid, chrom, pos, genotype, *other in reader:
            if limited and genotype:
                # skip known genotypes in limited version
                continue
            snps[rsid] = (chrom, pos, genotype, *other)

    with open(fasta_file) as fin:
        reader = csv.reader(fin, delimiter='\t')

        for name, allele in reader:
            rsid = name.split(':')[0]
            if rsid in snps:
                chrom, pos, _, *other = snps[rsid]
                print('\t'.join([rsid, chrom, pos, allele + allele, *other]))
                del snps[rsid]

        if not limited:  # don't add remaining snps in limited version
            for rsid in snps.keys():
                print('\t'.join([rsid, *snps[rsid]]))


def _sort_snps_by_chrom_pos(snps):
    snps = sorted(snps)
    return snps


def _extract_bedable_snps(snp_list, skip_known=False):
    with gzip.open(snp_list, mode='rt') as fin:
        reader = csv.reader(fin, delimiter='\t')
        next(reader)  # skip header

        snps = []
        for line in reader:
            # skip if chromosome or position are empty
            if len(line) < 3 or (not line[1] or not line[2]):
                continue

            # skp if genotype is available
            if skip_known:
                if len(line) >= 4 and len(line[3]) == 2:
                    continue

            rsid = line[0]
            chrom = int(line[1])
            pos = int(line[2])

            snps.append((chrom, pos, rsid))
    return snps


def _output_to_bedfile(output, snps):
    with open(output, mode='wt') as fout:
        writer = csv.writer(fout, delimiter='\t')
        for chrom, pos, rsid in snps:
            writer.writerow([chrom, pos - 1, pos, rsid])
