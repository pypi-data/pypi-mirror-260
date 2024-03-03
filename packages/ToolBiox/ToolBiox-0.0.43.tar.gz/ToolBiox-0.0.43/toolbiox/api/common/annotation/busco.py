from toolbiox.lib.common.os import mkdir, rmdir, have_file, cmd_run, copy_file, get_file_name
from toolbiox.config import busco_path, busco_download_dir
import json
import os


class BUSCO_JOB(object):
    """
    BUSCO_JOB

    input_fasta_file = "genome.fasta"
    s_id = "test"
    mode = "genome" or "proteins"

    test_busco_job = BUSCO_JOB(s_id, input_fasta_file, mode="genome")
    test_busco_job.run()
    """

    def __init__(self, job_id=None, input_fasta_file=None, lineage_dataset="embryophyta_odb10", mode="genome", augustus_species="arabidopsis", num_threads=8, debug=False, work_dir=None):
        self.job_id = job_id
        self.input_fasta_file = os.path.abspath(input_fasta_file) if input_fasta_file else None
        self.lineage_dataset = lineage_dataset
        self.mode = mode
        self.augustus_species = augustus_species
        self.num_threads = num_threads
        self.debug = debug
        self.work_dir = os.path.abspath(
            work_dir) if work_dir else os.path.abspath(os.path.curdir)
        mkdir(self.work_dir, True)

    def run(self):
        self.busco_out_report = os.path.join(self.work_dir, 'busco_report.json')

        if not (have_file(self.busco_out_report)):
            busco_out = "%s_vs_%s" % (get_file_name(
                self.input_fasta_file), self.lineage_dataset)

            if self.mode == "genome":
                cmd_string = "%s --offline --download_path %s -c %d -m genome -i %s -o %s -l %s --augustus_species %s" % (
                    busco_path, busco_download_dir, self.num_threads, self.input_fasta_file, busco_out, self.lineage_dataset, self.augustus_species
                )
            elif self.mode == "proteins":
                cmd_string = "%s --offline --download_path %s -c %d -m proteins -i %s -o %s -l %s" % (
                    busco_path, busco_download_dir, self.num_threads, self.input_fasta_file, busco_out, self.lineage_dataset
                )

            f, o, e = cmd_run(cmd_string, cwd=self.work_dir, silence=True)
            if not f:
                print(o)
                print(e)
                raise ValueError("busco failed, see above info!")

            busco_report = os.path.join(self.work_dir,
                                        busco_out, 'short_summary.specific.%s.%s_vs_%s.json' % (self.lineage_dataset, get_file_name(self.input_fasta_file), self.lineage_dataset))

            copy_file(busco_report, self.busco_out_report)

            if not self.debug:
                rmdir(os.path.join(self.work_dir, busco_out))

        self.parse()

        return self.busco_report

    def parse(self, busco_out_report=None):
        if not hasattr(self, 'busco_out_report'):
            self.busco_out_report = busco_out_report

        with open(self.busco_out_report, "r") as f:
            busco_report_dict = json.load(f)

        self.busco_report = busco_report_dict

        return self.busco_report
            



if __name__ == "__main__":
    # busco example
    ref_fa = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/HiC_scaffold_1.fa'
    work_dir = '/lustre/home/xuyuxing/Database/Cuscuta/Cau/genomev2.0/anno/test'

    test_busco_job = BUSCO_JOB(
        'test', ref_fa, mode="genome", work_dir=work_dir)
    test_busco_job.run()
