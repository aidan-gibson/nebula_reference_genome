import re

# got cram headers via samtools view -H nebula.cram > cramheaders.txt
cram_headers = 'cramheaders.txt'

# ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz and gunzipped it
# grep 'M5:' GCA_000001405.15_GRCh38_no_alt_analysis_set.fna > verifyref.txt
ref_headers = 'verifyref.txt'


# cram section
cram_pattern = r'^@SQ.*SN:(\S+).*M5:(\S+)'
cram_chr_m5_dict = {}
with open(cram_headers, 'r') as file:
    for line in file:
        match = re.match(cram_pattern, line)
        if match:
            chr_name = match.group(1)
            m5_value = match.group(2)
            cram_chr_m5_dict[chr_name] = m5_value
# print(cram_chr_m5_dict)
#print(len(cram_chr_m5_dict))


# ref section

ref_pattern = r'^>(\S+).*M5:(\S+)'

# Initialize the dictionary
ref_chr_m5_dict = {}

# Read the file and process each line
with open(ref_headers, 'r') as file:
    for line in file:
        match = re.match(ref_pattern, line)
        if match:
            chr_name = match.group(1)
            m5_value = match.group(2)
            ref_chr_m5_dict[chr_name] = m5_value


# print(ref_chr_m5_dict)
#print(len(ref_chr_m5_dict))

# compare
            
# Compare the dictionaries
mismatch_found = False
for chr_name, m5_value in cram_chr_m5_dict.items():
    if chr_name not in ref_chr_m5_dict:
        print(f"Chromosome {chr_name} is present in CRAM but missing in the reference.")
        mismatch_found = True
    elif ref_chr_m5_dict[chr_name] != m5_value:
        print(f"Mismatch found for chromosome {chr_name}:")
        print(f"  CRAM M5 value: {m5_value}")
        print(f"  Reference M5 value: {ref_chr_m5_dict[chr_name]}")
        mismatch_found = True

# Check for chromosomes present in the reference but missing in CRAM
for chr_name in ref_chr_m5_dict:
    if chr_name not in cram_chr_m5_dict:
        print(f"Chromosome {chr_name} is present in the reference but missing in CRAM.")
        mismatch_found = True

if not mismatch_found:
    print("No mismatches found. CRAM and reference chromosomes and M5 values match.")