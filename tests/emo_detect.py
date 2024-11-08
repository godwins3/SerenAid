
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
import os

from transformers import pipeline

def get_emotion(message):
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, 'emo.keras')
    loaded_model = load_model(model_path)

    tokenizer = Tokenizer(num_words=50000)
    sequences = tokenizer.texts_to_sequences([message])

    # Pad the sequences to ensure consistent input size
    padded_sequences = pad_sequences(sequences, maxlen=79)

    # Make a prediction
    prediction = loaded_model.predict(padded_sequences)
    class_labels = ['Sadness', 'Joy', 'Love', 'Anger', 'Fear', 'Surprise']
    print(prediction)
    # Get the index of the highest probability
    predicted_index = prediction.argmax()

    # Get the corresponding class label
    predicted_label = class_labels[predicted_index]
    
    return predicted_label



def detect_emotion(message):
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    results = classifier(message)
    highest_score = 0
    highest_label = ""

    for result in results[0]:
        if result['score'] > highest_score:
            highest_score = result['score']
            highest_label = result['label']

    return highest_label



if __name__ =="__main__":
    # test custom model
    user_message = "I love you"
    emotion = get_emotion(user_message)
    print(emotion)

    # test huggingface model 
    emotion = detect_emotion(user_message)
    print(emotion)