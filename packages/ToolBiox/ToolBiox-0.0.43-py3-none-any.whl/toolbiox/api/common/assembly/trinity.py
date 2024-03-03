from toolbiox.api.common.mapping.hisat2 import HISAT2_JOB
from toolbiox.api.common.assembly import parse_fastq_arg
from toolbiox.config import trinity_path
from toolbiox.lib.common.os import cmd_run, mkdir, have_file
import warnings
import os


class TRINITY_JOB(object):
    """
    TRINITY_JOB

    fq1 = "fq1.fq" or fq1 = ["s1.fq1.fq","s2.fq1.fq"]
    fq2 = "fq2.fq" or fq2 = ["s1.fq2.fq","s2.fq2.fq"]
    work_dir = "/home/work/trinity_job"
    reference = "genome.fasta"

    test_trinity_job = TRINITY_JOB("test", fq1, fq2, reference, work_dir=work_dir)
    test_trinity_job.run()
    """

    def __init__(self, job_id=None, fq1=None, fq2=None, reference=None, sorted_bam=None, work_dir=None, max_memory='50G', threads=8, debug=False):
        fq1, fq2, c_job_id = parse_fastq_arg(fq1, fq2)

        if job_id:
            self.job_id = job_id
        else:
            self.job_id = c_job_id

        self.fq1 = fq1
        self.fq2 = fq2
        self.sorted_bam = sorted_bam
        self.max_memory = max_memory
        self.threads = threads
        self.reference = os.path.abspath(reference) if reference else None
        self.work_dir = os.path.abspath(
            work_dir) if work_dir else os.path.abspath(os.path.curdir)
        self.debug = debug

        if self.work_dir:
            mkdir(self.work_dir, True)

    def run(self):
        if self.reference or self.sorted_bam:
            self.trinity_fasta = self.work_dir + "/RNA.trinity.Trinity-GG.fasta"
            self.trinity_gene_trans_map = self.work_dir + \
                "RNA.trinity.Trinity-GG.fasta.gene_trans_map"
        else:
            self.trinity_fasta = self.work_dir + "/RNA.trinity.Trinity.fasta"
            self.trinity_gene_trans_map = self.work_dir + \
                "/RNA.trinity.Trinity.fasta.gene_trans_map"

        if have_file(self.trinity_fasta) and have_file(self.trinity_gene_trans_map):
            warnings.warn("Trinity already run, skip!")
            return

        if self.reference:
            map_dir = os.path.join(self.work_dir, 'map')
            ht2_map_job = HISAT2_JOB(self.job_id, self.fq1, self.fq2,
                                     'RNA', self.reference, map_dir, self.threads, self.debug)
            ht2_map_job.map()

            cmd_string = "%s --genome_guided_bam %s --max_memory %s --genome_guided_max_intron 50000 --CPU %d --full_cleanup --output RNA.trinity" % (
                trinity_path, ht2_map_job.bam_file, self.max_memory, self.threads)

        elif self.sorted_bam:
            cmd_string = "%s --genome_guided_bam %s --max_memory %s --genome_guided_max_intron 50000 --CPU %d --full_cleanup --output RNA.trinity" % (
                trinity_path, self.sorted_bam, self.max_memory, self.threads)

        else:
            if self.fq2 is None:
                cmd_string = '%s --seqType fq --max_memory %s --single %s --CPU %d --output RNA.trinity --full_cleanup' % (
                    trinity_path, self.max_memory, self.fq1, self.threads)
            else:
                cmd_string = '%s --seqType fq --max_memory %s --left %s --right %s --CPU %d --output RNA.trinity --full_cleanup' % (
                    trinity_path, self.max_memory, self.fq1, self.fq2, self.threads)

        f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=False)

        if not f:
            print(o)
            print(e)
            raise ValueError("Trinity pipeline failed, see above!")

        return


if __name__ == "__main__":
    # trinity example
    # genome_guided
    ref_fa = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/HiC_scaffold_1.fa'
    fq1 = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6_1.clean.fq.gz'
    fq2 = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6_2.clean.fq.gz'
    work_dir = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/test'

    test_trinity_job = TRINITY_JOB('test', fq1, fq2, ref_fa, work_dir)
    test_trinity_job.run()

    work_dir = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/test'
    sorted_bam = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6.sorted.bam'

    test_trinity_job = TRINITY_JOB(
        'test', sorted_bam=sorted_bam, work_dir=work_dir)
    test_trinity_job.run()

    # denovo
    fq1 = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6_1.clean.fq.gz'
    fq2 = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6_2.clean.fq.gz'
    work_dir = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/test'

    test_trinity_job = TRINITY_JOB('test', fq1, fq2, work_dir=work_dir)
    test_trinity_job.run()
