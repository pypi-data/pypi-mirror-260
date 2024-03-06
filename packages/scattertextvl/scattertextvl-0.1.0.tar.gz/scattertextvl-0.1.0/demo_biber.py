import scattertext as st
import scattertextvl as stvl
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')

convention_df = st.SampleCorpora.ConventionData2012.get_data().assign(
    Party=lambda df: df.party.apply(lambda x: {'democrat': 'Dem', 'republican': 'GOP'}[x]),
    Parse=lambda df: df.text.progress_apply(nlp)
)

biber_corpus = st.OffsetCorpusFactory(
    convention_df,
    category_col='Party',
    parsed_col='Parse',
    feat_and_offset_getter=stvl.BiberOffsetGetter()
).build(show_progress=True)

score_df = st.HedgesG(
    biber_corpus
).use_metadata().set_categories(
    category_name='Dem'
).get_score_df(
)

biber_stat_df = score_df.rename(columns={'hedges_g': 'HedgesG', 'hedges_g_p': 'HedgesGPval'}).assign(
    Frequency=lambda df: df.count1 + df.count2,
    X=lambda df: df.Frequency,
    Y=lambda df: df.HedgesG,
    Xpos=lambda df: st.Scalers.dense_rank(df.X),
    Ypos=lambda df: st.Scalers.scale_center_zero_abs(df.Y),
    ColorScore=lambda df: df.Ypos,
)

plot_df = pd.merge(
    biber_stat_df,
    stvl.get_biber_feature_df(),
    left_index=True,
    right_index=True
).reset_index().rename(columns={'index': 'term'}).set_index('term')

html = st.dataframe_scattertext(
    biber_corpus,
    plot_df=plot_df,
    category='Dem',
    category_name='Democratic',
    not_category_name='Republican',
    width_in_pixels=1000,
    suppress_text_column='Display',
    metadata=lambda c: c.get_df()['speaker'],
    use_non_text_features=True,
    ignore_categories=False,
    use_offsets=True,
    unified_context=False,
    horizontal_line_y_position=0,
    color_score_column='ColorScore',
    left_list_column='ColorScore',
    y_label='Hedges G',
    x_label='Frequency Ranks',
    y_axis_labels=[f'More Dem: g={plot_df.HedgesG.max():.3f}',
                   '0',
                   f'More Rep: g={-plot_df.HedgesG.max():.3f}'],
    tooltip_columns=['Frequency', 'HedgesG'],
    term_description_columns=['Feature', 'Category', 'Examples',
                              'hedges_g', 'hedges_g_p', 'Frequency', 'Operationalization'],
    term_description_column_names={'hedges_g': "Hedge's g",
                                   'hedges_g_p': "Hedge's g p-value"},
    header_names={'upper': 'Top Democratic', 'lower': 'Top Republican'},
    term_word_in_term_description='Biber Tag',
)

fn = 'demo_biber.html'
with open(fn, 'w') as of:
    of.write(html)
print(f'run open ./{fn}')

biber_category_corpus = biber_corpus.rename_metadata(
    stvl.get_biber_feature_df().reset_index()[['index','Category']].values
)

biber_stat_df = st.CohensD(biber_category_corpus).use_metadata().set_categories(
    'Positive', ['Negative']
).get_score_df(
).assign(
    Frequency = lambda df: df.count1+df.count2,
    X=lambda df: df.Frequency,
    Y=lambda df: df.hedges_g,
    Xpos=lambda df: st.Scalers.dense_rank(df.X),
    Ypos=lambda df: st.Scalers.scale_center_zero_abs(df.Y),
    ColorScore=lambda df: df.Ypos,
    Features = stvl.get_biber_feature_df().groupby('Category').apply(
        lambda gdf: ', '.join(gdf.Feature)
    )
)


plot_df = pd.merge(
    biber_stat_df,
    stvl.get_biber_feature_df(),
    left_index=True,
    right_index=True
).reset_index().rename(columns={'index': 'term'}).set_index('term')



html = st.dataframe_scattertext(
    biber_category_corpus,
    plot_df=plot_df,
    category='Dem',
    category_name='Democratic',
    not_category_name='Republican',
    width_in_pixels=1000,
    suppress_text_column='Display',
    metadata=lambda c: c.get_df()['speaker'],
    use_non_text_features=True,
    ignore_categories=False,
    use_offsets=True,
    unified_context=False,
    horizontal_line_y_position=0,
    color_score_column='ColorScore',
    left_list_column='ColorScore',
    y_label='Hedges G',
    x_label='Frequency Ranks',
    y_axis_labels=[f'More Dem: g={plot_df.HedgesG.max():.3f}',
                   '0',
                   f'More Rep: g={-plot_df.HedgesG.max():.3f}'],
    tooltip_columns=['Frequency', 'HedgesG'],
    term_description_columns=['Feature', 'Examples',
                              'hedges_g', 'hedges_g_p', 'Frequency', 'Operationalization'],
    term_description_column_names={'hedges_g': "Hedge's g",
                                   'hedges_g_p': "Hedge's g p-value"},
    header_names={'upper': 'Top Democratic', 'lower': 'Top Republican'},
    term_word_in_term_description='Biber Category',
)

fn = '.demo_biber_category.html'
with open(fn, 'w') as of:
    of.write(html)
print(f'run open ./{fn}')
