import csv
import gzip


def generate_bedfile(output, snp_list):
    with gzip.open(snp_list, mode='rt') as fin:
        reader = csv.reader(fin, delimiter='\t')
        next(reader)  # skip header

        snps = []
        for line in reader:
            if len(line) >= 3 and (not line[1] or not line[2]):
                # chromosome or position are empty
                continue

            chrom = int(line[1])
            pos = int(line[2])

            snps.append((chrom, pos))
    snps = sorted(snps)
    with gzip.open(output, mode='wt') as fout:
        writer = csv.writer(fout, delimiter='\t')
        for chrom, pos in snps:
            writer.writerow([chrom, pos - 1, pos])