import pandas as pd
from pythainlp import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

document = [
    "มีแอปเปิ้ลอยู่ทั้งหมดสิบลูก",
    "ฉันชอบผลไม้เป็นอย่างมาก",
    "แอปเปิ้ลมีสีแดง"
]

tokens_doc = []
for doc in document:
    tokens = word_tokenize(doc)
    tokens_doc.extend(tokens)

tf_transformer = TfidfVectorizer(smooth_idf=True, use_idf=True, tokenizer=word_tokenize)
matrix = tf_transformer.fit_transform(document)

print(type(matrix), matrix.shape)

tf_doc = matrix.todense()

print(tf_doc)

word_set = tf_transformer.get_feature_names_out()
print(word_set)

df_if = pd.DataFrame(tf_doc, columns=word_set)
print(df_if)