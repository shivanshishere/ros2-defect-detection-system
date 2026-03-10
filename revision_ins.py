import os
import tensorflow as tf

# =========================
# DATASET PATH
# =========================
TRAIN_PATH = "train/images"
VAL_PATH = "validation/images"

# Check paths
if not os.path.exists(TRAIN_PATH):
    print("❌ Train path not found")
else:
    print("✅ Train path found")

if not os.path.exists(VAL_PATH):
    print("❌ Validation path not found")
else:
    print("✅ Validation path found")


# =========================
# LOAD DATASET
# =========================
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_PATH,
    image_size=(224, 224),
    batch_size=32
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    VAL_PATH,
    image_size=(224, 224),
    batch_size=32
)

print("\n📂 Classes detected:")
print(train_ds.class_names)
print("\n✅ Dataset Loaded Successfully")


#dataset load in sequence

AUTOTUNE = tf.data.AUTOTUNE

train_ds= train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds=val_ds.cache().prefetch(buffer_size=AUTOTUNE)  


#mere pass ka data set h isliye hum transferlearing ka use kr rhe h 
#mobilenetv2 = ye cnn la light weight architecture hota h 
#include top = false rkhte hmeans last layer ko hi update krna h aage ki layer ko touch nhi krna q ki wo pretrained h
#weight = imagenet q ki tf ko batate hh ki model already trained h image net pr weight weight = none rakhemhe to bhut time lage  weight ko bhut data bhi chahiye


base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False # weight ko update nhi krna h 

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),  # 👈 IMPORTANT
    tf.keras.layers.Lambda(
        tf.keras.applications.mobilenet_v2.preprocess_input
    ),
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(6, activation='softmax')
])
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
) 

model.save("defect_model.h5")
print("✅ Model Saved Successfully")
