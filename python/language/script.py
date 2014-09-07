import nltk

nltk_packages = ['stopwords', 'maxent_treebank_pos_tagger', 'punkt', 'tagsets']
for p in nltk_packages:
    nltk.download(p)
