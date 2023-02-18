#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate base && jina flow --use flow.yml