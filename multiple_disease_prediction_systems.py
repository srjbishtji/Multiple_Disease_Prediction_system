# pip install 
# import library
import os
import pickle
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from captcha.image import ImageCaptcha
import random, string


# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Constants
length_captcha = 6
width = 200
height = 150

# Function to generate captcha
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))

# Function to control the captcha
def captcha_control():
    # Control if the captcha is correct
    if 'controllo' not in st.session_state or not st.session_state['controllo']:
        
        # Initialize controllo state
        st.session_state['controllo'] = False
        
        # Create columns for layout
        col1, col2 = st.columns([1, 3])
        
        # Generate and store captcha text
        if 'Captcha' not in st.session_state:
            st.session_state['Captcha'] = generate_captcha()
        
        # Display captcha image
        image = ImageCaptcha(width=width, height=height)
        data = image.generate(st.session_state['Captcha'])
        col1.image(data)
        
        # Captcha text input
        capta2_text = col2.text_area('Enter captcha text', height=30)
        
        return capta2_text

# Function for login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Integrate captcha control function
    capta2_text = captcha_control()
    
    # Check if captcha is verified and proceed with login
    if st.button("Login"):
        # Perform captcha verification
        if capta2_text is not None:
            capta2_text = capta2_text.replace(" ", "").lower().strip()
            
            if st.session_state['Captcha'].lower() == capta2_text:
                # Perform authentication
                if authenticate(username, password):
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                else:
                    st.error("Invalid username or password")
            else:
                st.error("🚨 Il codice captcha è errato, riprova")
                del st.session_state['Captcha']
                del st.session_state['controllo']
                st.experimental_rerun()
        else:
            st.error("Please enter the captcha text")

# Dummy authentication function (replace with your logic)
def authenticate(username, password):
    # Implement your authentication logic here
    # For demonstration purposes, using hardcoded username and password
    return username == "user" and password == "password"

# Call the login function
if not st.session_state.logged_in:
    login()




# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# loading the saved models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# Sidebar content
with st.sidebar:
    st.sidebar.title("Navigation")

    # If user is logged in, display navigation options
    if st.session_state.logged_in:
        selected = option_menu('Multiple Disease Prediction System',
                               ['Home',
                                'Diabetes Prediction',
                                'Heart Disease Prediction',
                                'Parkinsons Prediction',
                                'How to use these models',
                                'Learn about Diseases',
                                'About'],  # New section added
                               menu_icon='🧑‍⚕️',  # Corrected sidebar logo
                               icons=['house-door', 'activity', 'heart', 'person', 'info-circle', 'book'],  # Icon added
                               default_index=0)


# Home Page
if st.session_state.logged_in and selected == 'Home':
    st.title("Welcome to Health Assistant")
    st.write("Welcome to Health Assistant, your personalized health companion!")
    st.write("This tool utilizes advanced Machine Learning models to help you predict and manage various diseases.")
    st.write("Whether you want to assess your risk for diabetes, heart disease, or Parkinson's disease, we've got you covered.")
    st.write("In addition to predictions, you can also explore comprehensive information about these diseases to empower yourself with knowledge.")
    st.write("Get started by selecting an option from the sidebar and take control of your health journey today!")

    # Disclaimer
    st.subheader("Disclaimer:")
    st.write("This Web App may not provide accurate predictions at all times. When in doubt, please enter the values again and verify the predictions.")
    st.write("You are requested to provide your Name and Email for sending details about your test results. Rest assured, your information is safe and will be kept confidential.")
    st.write("It is important to note that individuals with specific risk factors or concerns should consult with healthcare professionals for personalized advice and management.")
    st.write("Please note that while this model is under development, it may not always provide precise results. We advise using it for predictive purposes only at this stage. It's important not to solely rely on the predictions generated by the model until further improvements are made.")


Age = ''  # Initialize Age variable

