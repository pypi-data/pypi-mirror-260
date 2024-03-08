## **ISeqDb** - Identify Sequences in Databases

Screening of query sequences for the presence of specific target genes.

*Query sequences* can be genomes, MAGs, contigs/scaffolds, multifasta and fasta files. Typically, *databases* contain multifasta homologous sequences.

ISeqDd was tested to search for target genes in bacterial MAGs. ISeqDb was written primarily to search for the presence of genes encoding cyanotoxins and other genes encoding metabolites hazardous to human health in cyanobacterial MAGs. Currently available databases include DNA sequences of genes encoding microcystins (*mcyB*, *mcyD*, *mcyE*), anatoxins (*anaC*, *anaF*) and geosmin.

Any other database of homologous sequences can be used. This includes, for example, the *rbcL* gene used to classify diatoms.

At present, only DNA sequences are supported.

## Installation

### Requirements

python>=3.10, pandas, blast>=2.15, pip

conda/mamba should be already installed (https://mamba.readthedocs.io/en/latest/)

### Conda and pip

Install dependencies creating a conda environment (through conda or mamba)

*mamba create -y --name ISeqDb python>=3.10*

*mamba activate ISeqDb*

*mamba install -y -c bioconda -c conda-forge python>=3.10 pandas blast>=2.15 pip*

Install ISeqDb

pip install -i https://test.pypi.org/simple/ ISeqDb==0.0.1a0

### Usage

*ISeqDb path_to/queryfile.fasta path_to/targetdatabase.tar.gz path_to/outputfile.txt*

### Arguments

#### positional arguments

queryfile: query file, fasta/multi-fasta format

targetdatabase: Target database for the blast analysis

outputfile: Output name text file

#### options:
  -h, --help: show this help message and exit

  -p MINPIDENT, --minpident MINPIDENT; Keep hits with pident >= minpident; default=85

  -k {megablast,blastn}, --task {megablast,blastn} Task: megablast, blastn, default=megablast

  -m MAXTARGSEQ, --maxtargseq MAXTARGSEQ Keep max target sequences >= maxtargseq; default=100

  -e MINEVALUE, --minevalue MINEVALUE Keep hits with evalue >= minevalue; default=1e-6

  -t THREADS, --threads THREADS Number of threads to use; default=1

  -s SORTOUTPUT, --sortoutput SORTOUTPUT Sort output by colname. eg.: bitscore, pident, alignment_length; default=bitscore

  -d {comma,semicolon,tab}, --delimiter {comma,semicolon,tab} Output delimiter: comma, semicolon, tab; default=comma

  -v, --version: show program's version number and exit

### Output legend (in square brackets, the blast codes)

   query_id:                    query/sequence identifier [qacc]

   subject_accession:           NCBI accession number or subject identifier in the database [sacc]

   pident:                      percentage of identical matches in query and subject sequences [pident]

   n_ident_match:               number of identical bases/matches [nident]

   n_diff_match:                number of different bases/matches [mismatch]

   n_gaps:                      total number of gaps [gaps]

   alignment_length:            length of the alignemnt between query and subject sequences [length]

   query_start_al:              start of alignment in query [qstart]

   query_end_al:                end of alignment in query [qend]

   subj_start_al:               start of alignment in subject [sstart]

   subj_end_al:                 end of alignment in subject [send]

   bitscore:                    bit score [bitscore]

   evalue:                      expect value [evalue]

   subject_seq_title:           title of subject sequence in database [stitle]

   align_query_seq:             aligned part of query sequence [qseq]

   align_subj_seq:              aligned part of subject sequence [sseq]

___
   ISeqDb relies on BLAST®:

   -   BLAST® Command Line Applications User Manual [Internet]. Bethesda (MD): National Center
       for Biotechnology Information (US); 2008-.
   -   Camacho C., Coulouris G., Avagyan V., Ma N., Papadopoulos J., Bealer K., Madden T.L. (2008)
       “BLAST+: architecture and applications.” BMC Bioinformatics 10:421. PubMed


