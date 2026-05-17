import gradio as gr
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Train model langsung dari dataset
def load_and_train():
    df = pd.read_excel('Car_sales.xlsx')
    df = df.dropna(subset=['Price_in_thousands'])
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    feature_cols = ['Engine_size', 'Horsepower', 'Curb_weight', 'Fuel_capacity',
                    'Width', 'Length', 'Wheelbase', 'Fuel_efficiency']
    X = df[feature_cols]
    y = df['Price_in_thousands']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    return model, feature_cols, rmse, r2

model, feature_cols, rmse, r2 = load_and_train()

def prediksi_harga(engine_size, horsepower, curb_weight, fuel_capacity,
                   width, length, wheelbase, fuel_efficiency):
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

    hasil = f"� Harga Prediksi: ${prediction:,.2f} ribu USD (${prediction * 1000:,.0f} USD)\n\n"
    hasil += "📋 Spesifikasi yang Diinputkan:\n"
    hasil += f"  • Engine Size     : {engine_size} L\n"
    hasil += f"  • Horsepower      : {horsepower} HP\n"
    hasil += f"  • Curb Weight     : {curb_weight} x1000 lbs\n"
    hasil += f"  • Fuel Capacity   : {fuel_capacity} gallons\n"
    hasil += f"  • Width           : {width} inches\n"
    hasil += f"  • Length          : {length} inches\n"
    hasil += f"  • Wheelbase       : {wheelbase} inches\n"
    hasil += f"  • Fuel Efficiency : {fuel_efficiency} MPG\n"

    return hasil

demo = gr.Interface(
    fn=prediksi_harga,
    inputs=[
        gr.Number(label="Engine Size (L)", value=2.5),
        gr.Number(label="Horsepower (HP)", value=180),
        gr.Number(label="Curb Weight (x1000 lbs)", value=3.2),
        gr.Number(label="Fuel Capacity (gallons)", value=17.0),
        gr.Number(label="Width (inches)", value=70.0),
        gr.Number(label="Length (inches)", value=185.0),
        gr.Number(label="Wheelbase (inches)", value=105.0),
        gr.Number(label="Fuel Efficiency (MPG)", value=26.0),
    ],
    outputs=gr.Textbox(label="Hasil Prediksi", lines=12),
    title="🚗 Prediksi Harga Mobil",
    description=f"Masukkan spesifikasi mobil untuk memprediksi harganya.\n\nModel: Linear Regression | R² Score: {r2:.4f} | RMSE: {rmse:.4f}",
    allow_flagging="never",
)

demo.launch()