# Diabetes Prediction Page
if st.session_state.logged_in and selected == 'Diabetes Prediction':
    # page title
    st.title('Diabetes Prediction using ML')

    # Getting user's name and Gmail ID
    st.subheader("Please provide your information to proceed with the prediction:")
    name = st.text_input("Your Name:")
    gmail_id = st.text_input("Your Gmail ID:")

    # Placeholder for prediction result
    diab_diagnosis = ''

    # Placeholder for patient data
    patient_data = {}

    # Initialize variables outside of the block
    Age = ''  # Initialize Age variable

    # Check if both name and Gmail ID are provided and if Gmail ID ends with "@gmail.com"
    if name and gmail_id and gmail_id.endswith("@gmail.com"):
        st.write("Thank you for providing your information. Please proceed with the prediction below.")

        # Use st.form to encapsulate the input fields and buttons related to prediction
        with st.form("diabetes_prediction_form"):
            # Getting the input data from the user
            col1, col2, col3 = st.columns(3)
            with col1:
                Pregnancies = st.number_input('Number of Pregnancies', min_value=0, max_value=20, step=1)
            with col2:
                Glucose = st.number_input('Glucose Level', min_value=0, max_value=200, step=1)
            with col3:
                BloodPressure = st.number_input('Blood Pressure value', min_value=0, max_value=200, step=1)
            with col1:
                SkinThickness = st.number_input('Skin Thickness value', min_value=0, max_value=100, step=1)
            with col2:
                Insulin = st.number_input('Insulin Level', min_value=0, max_value=900, step=1)
            with col3:
                BMI = st.number_input('BMI value', min_value=0.0, max_value=70.0, step=0.1)
            with col1:
                DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0, max_value=2.5, step=0.01)
            with col2:
                Age = st.number_input('Age of the Person', min_value=0, max_value=120, step=1)

            # Button to trigger the prediction
            submitted = st.form_submit_button("Get Diabetes Test Result")

        # Check if the form is submitted
        if submitted:
            # code for Prediction
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                          BMI, DiabetesPedigreeFunction, Age]
            user_input = [float(x) for x in user_input]
            diab_prediction = diabetes_model.predict([user_input])
            if diab_prediction[0] == 1:
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'

            # Store patient data
            patient_data = {
                "Name": name,
                "Age": Age,
                "Pregnancies": Pregnancies,
                "Glucose": Glucose,
                "Blood Pressure": BloodPressure,
                "Skin Thickness": SkinThickness,
                "Insulin": Insulin,
                "BMI": BMI,
                "Diabetes Pedigree Function": DiabetesPedigreeFunction
            }

            # Define normal ranges and units for each parameter
            normal_ranges = {
                "Pregnancies": "0-10",
                "Glucose": "70-125 mg/dl",
                "Blood Pressure": "120/80 mmHg",
                "Skin Thickness": "8-25 mm",
                "Insulin": "25-250 mIU/L",
                "BMI": "18-25 kg/m^2",
                "Diabetes Pedigree Function": "< 1"
            }

            # Display prediction result
            st.success(diab_diagnosis)

            # Display patient information
            st.subheader("Patient Information:")
            st.write(f"Name: {name}")  # Print the value of name
            st.write(f"Age: {Age}")  # Print the value of Age

            # Display normal ranges and units in a table
            st.subheader("Detailed Report:")
            parameter_names = list(normal_ranges.keys())
            normal_range_values = [normal_ranges[param] for param in parameter_names]
            patient_values = [patient_data[param] if param in patient_data else "" for param in parameter_names]
            df_normal_ranges = pd.DataFrame({
                "Parameter Name": parameter_names,
                "Normal Range": normal_range_values,
                "Patient Values": patient_values
            })
            st.table(df_normal_ranges)


    # Warning for invalid Gmail ID
    if gmail_id and not gmail_id.endswith("@gmail.com"):
        st.warning("Please provide a valid Gmail ID ending with '@gmail.com'.")
    # Warning for missing name or Gmail ID
    elif not (name and gmail_id):
        st.warning("Please provide both your name and Gmail ID to proceed with the prediction.")




