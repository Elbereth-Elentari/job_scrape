#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh
conda activate job_scrape

cd /media/arvala/449bba29-d169-4b35-a2f4-ff9f2d504363/arvala/Documents/job_scrape
python3.12 main.py > scraping_log.txt 2>&1

conda deactivate
