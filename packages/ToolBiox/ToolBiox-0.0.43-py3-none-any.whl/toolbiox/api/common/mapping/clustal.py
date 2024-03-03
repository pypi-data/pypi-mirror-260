from toolbiox.config import clustalo_path, clustalw_path
from toolbiox.api.common import JOB
from toolbiox.lib.common.os import cmd_run, rmdir, copy_file
from toolbiox.lib.common.genome.seq_base import read_fasta
import os


class CLUSTAL_JOB(JOB):
    def __init__(self, input_seqs_list=None, input_fasta_file=None, output_file=None, seq_type='PROTEIN', work_dir=None, threads=8, command='clustalw', clean=True, job_id=None):
        """
        seq_type: DNA or PROTEIN
        command: clustalo or clustalw
        """
        super(CLUSTAL_JOB, self).__init__(
            job_id=job_id, work_dir=work_dir, clean=clean)

        self.output_file = os.path.abspath(
            output_file) if output_file else None
        self.threads = threads
        self.seq_type = seq_type
        self.command = command
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
        tmp_output_file = os.path.abspath(
            os.path.join(self.work_dir, "output.aln.fasta"))

        if self.command == 'clustalo':
            if self.seq_type == 'DNA':
                cmd_string = "%s -i %s -o %s --threads=%s --force --auto" % (
                    clustalo_path, self.input_fasta_file, tmp_output_file, self.threads)
            elif self.seq_type == 'PROTEIN':
                cmd_string = "%s -i %s -o %s --threads=%s --force --auto --seqtype=Protein" % (
                    clustalo_path, self.input_fasta_file, tmp_output_file, self.threads)
        elif self.command == 'clustalw':
            if self.seq_type == 'DNA':
                cmd_string = "%s  -INFILE=%s -ALIGN -OUTPUT=FASTA -OUTFILE=%s -type=DNA" % (
                    clustalw_path, self.input_fasta_file, tmp_output_file)
            elif self.seq_type == 'PROTEIN':
                cmd_string = "%s  -INFILE=%s -ALIGN -OUTPUT=FASTA -OUTFILE=%s -type=protein" % (
                    clustalw_path, self.input_fasta_file, tmp_output_file)

        f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=True)

        if not f:
            print(o)
            print(e)
            raise ValueError("Clustal failed, see above info!")

        if self.output_file:
            if self.output_file != tmp_output_file:
                copy_file(tmp_output_file, self.output_file)
                rmdir(tmp_output_file)
        else:
            self.output_file = tmp_output_file

        self.parse()
        self.clean_env()

        return self.aln_seq_dict

    def parse(self):
        self.aln_seq_dict = read_fasta(self.output_file)[0]


if __name__ == '__main__':
    # clustal example
    from toolbiox.api.common.mapping.clustal import CLUSTAL_JOB

    input_fasta_file = "/lustre/home/xuyuxing/Work/orcidWGD2/WGD_identification2/orchid_OCF/2.tree/fasttree/OG0004557/pt.fa"
    work_dir = "/lustre/home/xuyuxing/Work/orcidWGD2/WGD_identification2/orchid_OCF/2.tree/fasttree/OG0004557/test"
    output_file = "/lustre/home/xuyuxing/Work/orcidWGD2/WGD_identification2/orchid_OCF/2.tree/fasttree/OG0004557/test/pt.aln.fa"

    clustal_job = CLUSTAL_JOB(input_fasta_file=input_fasta_file, output_file=output_file, work_dir=work_dir, command='clustalw',clean=False)
    clustal_job.run()
    print(clustal_job.aln_seq_dict)

    # clustal example
    from toolbiox.api import CLUSTAL_JOB
    from toolbiox.lib.common.genome.seq_base import FastaRecord

    input_seqs_list = []
    input_seqs_list.append(FastaRecord("seq1", "ATCGATCGATCATCGATCATCGATCATCG"))
    input_seqs_list.append(FastaRecord("seq2", "ATCGATCGATCGATCGATCGATCGATCGATCG"))
    input_seqs_list.append(FastaRecord("seq3", "ATCGTTCGATCGTTCGATCGTTCGATCGTTCG"))
    
    clustal_job = CLUSTAL_JOB(input_seqs_list=input_seqs_list, seq_type='DNA')
    clustal_job.run()

    for s in clustal_job.aln_seq_dict:
        print(s)
        print(clustal_job.aln_seq_dict[s].seq)

    print(clustal_job.aln_seq_dict)