# Heart Disease Prediction Page
if st.session_state.logged_in and selected == 'Heart Disease Prediction':
    # Page title
    st.title('Heart Disease Prediction using ML')

    # Getting user's name and Gmail ID
    st.subheader("Please provide your information to proceed with the prediction:")
    name = st.text_input("Your Name:")
    gmail_id = st.text_input("Your Gmail ID:")

    # Placeholder for prediction result
    heart_diagnosis = ''

    # Placeholder for patient data
    patient_data = {}

    # Check if both name and Gmail ID are provided and if Gmail ID ends with "@gmail.com"
    if name and gmail_id and gmail_id.endswith("@gmail.com"):
        st.write("Thank you for providing your information. Please proceed with the prediction below.")

        # Use st.form to encapsulate the input fields and buttons related to prediction
        with st.form("heart_disease_prediction_form"):
            # Getting the input data from the user
            col1, col2, col3 = st.columns(3)
            with col1:
                age = st.number_input('Age', min_value=0, max_value=150, step=1)
                sex = st.number_input('Sex', min_value=0, max_value=1, step=1)
                cp = st.number_input('Chest Pain types', min_value=0, max_value=3, step=1)
            with col2:
                trestbps = st.number_input('Resting Blood Pressure', min_value=0, max_value=300, step=1)
                chol = st.number_input('Serum Cholestoral in mg/dl', min_value=0, max_value=600, step=1)
                fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl', min_value=0, max_value=1, step=1)
            with col3:
                restecg = st.number_input('Resting Electrocardiographic results', min_value=0, max_value=2, step=1)
                thalach = st.number_input('Maximum Heart Rate achieved', min_value=0, max_value=300, step=1)
                exang = st.number_input('Exercise Induced Angina', min_value=0, max_value=1, step=1)
            with col1:
                oldpeak = st.number_input('ST depression induced by exercise', min_value=0.0, max_value=10.0, step=0.1)
                slope = st.number_input('Slope of the peak exercise ST segment', min_value=0, max_value=2, step=1)
            with col2:
                ca = st.number_input('Major vessels colored by flourosopy', min_value=0, max_value=4, step=1)
                thal = st.number_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect', min_value=0, max_value=2, step=1)

            # Button to trigger the prediction
            submitted = st.form_submit_button("Get Heart Disease Test Result")

        # Check if the form is submitted
        if submitted:
            # Code for Prediction
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            user_input = [float(x) for x in user_input]
            heart_prediction = heart_disease_model.predict([user_input])
            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'

            # Store patient data
            patient_data = {
                "Name": name,
                "Age": age,
                "Sex": sex,
                "Chest Pain Types": cp,
                "Resting Blood Pressure": trestbps,
                "Serum Cholestoral": chol,
                "Fasting Blood Sugar": fbs,
                "Resting Electrocardiographic Results": restecg,
                "Maximum Heart Rate Achieved": thalach,
                "Exercise Induced Angina": exang,
                "ST Depression Induced by Exercise": oldpeak,
                "Slope of the Peak Exercise ST Segment": slope,
                "Major Vessels Colored by Flourosopy": ca,
                "Thal": thal
            }

            # Define normal ranges and units for each parameter
            normal_ranges = {
                "Age": "0-150",
                "Sex": "0-1",
                "Chest Pain Types": "0-3",
                "Resting Blood Pressure": "0-300 mmHg",
                "Serum Cholestoral": "0-600 mg/dl",
                "Fasting Blood Sugar": "0-1",
                "Resting Electrocardiographic Results": "0-2",
                "Maximum Heart Rate Achieved": "0-300 bpm",
                "Exercise Induced Angina": "0-1",
                "ST Depression Induced by Exercise": "0.0-10.0",
                "Slope of the Peak Exercise ST Segment": "0-2",
                "Major Vessels Colored by Flourosopy": "0-4",
                "Thal": "0-2"
            }

            # Display prediction result
            st.success(heart_diagnosis)

            # Display patient information
            st.subheader("Patient Information:")
            st.write(f"Name: {name}")  # Print the value of name
            st.write(f"Age: {age}")  # Print the value of Age

            # Display detailed report in a table
            st.subheader("Detailed Report:")
            parameter_names = list(normal_ranges.keys())
            normal_range_values = [normal_ranges[param] for param in parameter_names]
            patient_values = [patient_data[param] if param in patient_data else "" for param in parameter_names]
            df_normal_ranges = pd.DataFrame({
                "Parameter Name": parameter_names,
                "Normal Range": normal_range_values,
                "Patient Values": patient_values
            })
            st.table(df_normal_ranges)


    # Warning for invalid Gmail ID
    if gmail_id and not gmail_id.endswith("@gmail.com"):
        st.warning("Please provide a valid Gmail ID ending with '@gmail.com'.")
    # Warning for missing name or Gmail ID
    elif not (name and gmail_id):
        st.warning("Please provide both your name and Gmail ID to proceed with the prediction.")



