import click
from typing import Dict, List, Tuple
import os

import wave
import contextlib
import random


PUNCT = set(["!", ".", "?"])


def read_meta(fn: str) -> Tuple[List[str], List[str]]:
    wavs, srcs, tgts = [], [], []
    path = os.path.dirname(fn)
    with open(fn, "r") as file:
        next(file)
        for i, line in enumerate(file):
            wav, _, src, tgt, *meta = line.rstrip().split("\t")
            wavs.append(wav)
            srcs.append(src)
            tgts.append(tgt)

    return path, wavs, srcs, tgts


def get_trigrams(data: List[str]) -> List[List[str]]:
    """Input is a List of sentence strings including white-space"""
    tris = []
    for sent in data:
        tris.append([sent[i:i+3] for i in range(len(sent)-2)])

    return tris


def get_trigram_counts(tri_sents: List[List[str]]) -> Dict[str, int]:
    """Count each trigram"""
    tri_cnts = {}

    for sent in tri_sents:
        for tri in sent:
            tri_cnts.setdefault(tri, 0) 
            tri_cnts[tri] += 1

    return tri_cnts


def compute_len_ratio(src: List[str], tgt: List[str]) -> float:
    """Get the ratio of src to tgt trigrams"""
    assert(len(src) == len(tgt))
    src_tot, tgt_tot = 0, 0
    for s1, s2 in zip(src, tgt):
        src_tot += len(s1)
        tgt_tot += len(s2)

    return tgt_tot / src_tot


def get_duration(fn: str) -> float:
    with contextlib.closing(wave.open(fn, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def compute_wav_len_ratio(data_path: str, wav_fns: List[str], tgt: List[str]) -> float:
    """For source, use duration of wav file"""
    dur_tot, tgt_tot = 0, 0
    for w, t in zip(wav_fns, tgt):
        w = os.path.join(data_path, w)
        dur_tot += get_duration(w)
        tgt_tot += len(t)

    return tgt_tot / dur_tot


@click.command()
@click.option("--train_meta", required=True, type=str)
@click.option("--test_meta", required=True, type=str)
@click.option("--out_fn", required=True, type=str)
@click.option("--task", type=click.Choice(['translate', 'speech'], case_sensitive=False), required=True)
def main(train_meta, test_meta, out_fn, task):
    data_path, wavs, src, tgt = read_meta(train_meta)
    tst_data_path, tst_wavs, tst_src, tst_tgt = read_meta(test_meta)
    ## Train
    # Make character trigrams
    src_trigrams = get_trigrams(src)
    tgt_trigrams = get_trigrams(tgt)
    # count target trigrams, for taking the top-N
    trigram_cnts = get_trigram_counts(tgt_trigrams)
    tgt_trigrams_flat = sorted(trigram_cnts, key=trigram_cnts.get, reverse=True)
    # Compute avg length ratio (src len / tgt len)
    if task == "translate":
        len_ratio = compute_len_ratio(src_trigrams, tgt_trigrams)
    elif task == "speech":
        len_ratio = compute_wav_len_ratio(data_path, wavs, tgt_trigrams)
    
    if task == "translation":
        tst_inputs = get_trigrams(tst_src)  
    elif task == "speech":
        tst_inputs = [os.path.join(tst_data_path, t) for t in tst_wavs]

    ## Write predictions
    with open(out_fn, "w") as out:
        for tst_sent in tst_inputs:
            # Choose the top-n most frequent trigrams where n is determined by the length ratio
            if task == "translation":
                tgt_len = len(tst_sent) * len_ratio
            elif task == "speech":
                tgt_len = get_duration(tst_sent) * len_ratio
            # reduce multiple white-spaces to one character
            tgt_len = int(tgt_len)
            translation = ''.join(tgt_trigrams_flat[:tgt_len]).split()
            # randomize order of trigrams
            random.shuffle(translation)
            # Lowercase non-word initial words
            [t.lower() for t in translation[1:]]
            # Copy end punct from src sentence
            if translation and translation[-1][-1] not in PUNCT and tst_sent[-1] in PUNCT:
                translation[-1] += tst_sent[-1]

            out.write(" ".join(translation))
            out.write("\n")


if __name__=='__main__':
    main()