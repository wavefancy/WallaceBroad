#change the master port when have a test run.
spark-submit --jars /medpop/esp2/wallace/program/hail/hail/gcp/hail-0.1-1214727c640f-Spark-2.1.0.jar --py-files /medpop/esp2/wallace/program/hail/hail/gcp/hail-0.1-1214727c640f.zip --master spark://uger-c010.broadinstitute.org:7077 vcfSamplesQC.py -i data/test.vcf.gz -o data/qc.out.test
