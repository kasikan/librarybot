from gensim.models import Word2Vec
import gensim

#Model From Wikipedia corpus 
#model_filename = "word2vecTH_model.model"
#model = gensim.models.Word2Vec.load("wiki.th.text.model")
#model.vector_size
#print(model.wv.most_similar("[บริการ]"))

#Model from database 
#model = Word2Vec.load(model_filename)
#model.vector_size
#print(model.wv.most_similar("บริการ"))

#word_vector = model.wv["มหาวิทยาลัย"]
#print("Word Vector:", word_vector)



# Load the Word2Vec model from Wikipedia corpus
wiki_model_filename = "wiki.th.text.model"
wiki_model = gensim.models.Word2Vec.load(wiki_model_filename)

# Search for a word in the Wikipedia model
word_to_search = "มหาลัย"
if word_to_search in wiki_model.wv:
    print(wiki_model.wv.most_similar(word_to_search))
else:
    print(f"Word '{word_to_search}' not found in the Wikipedia model.")

# Load the Word2Vec model from database
database_model_filename = "word2vecTH_model.model"
database_model = Word2Vec.load(database_model_filename)

# Search for a word in the database model
if word_to_search in database_model.wv:
    print(database_model.wv.most_similar(word_to_search))
else:
    print(f"Word '{word_to_search}' not found in the database model.")
