import numpy as np
from tensorflow.keras.applications import VGG16 # type: ignore
from tensorflow.keras.applications.vgg16 import preprocess_input # type: ignore
from tensorflow.keras.preprocessing import image as keras_image # type: ignore
from tensorflow.keras.layers import GlobalAveragePooling2D # type: ignore
from tensorflow.keras.models import Model # type: ignore
from sklearn.metrics.pairwise import cosine_similarity

def create_model():
    # Load pre-trained VGG16 model
    base_model = VGG16(weights='imagenet', include_top=False)

    # Add global average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)

    # Final model
    model = Model(inputs=base_model.input, outputs=x)

    return model

def load_and_preprocess_image(image_path):
    img = keras_image.load_img(image_path, target_size=(225, 225))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def compare_images(image1_path, image2_path, model):
    # Load and preprocess images
    image1 = load_and_preprocess_image(image1_path)
    image2 = load_and_preprocess_image(image2_path)
    
    # Get features from images using the model
    features1 = model.predict(image1)
    features2 = model.predict(image2)
    
    # Compute cosine similarity between features
    similarity_score = cosine_similarity(features1, features2)[0][0]
    
    return similarity_score

# Example usage

image1_path = "dev_images/g7.png"
image2_path = "dev_images/g9.png"

# Create and compile the model
model = create_model()

# Then, use compare_images function to compare images
similarity_score = compare_images(image1_path, image2_path, model)
print("Similarity score:", similarity_score)
