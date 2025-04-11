import pickle
import re 
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

with open('rf_model_final.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open('count_vectorizer_final.pkl', 'rb') as cv_file:
    loaded_cv = pickle.load(cv_file)

def predict_sentiments(reviews):

    ps = PorterStemmer()
    processed_reviews = []
    for review in reviews:
        rp = re.sub('[^a-zA-Z]', " ", review)
        rp = rp.lower()                      
        rp = rp.split()                       
        rp = [ps.stem(word) for word in rp if word not in set(stopwords.words('english'))]
        rp = " ".join(rp)
        processed_reviews.append(rp)
    

    test_vectors = loaded_cv.transform(processed_reviews).toarray()
    predicted_labels = loaded_model.predict(test_vectors)
    return predicted_labels.tolist()
