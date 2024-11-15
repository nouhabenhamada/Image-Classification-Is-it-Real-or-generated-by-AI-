import streamlit as st
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model
from PIL import Image

IMG_SIZE = 224

# Charger le modèle pré-entraîné
model = load_model('model_effnet_2.h5')

# Titre de l'application
st.title('Image prediction : Real or AI generated ?')

# Instructions pour l'utilisateur
st.write("Upload an image and the model will tell you if it is real or AI generated.")

# Interface pour télécharger une image
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Charger et afficher l'image téléchargée
    img = Image.open(uploaded_file)
    st.image(img, caption="Image uploaded", use_column_width=True)

    # Prétraiter l'image avant de la passer dans le modèle
    img = img.resize((IMG_SIZE, IMG_SIZE))  # Assurez-vous que IMG_SIZE est la taille d'entrée de votre modèle
    img_array = np.array(img)  # Convertir l'image en array
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension pour la batch
    img_array = preprocess_input(img_array)  # Prétraitement spécifique à EfficientNet

    # Prédire l'image avec le modèle
    prediction = model.predict(img_array)

    # Afficher le résultat
    if prediction[0][0] > prediction[0][1]:
        st.write("The image is **IA generated**.")
    else:
        st.write("The image is **real**.")

    # Afficher la probabilité de chaque classe
    st.write(f"The probability of image generated by AI : {prediction[0][0]*100:.2f}%")
    st.write(f"The probability of real image : {prediction[0][1]*100:.2f}%")