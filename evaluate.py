from jiwer import wer, cer
import sacrebleu
import argparse


def calculate_score_report(sys, ref, score_only):

    chrf = sacrebleu.corpus_chrf(sys, ref)
    bleu = sacrebleu.corpus_bleu(sys, ref)

    prefix = 'BLEU = ' if score_only else ''

    print('#### Score Report ####')
    print(chrf)
    print('{}{}'.format(prefix, bleu.format(score_only=score_only)))


def calculate_asr_scores(sys, ref):
	
    word_error_rate = wer(ref, sys)
    character_error_rate = cer(ref,sys)
    
    print('--'*25)
    print("Word Error Rate: {}".format(word_error_rate))
    print('Character Error Rate: {}'.format(character_error_rate))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--system_output', '--sys', type=str, help='File with each line-by-line model outputs')
    parser.add_argument('--gold_reference', '--ref', type=str, help='File with corresponding line-by-line references')
    parser.add_argument('--detailed_output', action='store_const', const=True, default=False, help='(sacrebleu) Print additional BLEU information (default=False)')
    args = parser.parse_args()

    gold_lines = []
    no_translations = []
    with open(args.gold_reference, 'r') as f:
        for i, line in enumerate(f):

            if len(line.strip()) == 0:
                no_translations.append(i)
                continue

            gold_lines.append(line.strip())

    system_lines = []

    print(no_translations)

    with open(args.system_output, 'r') as f:
        for i,line in enumerate(f):

            if i in no_translations:
                continue

            system_lines.append(line.strip())


    assert len(system_lines) == len(gold_lines)

    print(len(system_lines))


    calculate_score_report(system_lines, [gold_lines], score_only=not args.detailed_output)

calculate_asr_scores(system_lines, gold_lines)
