from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def produce_Doc2Vec_Model(df, vector_size, window, min_count, dm, epochs):
    corpus = df["review_clean"].tolist()

    # Prepare tagged documents (documents with unique IDs)
    tagged_data = [TaggedDocument(words=doc, tags=[str(i)]) for i, doc in enumerate(corpus)]

    # Create and train the Doc2Vec model
    model = Doc2Vec(vector_size=vector_size, window=window, min_count=min_count, dm=dm, epochs=epochs)  # Adjust parameters as needed
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.save("models\doc2vec.model")
    return model

def load_Doc2Vec():
    return Doc2Vec.load("models\doc2vec.model")