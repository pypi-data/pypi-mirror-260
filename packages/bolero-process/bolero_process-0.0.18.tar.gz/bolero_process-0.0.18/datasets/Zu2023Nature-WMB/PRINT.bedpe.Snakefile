import pysam
from tqdm import tqdm


samples = ['CEMBA190711_8E']
barcode_tag_name = 'CB'


def add_cb_cemba_atac(input_path):
    output_path = str(input_path)[:-3] + "add_cb.bam"
    with pysam.AlignmentFile(input_path) as bam:
        with pysam.AlignmentFile(output_path, mode='wb', template=bam) as out_bam:
            for read in tqdm(bam):
                bc = read.qname.split(":")[0]
                read.set_tag("CB", bc)
                out_bam.write(read)


rule all:
    input:
        bedpe = expand("bedpe/{sample}.bedpe.gz", sample=samples)


rule gsutil:
    output:
        temp("/tmp/{sample}/raw.bam")
    threads:
        8
    shell:
        "gsutil -m cp gs://hms-hanqing-temp/cemba_atac/raw_bams/{wildcards.sample}.bam {output} "


rule sort:
    input:
        "/tmp/{sample}/raw.bam"
    output:
        temp("/tmp/{sample}/sort.bam")
    params:
        tmp="/tmp/{sample}/sort"
    priority: 50
    threads:
        4
    shell:
        "samtools sort -n -m 3G -T {params.tmp} -@ {threads} -O BAM -o {output} {input}"


rule add_cb:
    input:
        "/tmp/{sample}/sort.bam"
    output:
        temp("/tmp/{sample}/sort.add_cb.bam")
    run:
        add_cb_cemba_atac(str(input))


rule dedup:
    input:
        "/tmp/{sample}/sort.add_cb.bam"
    output:
        temp("/tmp/{sample}/dedup.bam")
    params:
        tmp="/tmp/{sample}/"
    threads:
        2
    shell:
        "picard MarkDuplicates "
        "--INPUT {input} "
        "--TMP_DIR {params.tmp} "
        "--METRICS_FILE {input}.qc "
        "--ASSUME_SORT_ORDER queryname "
        "--VALIDATION_STRINGENCY LENIENT "
        "--OUTPUT {output} "
        "--BARCODE_TAG {barcode_tag_name} "
        "--REMOVE_DUPLICATES TRUE"


rule filter:
    input:
        "/tmp/{sample}/dedup.bam"
    output:
        "bam/{sample}.dedup.qc.bam"
    threads:
        4
    priority: 100
    shell:
        "samtools view -@ {threads} -q 30 -f 2 -F 1804 -O BAM -o {output} {input}"


rule bedpe:
    input:
        "bam/{sample}.dedup.qc.bam"
    output:
        "bedpe/{sample}.bedpe.gz"
    shell:
        "bedtools bamtobed -i {input} -bedpe | gzip -c > {output}"
