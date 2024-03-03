from toolbiox.lib.common.genome.genome_feature2 import GenomeFeature, ChrLoci


def try_int(value):
    try:
        return int(value)
    except ValueError:
        return value


def read_psl_file(input_psl_file):

    psl_gf_dict = {}

    with open(input_psl_file, "r") as f:
        q_num_dict = {}

        for line in f:
            line = line.strip()
            line_list = line.split("\t")
            info_flag = False
            try:
                [int(i) for i in line_list[:6]]
                info_flag = True
            except BaseException:
                info_flag = False

            if info_flag:
                match, mismatch, rep_match, n_count, q_gap_count, q_gap_bases, t_gap_count, t_gap_bases, strand, q_name, q_size, q_start, q_end, t_name, t_size, t_start, t_end, block_count, block_sizes, q_starts, t_starts = map(
                    try_int, line_list[:22])
                block_sizes = block_sizes.strip(",").split(",")
                block_sizes = list(map(try_int, block_sizes))
                q_starts = q_starts.strip(",").split(",")
                q_starts = list(map(try_int, q_starts))
                t_starts = t_starts.strip(",").split(",")
                t_starts = list(map(try_int, t_starts))

                q_num_dict.setdefault(q_name, 0)
                q_num_dict[q_name] += 1

                p_id = "%s.h%d" % (q_name, q_num_dict[q_name])
                t_loci = ChrLoci(
                    chr_id=t_name,
                    strand=strand,
                    start=t_start + 1,
                    end=t_end + 1)
                p_gf = GenomeFeature(
                    id=p_id,
                    type='blat_hit',
                    chr_loci=t_loci,
                    qualifiers={
                        "q_name": q_name,
                        "q_size": q_size,
                        "q_start": q_start,
                        "q_end": q_end,
                        "match": match,
                        "mismatch": mismatch,
                        "rep_match": rep_match,
                        "n_count": n_count,
                        "q_gap_count": q_gap_count,
                        "q_gap_bases": q_gap_bases,
                        "t_gap_count": t_gap_count,
                        "t_gap_bases": t_gap_bases,
                        "n_count": n_count,
                        "block_count": block_count},
                    sub_features=[])

                for i in range(block_count):
                    q_start = q_starts[i] + 1
                    t_start = t_starts[i] + 1
                    block_size = block_sizes[i]
                    q_end = q_start + block_size
                    t_end = t_start + block_size

                    t_loci = ChrLoci(
                        chr_id=t_name,
                        strand=strand,
                        start=t_start,
                        end=t_end)
                    m_gf = GenomeFeature(
                        id="%s.m%d" %
                        (p_id,
                         i +
                         1),
                        type='match',
                        chr_loci=t_loci,
                        qualifiers={
                            "q_name": q_name,
                            "q_size": q_size,
                            "q_start": q_start,
                            "q_end": q_end})

                    p_gf.sub_features.append(m_gf)

                psl_gf_dict[p_id] = p_gf

    return psl_gf_dict
