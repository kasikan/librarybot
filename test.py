import gensim

model = gensim.models.Word2Vec.load("wiki.th.text.model")
model.vector_size
# print(model.wv.most_similar("แมว"))

# word_vector = model.wv["แมว"]
# print("Word Vector:", word_vector)