# Parkinson's Prediction Page
if st.session_state.logged_in and selected == "Parkinsons Prediction":
    # Page title
    st.title("Parkinson's Disease Prediction using ML")

    # Getting user's name and Gmail ID
    st.subheader("Please provide your information to proceed with the prediction:")
    name = st.text_input("Your Name:")
    gmail_id = st.text_input("Your Gmail ID:")

    # Placeholder for prediction result
    parkinsons_diagnosis = ''

    # Placeholder for patient data
    patient_data = {}

    # Check if both name and Gmail ID are provided and if Gmail ID ends with "@gmail.com"
    if name and gmail_id and gmail_id.endswith("@gmail.com"):
        st.write("Thank you for providing your information. Please proceed with the prediction below.")

        # Use st.form to encapsulate the input fields and button related to prediction
        with st.form("parkinsons_prediction_form"):
            # Getting the input data from the user
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                fo = st.number_input('MDVP-Fo(Hz)', min_value=0.0, max_value=None, step=0.1)
            with col2:
                fhi = st.number_input('MDVP-Fhi(Hz)', min_value=0.0, max_value=None, step=0.1)
            with col3:
                flo = st.number_input('MDVP-Flo(Hz)', min_value=0.0, max_value=None, step=0.1)
            with col4:
                Jitter_percent = st.number_input('MDVP-Jitter(%)', min_value=0.0, max_value=None, step=0.01)
            with col5:
                Jitter_Abs = st.number_input('MDVP-Jitter(Abs)', min_value=0.0, max_value=None, step=0.001)
            with col1:
                RAP = st.number_input('MDVP-RAP', min_value=0.0, max_value=None, step=0.001)
            with col2:
                PPQ = st.number_input('MDVP-PPQ', min_value=0.0, max_value=None, step=0.001)
            with col3:
                DDP = st.number_input('Jitter-DDP', min_value=0.0, max_value=None, step=0.001)
            with col4:
                Shimmer = st.number_input('MDVP-Shimmer', min_value=0.0, max_value=None, step=0.01)
            with col5:
                Shimmer_dB = st.number_input('MDVP-Shimmer(dB)', min_value=0.0, max_value=None, step=0.1)
            with col1:
                APQ3 = st.number_input('Shimmer-APQ3', min_value=0.0, max_value=None, step=0.01)
            with col2:
                APQ5 = st.number_input('Shimmer-APQ5', min_value=0.0, max_value=None, step=0.01)
            with col3:
                APQ = st.number_input('MDVP-APQ', min_value=0.0, max_value=None, step=0.01)
            with col4:
                DDA = st.number_input('Shimmer-DDA', min_value=0.0, max_value=None, step=0.01)
            with col5:
                NHR = st.number_input('NHR', min_value=0.0, max_value=None, step=0.01)
            with col1:
                HNR = st.number_input('HNR', min_value=0.0, max_value=None, step=0.1)
            with col2:
                RPDE = st.number_input('RPDE', min_value=0.0, max_value=None, step=0.01)
            with col3:
                DFA = st.number_input('DFA', min_value=0.0, max_value=None, step=0.01)
            with col4:
                spread1 = st.number_input('spread1', min_value=0.0, max_value=None, step=0.01)
            with col5:
                spread2 = st.number_input('spread2', min_value=0.0, max_value=None, step=0.01)
            with col1:
                D2 = st.number_input('D2', min_value=0.0, max_value=None, step=0.1)
            with col2:
                PPE = st.number_input('PPE', min_value=0.0, max_value=None, step=0.01)

            # Button to trigger the prediction
            submitted = st.form_submit_button("Get Parkinson's Test Result")

        # Check if the form is submitted
        if submitted:
            # Code for Prediction
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                          RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                          APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
            user_input = [float(x) for x in user_input]
            parkinsons_prediction = parkinsons_model.predict([user_input])
            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"

            # Store patient data
            patient_data = {
                "Name": name,
                "MDVP-Fo(Hz)": fo,
                "MDVP-Fhi(Hz)": fhi,
                "MDVP-Flo(Hz)": flo,
                "MDVP-Jitter(%)": Jitter_percent,
                "MDVP-Jitter(Abs)": Jitter_Abs,
                "MDVP-RAP": RAP,
                "MDVP-PPQ": PPQ,
                "Jitter-DDP": DDP,
                "MDVP-Shimmer": Shimmer,
                "MDVP-Shimmer(dB)": Shimmer_dB,
                "Shimmer-APQ3": APQ3,
                "Shimmer-APQ5": APQ5,
                "MDVP-APQ": APQ,
                "Shimmer-DDA": DDA,
                "NHR": NHR,
                "HNR": HNR,
                "RPDE": RPDE,
                "DFA": DFA,
                "spread1": spread1,
                "spread2": spread2,
                "D2": D2,
                "PPE": PPE
            }

            # Normal ranges for Parkinson's Disease parameters
            normal_ranges = {
                "MDVP-Fo(Hz)": "0.0 - 300.0",
                "MDVP-Fhi(Hz)": "0.0 - 300.0",
                "MDVP-Flo(Hz)": "0.0 - 300.0",
                "MDVP-Jitter(%)": "0.0 - 1.0",
                "MDVP-Jitter(Abs)": "0.0 - 0.1",
                "MDVP-RAP": "0.0 - 0.1",
                "MDVP-PPQ": "0.0 - 0.1",
                "Jitter-DDP": "0.0 - 0.3",
                "MDVP-Shimmer": "0.0 - 1.0",
                "MDVP-Shimmer(dB)": "0.0 - 30.0",
                "Shimmer-APQ3": "0.0 - 1.0",
                "Shimmer-APQ5": "0.0 - 1.0",
                "MDVP-APQ": "0.0 - 1.0",
                "Shimmer-DDA": "0.0 - 1.0",
                "NHR": "0.0 - 1.0",
                "HNR": "0.0 - 40.0",
                "RPDE": "0.0 - 1.0",
                "DFA": "0.0 - 1.0",
                "spread1": "0.0 - 1.0",
                "spread2": "0.0 - 1.0",
                "D2": "0.0 - 20.0",
                "PPE": "0.0 - 1.0"
            }

            # Display prediction result
            st.success(parkinsons_diagnosis)

            # Display patient information
            st.subheader("Patient Information:")
            st.write(f"Name: {name}")  # Print the value of name

            # Display detailed report in a table
            st.subheader("Detailed Report:")
            parameter_names = list(normal_ranges.keys())
            normal_range_values = [normal_ranges[param] for param in parameter_names]
            patient_values = [patient_data[param] if param in patient_data else "" for param in parameter_names]
            df_report = pd.DataFrame({
                'Parameter Name': parameter_names,
                'Normal Range': normal_range_values,
                'Patient Value': patient_values
            })
            st.dataframe(df_report)



    
    # Warning for invalid Gmail ID
    elif gmail_id and not gmail_id.endswith("@gmail.com"):
        st.warning("Please provide a valid Gmail ID ending with '@gmail.com'.")


    
    # Warning for invalid Gmail ID
    if gmail_id and not gmail_id.endswith("@gmail.com"):
        st.warning("Please provide a valid Gmail ID ending with '@gmail.com'.")
    # Warning for missing name or Gmail ID
    elif not (name and gmail_id):
        st.warning("Please provide both your name and Gmail ID to proceed with the prediction.")


