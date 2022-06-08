#!/bin/bash

set -eou pipefail

# for l in Bribri Guarani Kotiria Quechua Waikhana; do
for l in Bribri Kotiria Quechua Waikhana; do
    echo $l
    python -u baseline.py \
        --train_meta data/$l/train/meta.tsv \
        --test_meta data/$l/dev/meta.tsv \
        --out_fn preds/${l}-dev-speech.txt \
        --task speech
done