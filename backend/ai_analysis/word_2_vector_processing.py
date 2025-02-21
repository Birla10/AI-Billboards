from gensim.models import Word2Vec
import gensim.downloader as api
import tempfile
import gensim

# wv = api.load("word2vec-google-news-300")

# # Convert KeyedVectors to a trainable Word2Vec model
# model = Word2Vec(vector_size=300, window=5, min_count=1, workers=4)
# model.build_vocab_from_freq(wv.key_to_index)  # Use existing vocab

# # Copy existing word vectors
# model.wv.vectors = wv.vectors
# model.wv.key_to_index = wv.key_to_index
# model.wv.index_to_key = wv.index_to_key

# word_list = [
#     "Telephone", "Silver", "Communication Device", "Cameras", "Gadget", "Nail",
#     "Thumb", "Lens", "Mobile device", "Smartphone", "Display device", "Technology",
#     "Portable communications device", "Hand", "Telephony", "Electronic device",
#     "Camera", "Finger"
# ]

# # Convert words into training sentences
# sentences = [[word.lower()] for word in word_list]

# # Add new words to vocabulary
# model.build_vocab(sentences, update=True)

# # Fine-tune the model on your custom words
# model.train(sentences, total_examples=len(sentences), epochs=10)

# # Save the updated model
# model.save("updated_word2vec.model")

new_model = gensim.models.Word2Vec.load("updated_word2vec.model")

vector_si = new_model.wv['Communication Device']

print(vector_si)