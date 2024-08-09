from flask import Flask, request, render_template,jsonify
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from Utils.extract_entities import extract_entities
from Utils.filter_properties import filter_properties
from Utils.llama_response import fine_tuned_resp
from Utils.answer_composition import RealEstateChatbot


# # Load the trained model
# model = joblib.load('/home/jyotsna/Virtual_Real_Estate_Agent/model/test_model_file.pkl')

# # Load tokenizer and label encoder
# tokenizer = joblib.load('/home/jyotsna/Virtual_Real_Estate_Agent/model/tokenizer.pkl')
# le = joblib.load('/home/jyotsna/Virtual_Real_Estate_Agent/model/label_encoder.pkl')

# Define the maximum sequence length
max_sequence_length = 9  # Adjust according to your training

# Create a DataFrame
data = {
    "Bedroom": [2, 3, 4,5,3,2, 3, 4, 2, 3],
    "Bathroom": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
    "Price": [500000, 600000, 700000, 800000, 500000, 600000, 700000, 800000, 600000, 700000],
    "City": ["Toronto", "Toronto", "Toronto", "Kitchener","Toronto", "Kitchener", "Kitchener", "Toronto", "Kitchener","Kitchener"],
    "House Type": ["Condo", "House", "Apartment", "Townhouse", "Condo", "House", "Apartment", "Townhouse", "House", "Condo"],
    "House Size": ["150 sqft", "250 sqft", "350 sqft", "450 sqft", "150 sqft", "250 sqft", "350 sqft", "450 sqft", "250 sqft", "350 sqft"],
    "Water": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Electricity": ["Yes", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "Yes", "No"],
    "Financing": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Nearby": ["Hospital, School", "School, Grocery", "Grocery, Public Transport", "Public Transport, Recreational Park", "Hospital, School", "School, Grocery", "Grocery, Public Transport", "Public Transport, Recreational Park", "Hospital, School", "School, Grocery"],
    "Status": ["Available", "Sold", "Available", "Sold", "Available", "Sold", "Available", "Sold", "Available", "Sold"],
    "Swimming Pool": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Recent renovation/upgrades": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Year built": [2010, 2012, 2014, 2016, 2010, 2012, 2014, 2016, 2012, 2014],
    "Move-in-ready": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Heating": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Cooling": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Parking": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Repairs needed?": ["No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes"],
    "Basement": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
    "Visit availability date time": ["2024/12/10", "2024/12/11", "2024/12/12", "2024/12/13", "2024/12/10", "2024/12/11", "2024/12/12", "2024/12/13", "2024/12/11", "2024/12/12"],
    "Detailed/ summary of property": ["Spacious condo in downtown Toronto", "Beautiful house with a large backyard", "Modern apartment with city views", "Townhouse in a quiet neighborhood", "Cozy condo in Kitchener", "Large house with a garden", "Apartment near public transport", "Townhouse close to amenities", "House with modern finishes", "Condo with upgraded features"]
}

property_df = pd.DataFrame(data)



# Initialize the RealEstateChatbot
chatbot = RealEstateChatbot(filter_properties_func=filter_properties)


def predict(prompt):
    # Get the user input from the form
    user_input=prompt
    # # Preprocess the input
    # new_sequence = tokenizer.texts_to_sequences([user_input])
    # new_padded_sequence = pad_sequences(new_sequence, maxlen=max_sequence_length, padding='post')

    # #Predict the intent
    # prediction = model.predict(new_padded_sequence)
    # predicted_intent = np.argmax(prediction)
    
    # # Decode the predicted intent
    # predicted_intent_array = np.array([predicted_intent])
    # predicted_intent_label = le.inverse_transform(predicted_intent_array)[0]
    # print(predicted_intent_label,'predicted_intent_label')
    response=fine_tuned_resp(user_input)

    # # Extract entities from the user input
    # entities = extract_entities(user_input)
 
    # #Generate a response based on the predicted intent and extracted entities
    # response = chatbot.compose_answer(predicted_intent_label, entities, property_df)

    # Return the prediction to the user
    #return render_template('index.html', prediction=predicted_intent_label,response = response)
    # Return the prediction and response to the user as JSON
    return response

