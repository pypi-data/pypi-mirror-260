# LeafCutterITI

By Xingpei Zhang

### Citation:
**Alamancos, G. P., Pagès, A., Trincado, J. L., Bellora, N., & Eyras, E. (2015). Leveraging transcript quantification for fast computation of alternative splicing profiles. RNA , 21(9), 1521–1531. https://doi.org/10.1261/rna.051557.115**

**Li, Y. I., Knowles, D. A., Humphrey, J., Barbeira, A. N., Dickinson, S. P., Im, H. K., & Pritchard, J. K. (2018). Annotation-free quantification of RNA splicing using LeafCutter. Nature Genetics, 50(1), 151–158. https://doi.org/10.1038/s41588-017-0004-9**

**Patro, R., Duggal, G., Love, M. I., Irizarry, R. A., & Kingsford, C. (2017). Salmon provides fast and bias-aware quantification of transcript expression. Nature Methods, 14(4), 417–419. https://doi.org/10.1038/nmeth.4197**


### Requirements (versions used for development)

- python (v3.10.11)

#### Python Dependencies
- numpy 
- pandas
- pyranges

#### Additional Requirement for isoform quantification

- salmon (v1.10.0)

#### Other dependencies for Leafcutter as listed in https://github.com/davidaknowles/leafcutter/tree/master, especially for Leafcutter_ds

## LeafcutterITI
A modified version of Leafcutter that detects and analyzes alternative splicing events by quantifying excised introns by utilizing isoform abundance and transcriptome annotation. 

![LeafcutterITI_Workflow](figures/LeafcutterITI_workflow.png)



There are two parts of LeafcutterITI: 
- LeafcutterITI_map_gen
- LeafcutterITI_clustering

### LeafcutterITI_map_gen
```
usage: python leafcutterITI_map_gen.py [-a/--annot] [--annot_source] [-o/--outprefix] 
                     [--maxintronlen] [--minintronlen] [-v/--virtual_intron]

Mandatory parameters:

-a, --annot     The transcriptome annotation gtf file for LeafcutterITI_map_gen to run with 

Optional Parameters:

--annot_source          The annotation source for the annotation, currently support Gencode and Stringtie 
                        (default: gencode)

-o, --outprefix         The prefix for output files (default: Leafcutter_)

--maxintronlen          The maximum allowed intron length for introns (default: 5,000,000)

--minintronlen          The minimum allowed intron length for introns (default: 50)

--quality_control       Whether to remove pseudogene, and decay transcript (default: True)

-v, --virtual_intron    Whether to compute virtual intron that can be used to capture
                        AFE and ALE usage, a testing feature (default: None)

```

### LeafcutterITI_clustering

```
usage: python leafcutterITI_clustering.py [--map] [--count_files] [--connect_file] [-a/--annot]
                    [--cluster_def] [-o/--outprefix] [-n/--normalization] [--samplecutoff]
                    [--introncutoff] [-m/--minclucounts] [-r/--mincluratio]

Mandatory parameters:
--map             The isoforms to introns map generated from leafcutterITI_map_gen  

--count_files     A txt file that contain the sample names 

--connect_file    The intron-exon connectivity file generated from leafcutterITI_map_gen 

-a, --annot       The transcriptome annotation gtf file 


Optional Parameters:
--cluster_def           The definition used for cluster refinement, three def available, 1: overlap, 2: overlap+share_intron_splice_site, 
                        3: overlap+share_intron_splice_site+shared_exon_splice_site (default: 3)

-o, --outprefix         The prefix for output files (default: Leafcutter_)

-n, --normalization     whether to performance normalization, if not use TPM directly (default: True)

--preprocessed          whether the files provided are already normalized, mainly for rerunning the pipeline and don't 
                        perform normalization again (default: False) 

--samplecutoff          minimum Normalized count/TPM for an intron in a sample to count as exist (default: 0)

--introncutoff          minimum Normalized count/TPM for an intron to count as exist(default 5)

--m, --minclucounts     minimum Normalized count/TPM to support a cluster (default: 30)

-r, --mincluratio       minimum fraction of reads in a cluster that supports an intron (default 0.01)

```



## Detailed Tutorial to run the LeafcutterITI

In this tutorial, we walk through all the steps to run the LeafcutterITI pipeline. For each step, we discuss the possible parameters that can be changed, how to do so and the considerations involved in each of the parameters. Finally, we show example inputs and outputs of each step (with column explanations) so the user knows what to expect and can make custom files as needed.


### Step 0: Transcriptome annotation download or generation and Salmon isoform quantification

Example human transcriptome annotation can be downloaded from https://www.gencodegenes.org/human/


### Step 1: Isoform to intron map generation

In this step, LeafcutterITI_map_gen will be used to generate a map that contains information about which isoform is generated by splicing which introns. The map will also contain information about which exon is in which isoform. This step only needs to run once for each unique transcriptome annotation gtf file. 

Sample run:
```
python LeafcutterITI_map_gen -a gencode.v45.annotation.gtf --annot_source gencode -o sample_run_ --maxintronlen 5000000 --minintronlen 50 -v False          
```


Depending on the setting, two or four files will be generated.
- {out_prefix}isoform_intron_map.tsv
- {out_prefix}intron_exon_connectivity.tsv
- {out_prefix}isoform_intron_map_with_virtual.tsv
- {out_prefix}intron_exon_connectivity_with_virtual.tsv

where with_virtual mean virtual intron was used to capture AFE and ALE (testing feature). Both transcript_intron_map.tsv and intron_exon_connectivity.tsv

if annotation_source='gencode', an additional file will be generated to give out information about the possible isoform type that can be generated by splicing out each intron
- {out_prefix}intron_source_map.tsv

This is a testing feature that haven't been tested yet
  
A record file that contain the parameters will also be generated

### Step 2: Salmon isoform quantification

For usage of Salmon please refer https://salmon.readthedocs.io/en/latest/salmon.html

In the rest of the tutorial, we assume RNA-seq data were aligned to the transcriptome using Salmon. Then we will obtain file ending with .sf that described the isoform quantification results.


### Step 3: LeafcutterITI clustering

For this step, we will need the file generated from step 1, the file path and the name for the isoform quantification files generated by Salmon, and the transcriptome annotation


Sample run:
```
python LeafcutterITI_clustering --map transcript_intron_map.tsv --count_files quantification_files.txt --connect_file intron_exon_connectivity.tsv -a gencode.v45.annotation.gtf --cluster_def 3 \
                                --normalization True -o sample_run_ --minclucounts 30 --mincluratio 0.01
```


Two main output files will be obtained:
- {out_prefix}refined_cluster
- {output_prefix}ratio_count

sample {out_prefix}refined_cluster
```
sample1.sf sample2.sf sample3.sf sample4.sf sample5.sf sample6.sf
chr1:17055:17233:clu_1 21.1 13 18 20 17 12 
chr1:17055:17606:clu_1 4 11.4 12 7 2 0 5 
chr1:17368:17606:clu_1 127 132 128 55 93 90 68 
chr1:668593:668687:clu_2 3 11.3 1 3 4 4 8 
chr1:668593:672093:clu_2 11 16 23 2.5 3 20 9
```

These two files are equivalent to Leafcutter clustering numers.counts.gz and counts.gz. It is worth noticing that the normalized count or TPM is not necessarily an integer, but the normalized count will exhibit a count-like property.




### Step 4:
The output from step 3 is equivalent to results from leafcutter clustering, and the results are compatible with downstream analysis for Leafcutter, such as Leafcutter_ds and Leafviz. 
Further information and downstream analysis please refer to https://davidaknowles.github.io/leafcutter/index.html