# How to use these models
if st.session_state.logged_in and selected == 'How to use these models':
    st.title("How to use these models (Understanding the meaning of the input fields)")

    # Explanation for Diabetes Prediction
    with st.expander("Diabetes Prediction", expanded=False):
        st.write("To predict diabetes, input the following numerical values corresponding to the patient's health metrics:")
        st.write("- **Pregnancies:** Number of times the patient has been pregnant.")
        st.write("- **Glucose:** Plasma glucose concentration measured 2 hours after consuming a glucose solution during an oral glucose tolerance test.")
        st.write("- **Blood Pressure:** Diastolic blood pressure, measured in millimeters of mercury (mm Hg).")
        st.write("- **Skin Thickness:** Thickness of the triceps skin fold, measured in millimeters (mm).")
        st.write("- **Insulin:** 2-Hour serum insulin level, measured in microunits per milliliter (mu U/ml).")
        st.write("- **BMI:** Body mass index, calculated as weight in kilograms divided by the square of height in meters (kg/m^2).")
        st.write("- **Diabetes Pedigree Function:** A numerical value that represents the likelihood of diabetes based on family history.")
        st.write("- **Age:** Age of the patient in years.")

    # Explanation for Heart Disease Prediction
    with st.expander("Heart Disease Prediction", expanded=False):
        st.write("To predict heart disease, input the following numerical values corresponding to the patient's health metrics:")
        st.write("- **Age:** Age of the patient in years.")
        st.write("- **Sex:** Gender of the patient (0 = female, 1 = male).")
        st.write("- **Chest Pain Type:** Type of chest pain experienced by the patient (1 = typical angina, 2 = atypical angina, 3 = non-anginal pain, 4 = asymptomatic).")
        st.write("- **Resting Blood Pressure:** Resting blood pressure measured in millimeters of mercury (mm Hg).")
        st.write("- **Cholesterol:** Serum cholesterol level in mg/dl.")
        st.write("- **Fasting Blood Sugar:** Fasting blood sugar level measured in mg/dl (1 = true, 0 = false).")
        st.write("- **Resting ECG:** Resting electrocardiographic results (0 = normal, 1 = having ST-T wave abnormality, 2 = showing probable or definite left ventricular hypertrophy by Estes' criteria).")
        st.write("- **Max Heart Rate:** Maximum heart rate achieved during exercise.")
        st.write("- **Exercise Induced Angina:** Exercise-induced angina (1 = yes, 0 = no).")
        st.write("- **ST Depression:** ST depression induced by exercise relative to rest.")
        st.write("- **Slope of Peak Exercise ST Segment:** Slope of the peak exercise ST segment (1 = upsloping, 2 = flat, 3 = downsloping).")
        st.write("- **Number of Major Vessels:** Number of major vessels (0-3) colored by fluoroscopy.")
        st.write("- **Thalassemia:** Thalassemia (3 = normal, 6 = fixed defect, 7 = reversible defect).")

    # Explanation for Parkinson's Disease Prediction
    with st.expander("Parkinson's Disease Prediction", expanded=False):
        st.write("To predict Parkinson's disease, input the following numerical values corresponding to the patient's health metrics:")
        st.write("- **Age:** Age of the patient in years.")
        st.write("- **Sex:** Gender of the patient (0 = female, 1 = male).")
        st.write("- **Resting Tremor:** Severity of resting tremor observed in the patient (0-4).")
        st.write("- **Tremor at Action:** Severity of tremor observed during action (0-4).")
        st.write("- **Rigidity:** Severity of rigidity observed in the patient (0-4).")
        st.write("- **Finger Tapping:** Severity of finger tapping impairment (0-4).")
        st.write("- **Handwriting:** Severity of handwriting impairment (0-4).")
        st.write("- **Drawing:** Severity of drawing impairment (0-4).")
        st.write("- **Essential Tremor:** Presence of essential tremor in the patient (0 = no, 1 = yes).")



