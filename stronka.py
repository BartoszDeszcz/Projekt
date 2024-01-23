import streamlit as st
import pickle
import pandas as pd

# Title of the page
st.title("Przewidywanie ceny mieszkania w Kalifornii")

# Input fields
wysokosc_geograficzna = st.text_input("Wysokość geograficzna")
lat = st.text_input("Szerokość geograficzna")
total_rooms = st.text_input("Liczba pokoi w bloku")
liczba_mieszkan_w_bloku = st.text_input("Liczba mieszkań w bloku")
liczba_sypialni = st.text_input("Liczba sypialni")
housing_median_age = st.text_input("Wiek nieruchomości")
median_income = st.text_input("Mediana przychodów mieszkańców bloku (podana w tysiącach dolarów)")

#Validate input values
if not wysokosc_geograficzna or not lat or not total_rooms or not liczba_mieszkan_w_bloku or not housing_median_age or not liczba_sypialni or not median_income:
    st.warning("Wprowadzaj wartości numeryczne w pola tekstowe.")
    st.stop()

# Convert input to numeric
input_data = {
    "wysokosc_geograficzna": float(wysokosc_geograficzna),
    "lat": float(lat),
    "total_rooms": float(total_rooms),
    "liczba_mieszkan_w_bloku": float(liczba_mieszkan_w_bloku),
    "housing_median_age": float(housing_median_age),
    "liczba_sypialni": float(liczba_sypialni),
    "median_income": float(median_income),
}

# Load the model
def wczytaj_model(filepath: str):
    with st.spinner('Wczytywanie modelu...'):
        return pickle.load(open(filepath, 'rb'))

loaded_model = wczytaj_model('/Users/bartusinhogaucho/Developer/vscode/ML/Projekt/linear_reg_model.pkl')

# Prepare input data for prediction
input_data = pd.DataFrame([input_data])

# Prediction
try:
    prediction = loaded_model.predict(input_data).squeeze()
    st.session_state['prediction'] = prediction
    st.success("Zrobione!")

    if st.session_state['prediction']:
        pred = st.session_state['prediction']
        st.markdown(
            """
            <style>
            [data-testid="stMetricValue"] {
                font-size: 34px;
                color: green;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.metric(label='Oszacowana wartość nieruchomości:', value=f"$ {pred:.2f}")

except Exception as e:
    st.error(f"Wystąpił błąd podczas przewidywania: {str(e)}")
