from toolbiox.config import cap3_path
from toolbiox.api.common import JOB
from toolbiox.lib.common.os import cmd_run, get_file_name
from toolbiox.lib.common.genome.seq_base import read_fasta_by_faidx
import os


class CAP3_JOB(JOB):
    def __init__(self, input_seqs_list=None, input_fasta_file=None, work_dir=None, clean=True, job_id=None):
        super(CAP3_JOB, self).__init__(
            job_id=job_id, work_dir=work_dir, clean=clean)

        self.build_env()

        # write input fasta file
        if input_fasta_file:
            self.file_attr_check(input_fasta_file, 'input_fasta_file')
        elif input_seqs_list:
            self.input_fasta_file = os.path.join(
                self.work_dir, "input.fasta")
            with open(self.input_fasta_file, 'w') as f:
                for seq in input_seqs_list:
                    f.write(">%s\n%s\n" % (seq.seqname_short(), seq.seq))
        else:
            raise ValueError("No input file or seq list!")

    def run(self):
        cmd_string = "%s %s -o 40 -p 90 >/dev/null" % (
            cap3_path, self.input_fasta_file)
        f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=True)

        if not f:
            print(o)
            print(e)
            raise ValueError("CAP3 failed, see above info!")

        self.parse()
        self.clean_env()

        return self.assembly_seq_dict

    def parse(self):
        self.cap_contig_file = "%s/%s.cap.contigs" % (
            self.work_dir, get_file_name(self.input_fasta_file))
        self.cap_singlet_file = "%s/%s.cap.singlets" % (
            self.work_dir, get_file_name(self.input_fasta_file))

        self.contig_dict = {}
        if os.path.getsize(self.cap_contig_file):
            self.contig_dict = read_fasta_by_faidx(self.cap_contig_file)

        self.singlet_dict = {}
        if os.path.getsize(self.cap_singlet_file):
            self.singlet_dict = read_fasta_by_faidx(self.cap_singlet_file)

        self.assembly_seq_dict = {}
        num = 0
        for s_id in self.contig_dict:
            num += 1
            new_s_id = "cap_" + str(num)
            seq = self.contig_dict[s_id]
            seq.id = new_s_id
            seq.seqname = new_s_id
            self.assembly_seq_dict[new_s_id] = seq
        for s_id in self.singlet_dict:
            num += 1
            new_s_id = "cap_" + str(num)
            seq = self.singlet_dict[s_id]
            seq.id = new_s_id
            seq.seqname = new_s_id
            self.assembly_seq_dict[new_s_id] = seq

        return self.assembly_seq_dict