# New Section: Learn about Diseases
if st.session_state.logged_in and selected == 'Learn about Diseases':
    st.title("Learn about Diseases")
    st.write("Here you can find information about the three diseases:")
    
    # Use expander to create a hamburger menu for each disease
    with st.expander("Diabetes", expanded=False):
        st.write("Diabetes mellitus is a chronic metabolic disorder characterized by elevated blood glucose levels over a prolonged period. This condition occurs when the body either doesn't produce enough insulin or cannot effectively use the insulin it produces. Insulin is a hormone that regulates blood sugar and allows cells to utilize glucose for energy.")
        st.write("There are three main types of diabetes:")
        st.write("- **Type 1 diabetes:** This type occurs when the body's immune system mistakenly attacks and destroys the insulin-producing cells in the pancreas. People with type 1 diabetes require lifelong insulin therapy to survive.")
        st.write("- **Type 2 diabetes:** This is the most common type of diabetes, accounting for around 90% of cases. It occurs when the body becomes resistant to insulin or doesn't produce enough insulin to maintain normal blood glucose levels. Type 2 diabetes is often linked to lifestyle factors such as obesity, unhealthy diet, and lack of physical activity.")
        st.write("- **Gestational diabetes:** This type develops during pregnancy and usually resolves after childbirth. However, women who have had gestational diabetes have an increased risk of developing type 2 diabetes later in life.")
        st.write("Diabetes can lead to various complications if not managed properly, including:")
        st.write("- Cardiovascular disease")
        st.write("- Kidney disease")
        st.write("- Nerve damage (neuropathy)")
        st.write("- Eye damage (retinopathy)")
        st.write("- Foot damage")
        st.write("- Skin conditions")
        st.write("Managing diabetes involves a combination of lifestyle changes, medication (including insulin therapy for type 1 diabetes), and regular monitoring of blood sugar levels. Key strategies for managing diabetes include:")
        st.write("- Adopting a healthy diet rich in fruits, vegetables, whole grains, and lean proteins, while limiting sugar, refined carbohydrates, and saturated fats.")
        st.write("- Engaging in regular physical activity to help control weight, lower blood sugar levels, and improve overall health.")
        st.write("- Monitoring blood glucose levels regularly using a glucose meter.")
        st.write("- Taking prescribed medications as directed, including insulin")

    with st.expander("Heart Disease", expanded=False):
        st.write("Heart disease refers to conditions that involve narrowing or blockage of blood vessels leading to the heart (coronary arteries). These conditions can cause heart attacks, chest pain (angina), or other symptoms. Heart disease is a leading cause of death worldwide.")
        st.write("There are several types of heart disease, including:")
        st.write("- Coronary artery disease (CAD): This is the most common type of heart disease and is caused by the buildup of plaque (fat, cholesterol, and other substances) in the coronary arteries, leading to reduced blood flow to the heart.")
        st.write("- Heart failure: Also known as congestive heart failure, this condition occurs when the heart cannot pump enough blood to meet the body's needs. It can result from various underlying conditions, such as CAD, high blood pressure, or cardiomyopathy.")
        st.write("- Arrhythmias: These are abnormal heart rhythms, which can cause the heart to beat too fast, too slow, or irregularly. Arrhythmias can lead to symptoms such as palpitations, dizziness, or fainting.")
        st.write("- Valvular heart disease: This involves damage or defects in one or more of the heart's valves, which can affect blood flow through the heart.")
        st.write("Risk factors for heart disease include:")
        st.write("- High blood pressure")
        st.write("- High cholesterol levels")
        st.write("- Smoking")
        st.write("- Diabetes")
        st.write("- Obesity")
        st.write("- Family history of heart disease")
        st.write("Preventive measures for heart disease include adopting a healthy lifestyle, such as eating a balanced diet, exercising regularly, maintaining a healthy weight, avoiding tobacco use, and managing underlying health conditions.")

    with st.expander("Parkinson's Disease", expanded=False):
        st.write("Parkinson's disease is a neurodegenerative disorder that affects movement. It typically develops gradually, starting with mild tremors and stiffness, and worsens over time. The primary symptoms of Parkinson's disease include:")
        st.write("- Tremors (shaking) in the hands, arms, legs, jaw, or head")
        st.write("- Bradykinesia (slowness of movement)")
        st.write("- Rigidity (stiffness of the limbs and trunk)")
        st.write("- Postural instability (impaired balance and coordination)")
        st.write("As Parkinson's disease progresses, additional symptoms may emerge, including:")
        st.write("- Difficulty with walking and balance")
        st.write("- Freezing of gait (sudden, brief inability to move the feet)")
        st.write("- Stooped posture")
        st.write("- Speech and swallowing difficulties")
        st.write("- Cognitive impairment (e.g., memory loss, dementia)")
        st.write("- Mood changes (e.g., depression, anxiety)")
        st.write("The exact cause of Parkinson's disease is unknown, but it is believed to involve a combination of genetic and environmental factors. There is currently no cure for Parkinson's disease, but treatments such as medication, physical therapy, and deep brain stimulation can help manage symptoms and improve quality of life for individuals with the condition.")

    st.write("---")

