import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# Load the model
model = tf.keras.models.load_model('emo.keras')

# Convert the Keras model to a TensorFlow Lite model with the necessary settings
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # Use TensorFlow Lite built-in ops
    tf.lite.OpsSet.SELECT_TF_OPS     # Use select TensorFlow ops
]
converter.experimental_lower_tensor_list_ops = False
converter.experimental_enable_resource_variables = True  # Enable resource variables
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('../models/emo.tflite', 'wb') as f:
    f.write(tflite_model)

# Test TFLite model
# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path='../models/emo.tflite')
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

message = "I feel like killing 1000 men and 1 monkey"

# Assuming you have saved tokenizer's configuration during training
# Here is an example of loading it (adjust path as necessary):
import json

with open('tokenizer_config.json', 'r') as f:
    tokenizer_config = json.load(f)
tokenizer = Tokenizer.from_json(tokenizer_config)

# Convert message to sequences and pad them
sequences = tokenizer.texts_to_sequences([message])
padded_sequences = pad_sequences(sequences, maxlen=79)

# Prepare the input data
input_data = np.array(padded_sequences, dtype=np.float32)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run the model
interpreter.invoke()

# Get the output
output_data = interpreter.get_tensor(output_details[0]['index'])
print('TFLite Prediction: ', output_data)
