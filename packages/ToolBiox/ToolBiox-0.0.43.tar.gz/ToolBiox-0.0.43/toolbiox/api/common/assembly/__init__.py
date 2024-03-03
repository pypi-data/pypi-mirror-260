import os

def parse_fastq_arg(fq1, fq2=None):
    if fq1 is None:
        return None, None, None

    if isinstance(fq1, list):
        s_fq1 = fq1[0]
        fq1 = [os.path.abspath(i) for i in fq1]
        fq1 = ",".join(fq1)
    else:
        fq1 = os.path.abspath(fq1)
        s_fq1 = fq1

    if fq2:
        if isinstance(fq2, list):
            fq2 = [os.path.abspath(i) for i in fq2]
            fq2 = ",".join(fq2)
        else:
            fq2 = os.path.abspath(fq2)

    c_job_id = os.path.splitext(os.path.basename(s_fq1))[0]

    return fq1, fq2, c_job_id