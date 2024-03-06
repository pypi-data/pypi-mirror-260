import scattertext as st
from unittest import TestCase

import pandas as pd
import spacy

from scattertextvl.features.arglex_offset_getter import get_arglex_offset_getter


class TestArglexOffsetGetter(TestCase):
    def sample_df(self):
        return pd.DataFrame([
            ['a', '''my understanding is that'''],
            ['a', '''but my understanding is that I'''],
            ['a', '''but I firmly believe this is a terrible movie.'''],
            ['b', '''What I would do would be important if I were in your shoes.'''],
            ['b', '''this is another document. my understanding is that
				blah blah blah''']
        ], columns=['Category', 'Text']).assign(
            Parse=lambda df: df.Text.apply(spacy.blank('en'))
        )

    def test_arglex(self):
        corpus = st.OffsetCorpusFactory(
            df=self.sample_df(),
            parsed_col='Parse',
            category_col='Category',
            feat_and_offset_getter=get_arglex_offset_getter()
        ).build()
        assert corpus.get_metadata_freq_df().to_dict(orient='records') == [{'a freq': 2, 'b freq': 1},
                                                                           {'a freq': 0, 'b freq': 1},
                                                                           {'a freq': 0, 'b freq': 1}]

        assert corpus.get_metadata() == ['assessments', 'inyourshoes', 'priority']
