# Zecure Backend: Django Server and Neural Network Model

Django backend and machine learning model for Zecure, a final-year team project that detects network attacks. The mobile app part of the project is in the zecure repository.

## What it does
- Trains a neural network on the NSL-KDD dataset to classify network traffic as normal or as a specific attack type
- Captures live network packets with Scapy, extracts features from each one, and predicts whether it is normal or an attack
- Provides a Django website with separate admin and expert sections
- Stores users, complaints, replies, logs and requests in a MySQL database

## The model
- A dense neural network (DNN) built with Keras: two hidden layers (64 and 32 units, ReLU) and a softmax output
- 7 input features: protocol type, service, flag, source bytes, destination bytes, TTL and packet length
- Trained for 10 epochs on 80% of the data, with 20% held out for validation
- Categorical features are label-encoded and numeric features are standardized; the saved encoder and scaler are in `MyApp`

## Project structure
- `MyApp/finaltrainingcode.py`: data preparation and model training
- `MyApp/finalpredictioncode.py`: loads the trained model and predicts on new traffic
- `MyApp/ids_dnn_model_7features.h5`, `scaler.pkl`, `label_encoder.pkl`: the trained model and its helpers
- `MyApp/views.py`, `urls.py`, `models.py`: website logic and database models
- `templates/`: HTML pages for login, the admin section and the expert section

## Features
- Login and password recovery
- Admin: add and edit experts, view users, view complaints and send replies, view app reviews
- Expert: add, edit and view videos, view requests (approved and rejected), view profile, change password

## Tech used
- Python, Django, Scapy
- TensorFlow/Keras, scikit-learn, pandas, NumPy
- MySQL

## Running it locally
1. Install the dependencies: Django, mysql-connector-python, mysqlclient, TensorFlow, scikit-learn, pandas, NumPy and joblib.On 
   Windows, packet capture also needs Npcap, and the script must run with administrator rights
2. Create a MySQL database named `IDPS`.
3. Set these environment variables: `DB_USER`, `DB_PASSWORD`, `DB_NAME` (default `IDPS`), `DB_HOST` (default `localhost`) and 
   `DJANGO_SECRET_KEY`.
4. Download the NSL-KDD file `KDDTrain+.csv` and place it in `MyApp` if you want to retrain the model.
5. Run `python manage.py migrate`, then `python manage.py runserver`.

## Not included
- Front-end theme files (Bootstrap, carousel and icon libraries, stock images) and uploaded media, which are third-party or test files
- The NSL-KDD dataset, which is publicly available

## Note
This was a team project developed during my BSc Computer Science degree at MAMO College, University of Calicut. Database credentials are read from environment variables, not stored in the code.
