import tensorflow as tf
import numpy as np
import cv2

# Load saved model
model = tf.keras.models.load_model("defect_model.h5")
print("✅ Model Loaded")

class_names = ['crazing', 'inclusion', 'patches',
               'pitted_surface', 'rolled-in_scale', 'scratches']

# Test image path
img_path = r"c:\Users\Shivansh\Pictures\Screenshots\Screenshot (19).png"

# Read image
img = cv2.imread(img_path)
img = cv2.resize(img, (224, 224))
img = np.expand_dims(img, axis=0)

# Prediction
prediction = model.predict(img)
class_index = np.argmax(prediction)
confidence = np.max(prediction)

print("Prediction:", class_names[class_index])
print("Confidence:", confidence)