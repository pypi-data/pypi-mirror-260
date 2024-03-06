import logging
import warnings

import spacy

from scattertext.features.featoffsets.feat_and_offset_getter import FeatAndOffsetGetter
from scattertextvl.features.biber.biber_sentence_processor import process_sentence, process_sentence_extended



class BiberOffsetGetter(FeatAndOffsetGetter):
    def __init__(self):
        warnings.warn(
            "In addition to citing Scattertext, cite as:\n"
            "Elen Le Foll and Muhammad Shakir. MFTE Python 1.0. 2023. "
            "https://github.com/mshakirDr/MFTE"
        )

    def get_term_offsets(self, doc):
        return []

    def get_metadata_offsets(self, doc: spacy.tokens.doc.Doc) -> list:
        if len(doc) and all(tok.tag_ == '' for tok in doc):
            logging.warning("All POS tags in `doc` are ''. Check to make sure you properly "
                            "initialized the tagger.")
        offset_tokens = {}
        for sent in doc.sents:
            words = [w.lower_ + '_' + w.tag_ for w in sent]
            tagged_words = process_sentence(words + [' '] * 20, True)
            tags = process_sentence_extended(tagged_words)[:-20]
            for word, tag in zip(sent, tags):
                start = word.idx
                end = word.idx + len(word.orth_)
                for single_tag in tag[len(word.orth_) + 1:].split():
                    token_stats = offset_tokens.setdefault(single_tag, [0, []])
                    token_stats[0] += 1
                    token_stats[1].append((start, end))
        return list(offset_tokens.items())