if __name__ == '__main__':
    # CAP3 example
    from toolbiox.api import CAP3_JOB

    input_fasta_file = "/lustre/home/xuyuxing/Feng/Work/Shikonin/family_trans/1/1.fa"

    cap3_job = CAP3_JOB(input_fasta_file=input_fasta_file)
    cap3_job.run()
    for i in cap3_job.assembly_seq_dict:
        print(cap3_job.assembly_seq_dict[i].seq)

    # CAP3 example
    from toolbiox.api import CAP3_JOB
    from toolbiox.lib.common.genome.seq_base import FastaRecord

    seq1 = """
GAATAAACCAATAATATAGTATTGACCCTCTAACTTCCCATCAGAATTCTTACATTGCAA
GAGAAAGAAAAAATCAAAGAATATCCTTGGTCAACGCAAAGAGATCACAAGTCAAAAAGT
TTCCAAAGAAGTATAAAATCTGCAGCTTAAGAAAATAATTTGACATTAATTTATCCAAGT
TTGCTGTATTTTTGGGACACTTTTGATCAGTTCGATGGTTAAGGAAACAGAATATTATGA
TGTTCTTGGTGTTAGTCCCACAGCTACTGAAGCTGAGATCAAGAAAGCTTATTACATCAA
GGCACGACAGGTCCATCCAGATAAAAACCCAAATGATCCTTTGGCGGCTCAAAATTTCCA
GGTTCTGGGCGAGGCTTACCAAGTATTGAGTGATCCATCCCAACGACAGGCATATGATTC
TTATGGAAAATCAGGAATCTCCGCTGAAGCAATCATTGATCCTGCAGCTATTTTTGCAAT
GCTTTTTGGGAGTGAACTTTTTGAAGAATACATTGGCCAGCTTGCCATGGCATCAATGGC
TTCACTGGATATCTTCACAGAAAGTGAAGCTTTTGATGCCAAAAAATTGCAGGAGCAGAT
GAGGGTGGTCCAAAAAGAAAGGGAAGAGAAACTTGTTCAAATTTTGAAAGATAGGCTACA
TCTCTATGTTCAAGGTAATAAAGACGACTTTGTTCGTCAAGCTGAAGCAGAAGTTTCAAG
ACTGTCCGGTGCAGCCTATGGTGTCGACATGTTAACTACAATTGGATACATATATTCAAG
GCAGGCAGCTAAAGAACTTGGAAAGAAGGCAATATATTTAGGTGTTCCGTTTGTTGCTGA
ATGGTTCAGAAACAAGGGGCACACTTTAAAATCCCATGTAACCGCAGCAACAGGTGCAAT
TGCTTTGATGCAACTACAAGAGGACATGAAACAGCAGCTCAGTGCAGAGAGAAACTTCAC
TGAGGAACAGGTTGAGGAATACATGGAATCTCATAAGAAAGTGATGGTTGATTCACTATG
GAAACTCAATGTTGCTGATATTGAAGCCACCTTATCCCGTGTTTGTCTAATGGTTTTACA
AGATAGTAATGTGAAGAAAGAGGAGCTTCGTGCCCGAGCAAAGGGATTAAAAACTCTTGG"""

    seq2 = """
TTCACTGGATATCTTCACAGAAAGTGAAGCTTTTGATGCCAAAAAATTGCAGGAGCAGAT
GAGGGTGGTCCAAAAAGAAAGGGAAGAGAAACTTGTTCAAATTTTGAAAGATAGGCTACA
TCTCTATGTTCAAGGTAATAAAGACGACTTTGTTCGTCAAGCTGAAGCAGAAGTTTCAAG
ACTGTCCGGTGCAGCCTATGGTGTCGACATGTTAACTACAATTGGATACATATATTCAAG
GCAGGCAGCTAAAGAACTTGGAAAGAAGGCAATATATTTAGGTGTTCCGTTTGTTGCTGA
ATGGTTCAGAAACAAGGGGCACACTTTAAAATCCCATGTAACCGCAGCAACAGGTGCAAT
TGCTTTGATGCAACTACAAGAGGACATGAAACAGCAGCTCAGTGCAGAGAGAAACTTCAC
TGAGGAACAGGTTGAGGAATACATGGAATCTCATAAGAAAGTGATGGTTGATTCACTATG
GAAACTCAATGTTGCTGATATTGAAGCCACCTTATCCCGTGTTTGTCTAATGGTTTTACA
AGATAGTAATGTGAAGAAAGAGGAGCTTCGTGCCCGAGCAAAGGGATTAAAAACTCTTGG
GAAAATTTTCCAGGTGCGCTAACTTAGTATATCCATTTCCCTGTAGTAAAGAACATGTTA
TTTTTGTTGTCCAAAATCCTGATTATCTCTTTTTTTCTTTCCCTCACTGCTCCTCCTTCC
CGGAACACATAATATTAGAGGGCTAAGTCCACCAATCCAAGTGATGCTGAAACCGTCTTA
GGCACTCCAGCAAACCAACAATTGAATGGGGGTGACACATCTCCGGGTGCTAGTACTACA
GAGAGATCTGCCTATTCGGCTAACCTTCCTAATTCTGCATTCGCACCTCAGAGTCCATAC
GTGGAGGCTCCTCAAATTGGCGGCACAGAGATTAATTTTAACTTGCCCATGCCAGCCGCA
CCCCCTGGTGCACAGAGACACGCATAAAGATGCAATCCGACCTGTTGTGCATAATTCTTC
TTTCAAATGTTGTGTTCGAAGGATACCATGTTAGAACGCCTCAAACAGCTGGGAAGGGCT
CGATTATGGCGCGCAGTGTGGAAATCACTTAACACTCCCCATTTCTAGTACCAACGTTTT
GCTGATTAATAATTTATCTCTCATGTGCAGCCACTCAGTTGTTTGGTTTAGGTGTATCTT
ATGAGATGCAGCATAAGAAATGAGATTGATTTTAGTGTGTTGAAAACCAGGTAATTTAAG
TACAATAATTATATGCTTGAATTATTTTATATAAATATTTTTACTATATGATGGACCTTC
ATAAATAATGGATA"""

    input_seqs_list = []
    input_seqs_list.append(FastaRecord("seq1", seq1))
    input_seqs_list.append(FastaRecord("seq2", seq2))

    cap3_job = CAP3_JOB(input_seqs_list=input_seqs_list)
    cap3_job.run()
    for i in cap3_job.assembly_seq_dict:
        print(cap3_job.assembly_seq_dict[i].seq)
