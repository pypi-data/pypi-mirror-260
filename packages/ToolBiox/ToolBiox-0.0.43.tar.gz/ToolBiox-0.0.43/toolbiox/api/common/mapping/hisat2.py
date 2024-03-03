from toolbiox.api.common.assembly import parse_fastq_arg
from toolbiox.config import hisat2_path, hisat2_build_path, samtools_path
from toolbiox.lib.common.os import cmd_run, mkdir, have_file, rmdir
import os


class HISAT2_JOB(object):
    """
    HISAT2_JOB

    genome_fasta_file = "genome.fasta"
    s_id = "test"
    fq1 = "fq1.fq" or fq1 = ["s1.fq1.fq","s2.fq1.fq"]
    fq2 = "fq2.fq" or fq2 = ["s1.fq2.fq","s2.fq2.fq"]
    model = "RNA" or "DNA"
    work_dir = "/home/work/hisat2_job"

    test_hisat2_job = HISAT2_JOB(s_id, fq1, fq2, 'RNA', genome_fasta_file, work_dir)
    test_hisat2_job.build(genome_fasta_file)
    sorted_bam_file, log_file = test_hisat2_job.map(fq1,fq2)
    mapping_ratio = hisat2_job.get_mapping_rate_from_log(log_file)
    """

    def __init__(self, job_id=None, fq1=None, fq2=None, model='RNA', reference=None, work_dir=None, threads=8, debug=False):
        """
        model: RNA or DNA
        """

        fq1, fq2, c_job_id = parse_fastq_arg(fq1, fq2)

        if job_id:
            self.job_id = job_id
        else:
            self.job_id = c_job_id

        self.fq1 = fq1
        self.fq2 = fq2
        self.model = model
        self.threads = threads
        self.reference = os.path.abspath(reference) if reference else None
        self.work_dir = os.path.abspath(
            work_dir) if work_dir else os.path.abspath(os.path.curdir)
        self.debug = debug

        if self.work_dir:
            mkdir(self.work_dir, True)

    def build(self, reference=None, work_dir=None):
        # check environment
        self.reference = os.path.abspath(
            reference) if reference else self.reference
        self.work_dir = os.path.abspath(
            work_dir) if work_dir else self.work_dir

        if self.reference is None:
            raise ValueError("reference not set!")
        if self.work_dir is None:
            self.work_dir = os.path.abspath(os.path.curdir)

        # check if reference was indexed
        ht2_index_file = self.reference + ".1.ht2"
        if have_file(ht2_index_file):
            return self.reference
        ht2_index_file = self.work_dir + "/" + \
            os.path.basename(self.reference) + ".1.ht2"
        if have_file(ht2_index_file):
            self.reference = ht2_index_file
            return self.reference

        # check genome_fasta_file
        cmd_string = "%s %s %s" % (
            hisat2_build_path, self.reference, os.path.basename(self.reference))
        if self.debug:
            print(cmd_string)
        f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=True)

        if not f:
            print(o)
            print(e)
            raise ValueError("hisat2-build failed, see above info!")

        self.reference = self.work_dir + "/" + os.path.basename(self.reference)
        return self.reference

    def map(self, overwrite=False):
        # run hisat2-build
        self.build()

        # run hisat2
        sam_file = "%s/%s.sam" % (self.work_dir, self.job_id)
        log_file = "%s/%s.log" % (self.work_dir, self.job_id)
        sorted_bam_file = "%s/%s.sorted.bam" % (self.work_dir, self.job_id)

        if not overwrite and have_file(sorted_bam_file):
            self.mapping_ratio = self.get_mapping_rate_from_log(log_file)
            self.bam_file = sorted_bam_file

        if self.model == 'RNA':
            if self.fq2:
                cmd_string = "%s -p %d --dta -x %s -1 %s -2 %s -S %s" % (
                    hisat2_path, self.threads, self.reference, self.fq1, self.fq2, sam_file)
            else:
                cmd_string = "%s -p %d --dta -x %s -1 %s -S %s" % (
                    hisat2_path, self.threads, self.reference, self.fq1, sam_file)
        elif self.model == 'DNA':
            if self.fq2:
                cmd_string = "%s -p %d -x %s -1 %s -2 %s -S %s" % (
                    hisat2_path, self.threads, self.reference, self.fq1, self.fq2, sam_file)
            else:
                cmd_string = "%s -p %d -x %s -1 %s -S %s" % (
                    hisat2_path, self.threads, self.reference, self.fq1, sam_file)

        if self.debug:
            print(cmd_string)
        f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=True)
        with open(log_file, 'w') as f:
            f.write(e)
        if not f:
            print(o)
            print(e)
            raise ValueError("hisat2 failed, see above info!")

        # sam to bam
        cmd_string = "%s sort -@ %d -o %s %s" % (
            samtools_path, self.threads, sorted_bam_file, sam_file)
        if self.debug:
            print(cmd_string)
        f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=True)
        if not f:
            print(o)
            print(e)
            raise ValueError("samtools failed, see above info!")

        # clean
        if not self.debug:
            rmdir(sam_file)

        self.mapping_ratio = self.get_mapping_rate_from_log(log_file)
        self.bam_file = sorted_bam_file

    def get_mapping_rate_from_log(self, log_file):
        with open(log_file, 'r') as f:
            f_info = f.read()
            mapping_rate = float([i.split("%")[0] for i in f_info.split(
                '\n') if 'overall alignment rate' in i][0])
            mapping_rate = mapping_rate/100
        return mapping_rate


if __name__ == "__main__":
    # hisat2 example
    ref_fa = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/HiC_scaffold_1.fa'
    fq1 = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6_1.clean.fq.gz'
    fq2 = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6_2.clean.fq.gz'
    work_dir = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/test'

    test_hisat2_job = HISAT2_JOB('test', fq1, fq2, 'RNA', ref_fa, work_dir)
    test_hisat2_job.build()
    test_hisat2_job.map()