# About Page
if st.session_state.logged_in and selected == 'About':
    st.title("About")
    st.write("Welcome to the Health Assistant application!")
    st.write("Health Assistant is a solo project developed by you, aimed at providing predictive analysis for multiple diseases using Machine Learning models.")
    st.write("Here's what you need to know about Health Assistant:")

    st.subheader("Purpose:")
    st.write("The primary purpose of Health Assistant is to empower individuals to take proactive measures towards their health. By leveraging advanced Machine Learning algorithms, the application offers predictions for diabetes, heart disease, and Parkinson's disease, helping users assess their risk factors and make informed decisions.")

    st.subheader("Development:")
    st.write("Health Assistant is developed solely by you using Python and Streamlit, making it accessible and user-friendly. The Machine Learning models used for disease prediction are trained on relevant datasets to ensure accuracy and reliability.")

    st.subheader("Future Plans:")
    st.write("As the sole developer of Health Assistant, you are committed to continuously improving the application to better serve users' needs. Here are some planned enhancements:")
    st.write("- Expansion of disease prediction capabilities: You aim to include predictions for additional diseases to offer a more comprehensive health assessment.")
    st.write("- Integration of personalized recommendations: In future updates, Health Assistant will provide tailored recommendations based on users' health data and predictive analysis.")
    st.write("- Enhanced user experience: You're working on refining the user interface and incorporating interactive features to enhance usability and engagement.")

    st.subheader("Feedback:")
    st.write("Your feedback is invaluable to the development of Health Assistant. If you have any suggestions, feature requests, or encounter any issues while using the application, please don't hesitate to reach out.")

    st.write("Thank you for choosing Health Assistant as your health companion!")