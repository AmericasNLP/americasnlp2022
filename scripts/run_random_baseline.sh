#!/bin/bash

set -eou pipefail

# for l in Bribri Guarani Kotiria Quechua Waikhana; do
mkdir -p preds
for task in translate speech; do
    for l in Bribri Kotiria Quechua Waikhana; do
        echo $l
        python -u baselines/random_baseline.py \
            --train_meta Downloads/$l/train/meta.tsv \
            --test_meta Downloads/$l/dev/meta.tsv \
            --out_fn preds/${l}-dev-speech.txt \
            --task speech
    done
done