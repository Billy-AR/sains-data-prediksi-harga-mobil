import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model
with open('model_info.pkl', 'rb') as f:
    model_info = pickle.load(f)

model = model_info['model']
feature_cols = model_info['feature_cols']

st.set_page_config(page_title="Prediksi Harga Mobil", page_icon="🚗", layout="centered")

st.title("🚗 Prediksi Harga Mobil")
st.markdown("Masukkan spesifikasi mobil di bawah ini untuk memprediksi harganya.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    engine_size = st.number_input("Engine Size (L)", min_value=0.5, max_value=10.0, value=2.5, step=0.1)
    horsepower = st.number_input("Horsepower (HP)", min_value=50, max_value=600, value=180, step=10)
    curb_weight = st.number_input("Curb Weight (x1000 lbs)", min_value=1.0, max_value=6.0, value=3.2, step=0.1)
    fuel_capacity = st.number_input("Fuel Capacity (gallons)", min_value=5.0, max_value=40.0, value=17.0, step=0.5)

with col2:
    width = st.number_input("Width (inches)", min_value=50.0, max_value=100.0, value=70.0, step=0.5)
    length = st.number_input("Length (inches)", min_value=100.0, max_value=300.0, value=185.0, step=1.0)
    wheelbase = st.number_input("Wheelbase (inches)", min_value=80.0, max_value=150.0, value=105.0, step=0.5)
    fuel_efficiency = st.number_input("Fuel Efficiency (MPG)", min_value=5.0, max_value=60.0, value=26.0, step=1.0)

st.markdown("---")

if st.button("🔍 Prediksi Harga", use_container_width=True):
    input_data = pd.DataFrame({
        'Engine_size': [engine_size],
        'Horsepower': [horsepower],
        'Curb_weight': [curb_weight],
        'Fuel_capacity': [fuel_capacity],
        'Width': [width],
        'Length': [length],
        'Wheelbase': [wheelbase],
        'Fuel_efficiency': [fuel_efficiency]
    })

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Harga Prediksi: **${prediction:,.2f} ribu USD** (${prediction * 1000:,.0f} USD)")

    st.markdown("### Spesifikasi yang Diinputkan:")
    st.dataframe(input_data.T.rename(columns={0: 'Nilai'}), use_container_width=True)

st.markdown("---")
st.markdown(f"*Model: Linear Regression | R² Score: {model_info['r2']:.4f} | RMSE: {model_info['rmse']:.4f}*")
