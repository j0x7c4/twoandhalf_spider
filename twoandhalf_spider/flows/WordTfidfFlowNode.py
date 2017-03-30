# -*- coding: utf-8 -*-
from twoandhalf_spider.flows.BaseFlowNode import BaseFlowNode
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


class WordTfidfFlowNode(BaseFlowNode):
    def __init__(self, db_conf, src, dst):
        super(WordTfidfFlowNode, self).__init__(db_conf=db_conf, src=src, dst=dst)
        self.src_fields = src[0]['fields']
        self.content_index = src[0]['content_index']
        self.id_index = src[0]['id_index']
        self.content_field = self.src_fields[self.content_index]
        self.id_field = self.src_fields[self.id_index]
        self.corpus = []
        self.stemmer = PorterStemmer()
        self.tfidf = None
        self.tfs = None
        self.word_index = None
        self.doc_index = None
        self.word_df = None

    def stem_tokens(self, tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens)
        return stems

    def calc_feature(self):
        self.doc_index = []
        for (i, record) in self.read():
            doc_id = record[self.id_field]
            text = record[self.content_field]
            lowers = text.lower()
            self.corpus.append(lowers)
            self.doc_index.append(doc_id)
        # this can take some time
        self.tfidf = TfidfVectorizer(tokenizer=self.tokenize)
        self.tfs = self.tfidf.fit_transform(self.corpus)
        self.word_index = self.tfidf.get_feature_names()
        self.word_df = [0 for i in range(len(self.word_index))]
        cx = self.tfs.tocoo()
        for (row, col, value) in zip(cx.row, cx.col, cx.data):
            self.word_df[col] += 1

    def action(self):
        self.calc_feature()
        word_index = [{"id": i, "word": word} for (i, word) in enumerate(self.word_index)]
        cx = self.tfs.tocoo()
        word_tfidf = [{"doc_id": self.doc_index[row], "word": self.word_index[col], "tfidf":value}
                      for (row, col, value) in zip(cx.row, cx.col, cx.data)]
        word_df = [{"id":i, "word": self.word_index[i], "df": self.word_df[i]} for i in range(len(self.word_df))]
        self.save([word_tfidf, word_df, word_index])

if __name__ == "__main__":
    src = [{
        "table": "weibo_post_seg",
        "fields": ["id", "body"],
        "content_index": 1,
        "id_index": 0
    }]

    dst = [{
        "table": "weibo_word_tfidf",
        "fields": ["doc_id", "word", "tfidf"],
        "schema": [
            ("doc_id", "varchar(45)"),
            ("word", "varchar(255)"),
            ("tfidf", "double")
        ]
    }, {
        "table": "weibo_word_df",
        "fields": ["id", "word", "df"],
        "schema": [
            ("id", "int"),
            ("word", "varchar(255)"),
            ("df", "double")
        ]
    },
        {
        "table": "weibo_word_index",
        "fields": ["id", "word"],
        "schema": [
            ("id", "int"),
            ("word", "varchar(255)")
        ]
    }
    ]
    from twoandhalf_spider.conf.mysql import host, user, passwd, db
    db_conf = {
        'host': host,
        'user': user,
        'passwd': passwd,
        'db': db
    }
    word_count = WordTfidfFlowNode(db_conf=db_conf, src=src, dst=dst)
    word_count.action()

