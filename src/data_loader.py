import pandas as pd

def load_datasets():
    try:
        df_corpus = pd.read_csv("data/cve_corpus.csv")
        df_epss = pd.read_csv("data/cve_cisa_epss_enriched_dataset.csv")
        return df_corpus, df_epss
    except FileNotFoundError:
        return None, None