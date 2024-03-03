from toolbiox.lib.common.os import mkdir, have_file, cmd_run
import os
from toolbiox.config import stringtie_path, gtf_to_alignment_gff3_perl_script


class STRINGTIE_JOB(object):
    """
    STRINGTIE_JOB

    sorted_bam = "rna.sorted.bam"
    s_id = "test"
    work_dir = "/home/work/stringtie_job"

    test_stringtie_job = STRINGTIE_JOB(s_id, sorted_bam, work_dir)
    test_stringtie_job.run()
    """

    def __init__(self, job_id=None, sorted_bam=None, work_dir=None, threads=8, debug=False):
        self.job_id = job_id
        self.sorted_bam = sorted_bam
        self.threads = threads
        self.work_dir = os.path.abspath(
            work_dir) if work_dir else os.path.abspath(os.path.curdir)
        self.debug = debug

        if self.work_dir:
            mkdir(self.work_dir, True)

    def run(self):
        stringtie_gff = os.path.join(self.work_dir, "stringtie.gff")

        if not have_file(stringtie_gff):
            stringtie_gtf = os.path.join(self.work_dir, "stringtie.gtf")
            cmd_string = "%s -o %s -p %d %s" % (
                stringtie_path, stringtie_gtf, self.threads, self.sorted_bam)
            f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=False)

            if not f:
                print(o)
                print(e)
                raise ValueError("stringtie failed, see above info!")

            cmd_string = "%s %s > %s" % (
                gtf_to_alignment_gff3_perl_script, stringtie_gtf, stringtie_gff)
            f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=False)

            if not f:
                print(o)
                print(e)
                raise ValueError(
                    "stringtie covert gtf to gff failed, see above info!")

        self.stringtie_gff = stringtie_gff


if __name__ == "__main__":
    # stringtie example
    sorted_bam = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/C8_H7GL5CCXY_L6.sorted.bam'
    work_dir = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/test'

    test_stringtie_job = STRINGTIE_JOB(
        'test', sorted_bam=sorted_bam, work_dir=work_dir)
    test_stringtie_job.run()
