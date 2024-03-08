#!/usr/bin/env python3
# ISeqDb - Identify Sequences in Databases
# version 0.0.2
# Nico Salmaso, FEM, nico.salmaso@fmach.it

import textwrap
import argparse
import pandas as pd
import os
import tarfile
from argparse import ArgumentParser, Namespace
from pandas import DataFrame


def main():
    # Argument parser
    # parser: ArgumentParser = argparse.ArgumentParser(description='ISeqDb v. 0.0.2')

    parser: ArgumentParser = argparse.ArgumentParser(
        description='ISeqDb v. 0.0.2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\

             Author: Nico Salmaso (nico.salmaso@fmach.it)
             
             Output legend (in square brackets, the blast codes)
                ---
                query_id:		        query/sequence identifier [qacc]
                subject_accession:	        NCBI accession number or subject identifier in the database [sacc]
                pident:			percentage of identical matches in query and subject sequences [pident]
                n_ident_match:		number of identical bases/matches [nident]
                n_diff_match:		number of different bases/matches [mismatch]
                n_gaps:			total number of gaps [gaps]
                alignment_length:	        length of the alignemnt between query and subject sequences [length]
                query_start_al:		start of alignment in query [qstart]
                query_end_al:		end of alignment in query [qend]
                subj_start_al:		start of alignment in subject [sstart]
                subj_end_al:		        end of alignment in subject [send]
                bitscore:			bit score [bitscore]
                evalue:			expect value [evalue]
                subject_seq_title:		title of subject sequence in database [stitle]
                align_query_seq:		aligned part of query sequence [qseq]
                align_subj_seq:		aligned part of subject sequence [sseq]
                                              
                ISeqDb relies on BLAST®:
                
                -   BLAST® Command Line Applications User Manual [Internet]. Bethesda (MD): National Center
                    for Biotechnology Information (US); 2008-.
                -   Camacho C., Coulouris G., Avagyan V., Ma N., Papadopoulos J., Bealer K., Madden T.L. (2008)
                    “BLAST+: architecture and applications.” BMC Bioinformatics 10:421. PubMed
                ---
             ''')
    )

    parser.add_argument('queryfile', default=None,
                        help="Input query file, fasta/multi-fasta format")

    parser.add_argument('targetdatabase', default=None,
                        help="Target database for the blast analysis")

    parser.add_argument('outputfile', default=None,
                        help="Output name text file")

    parser.add_argument('-p', '--minpident', type=int, required=False, default=85,
                        help="Keep hits with pident >= minpident; default=85")

    parser.add_argument('-k', '--task', required=False, default="megablast", choices=['megablast', 'blastn'],
                        help="Task: megablast, blastn, default=megablast")

    parser.add_argument('-m', '--maxtargseq', type=int, required=False, default=100,
                        help="Keep max target sequences >= maxtargseq; default=100")

    parser.add_argument('-e', '--minevalue', type=float, required=False, default=1e-6,
                        help="Keep hits with evalue >= minevalue; default=1e-6")

    parser.add_argument('-t', '--threads', type=int, required=False, default=2,
                        help="Number of threads to use; default=1")

    parser.add_argument('-s', '--sortoutput', required=False, default="bitscore",
                        help="Sort output by colname. eg.: bitscore, pident, alignment_length; default=bitscore")

    parser.add_argument('-d', '--delimiter', required=False, default="comma", choices=['comma', 'semicolon', 'tab'],
                        help="Output delimiter: comma, semicolon, tab; default=comma")

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.2')

    args: Namespace = parser.parse_args()

    # Print argument values
    print(' ')
    print('_____________________________________')
    print(' ')
    print("queryfile:", args.queryfile)
    print('')
    print("targetdatabase:", args.targetdatabase)
    print('')
    print("outputfile:", args.outputfile)
    print('')
    print("minpident:", args.minpident)
    print('')
    print("task:", args.task)
    print('')
    print("minevalue:", args.minevalue)
    print('_____________________________________')
    print(' ')

    # split dir target db
    dirtarget, file_name_db = os.path.split(args.targetdatabase)
    diroutput, file_name_ou_1 = os.path.split(args.outputfile)
    file_name_ou = file_name_ou_1.split('.')[0]

    # extract database, and open and extract database
    datseqtar = tarfile.open(args.targetdatabase)
    # extracting file
    datseqtar.extractall(dirtarget)
    datseqtar.close()

    # remove extensions
    datseq = args.targetdatabase.split('.')[0]

    define_cmd: str = (
        f'blastn -query {args.queryfile} -db {datseq} -task {args.task} '
        f'-perc_identity {args.minpident} -dust no -evalue {args.minevalue} '
        f'-outfmt \'6 delim=  qacc sacc pident nident mismatch gaps length '
        f'qstart qend sstart send bitscore evalue stitle qseq sseq\' '
        f'-max_target_seqs {args.maxtargseq} -num_threads {args.threads} '
        f'| tee -i {args.outputfile}_nh.txt'
    )

    os.system(define_cmd)

    # cleaning 1
    os.remove(datseq + '.ndb')
    os.remove(datseq + '.nhr')
    os.remove(datseq + '.nin')
    os.remove(datseq + '.nog')
    os.remove(datseq + '.nos')
    os.remove(datseq + '.not')
    os.remove(datseq + '.ntf')
    os.remove(datseq + '.nto')
    os.remove(datseq + '.nsq')

    column_names: list[str] = ['query_id', 'subject_accession', 'pident', 'n_ident_match', 'n_diff_match',
                               'n_gaps', 'alignment_length', 'query_start_al', 'query_end_al', 'subj_start_al',
                               'subj_end_al', 'bitscore', 'evalue', 'subject_seq_title', 'align_query_seq',
                               'align_subj_seq']

    file_header = f"{args.outputfile}_nh.txt"
    output_file = f"{args.outputfile}"

    # when the file is empty (no matches)
    if os.stat(file_header).st_size == 0:
        with open(file_header, 'w') as f:
            column_names_str = '\t'.join(map(str, column_names))
            f.write(column_names_str)
            print("No matches between query and subject sequences")
            print('_____________________________________')
            print("")

    # Read the non-empty file into a DataFrame
    dframe = pd.read_csv(file_header, delimiter='\t')
    # Convert the dframe (list of lists)
    data = dframe.values.tolist()

    data.insert(0, column_names)
    dataf: DataFrame = pd.DataFrame(data)
    dataf.to_csv(output_file, sep='\t', index=False, header=False)

    # sort file
    outputfile = pd.read_csv(args.outputfile, sep='\t')
    outputfile_sorted = outputfile.sort_values(by=args.sortoutput, ascending=False)

    if args.delimiter == "semicolon":
        sorted_file_name = os.path.join(diroutput, file_name_ou + '_sorted.csv2')
        sorted_file_name = str(sorted_file_name)
        outputfile_sorted.to_csv(sorted_file_name, sep=";", index=False)
    elif args.delimiter == "tab":
        sorted_file_name = os.path.join(diroutput, file_name_ou + '_sorted.tsv')
        sorted_file_name = str(sorted_file_name)
        outputfile_sorted.to_csv(sorted_file_name, sep="\t", index=False)
    else:
        sorted_file_name = os.path.join(diroutput, file_name_ou + '_sorted.csv')
        sorted_file_name = str(sorted_file_name)
        outputfile_sorted.to_csv(sorted_file_name, sep=",", index=False)

    # cleaning 2
    os.remove(args.outputfile + '_nh.txt')


if __name__ == "__main__":
    main()
