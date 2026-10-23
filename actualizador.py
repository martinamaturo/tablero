import yfinance as yf
import pandas as pd
import numpy as np
import json
from datetime import datetime

# Definición de activos y metadatos
ACTIVOS = {
    "ADP": {"fullName": "Automatic Data Processing", "operability": "CEDEAR", "risk": "Moderado"},
    "ALAB": {"fullName": "Astera Labs Inc.", "operability": "Activo USA", "risk": "Alto"},
    "AMAT": {"fullName": "Applied Materials", "operability": "CEDEAR", "risk": "Moderado"},
    "ANET": {"fullName": "Arista Networks", "operability": "CEDEAR", "risk": "Alto"},
    "MRVL": {"fullName": "Marvell Technology", "operability": "CEDEAR", "risk": "Alto"},
    "MU": {"fullName": "Micron Technology", "operability": "CEDEAR", "risk": "Alto"},
    "SNDK": {"fullName": "SanDisk (Western Digital)", "operability": "Activo USA", "risk": "Alto"},
    "CME": {"fullName": "CME Group Inc.", "operability": "Activo USA", "risk": "Bajo"},
    "WDC": {"fullName": "Western Digital Corp.", "operability": "CEDEAR", "risk": "Moderado"},
    "XBCI": {"fullName": "XBCI ETF", "operability": "Activo USA", "risk": "Alto"},
    "TSLA": {"fullName": "Tesla Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "NVDA": {"fullName": "NVIDIA Corp.", "operability": "CEDEAR", "risk": "Moderado"},
    "CRWD": {"fullName": "CrowdStrike", "operability": "CEDEAR", "risk": "Alto"},
    "MELI": {"fullName": "MercadoLibre", "operability": "CEDEAR", "risk": "Moderado"},
    "PLTR": {"fullName": "Palantir Tech", "operability": "CEDEAR", "risk": "Alto"},
    "AAPL": {"fullName": "Apple Inc.", "operability": "CEDEAR", "risk": "Bajo"}
}

def calcular_rsi(series, period=14):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calcular_poc(df, bins=10):
    precios = df['Close']
    volumenes = df['Volume']
    rango = np.linspace(precios.min(), precios.max(), bins+1)
    perfil = np.zeros(bins)
    for i in range(bins):
        condicion = (precios >= rango[i]) & (precios < rango[i+1])
        perfil[i] = volumenes[condicion].sum()
    poc_idx = np.argmax(perfil)
    return (rango[poc_idx] + rango[poc_idx+1]) / 2

resultados = []

for ticker, meta in ACTIVOS.items():
    try:
        data = yf.download(ticker, period="100d", interval="1d", progress=False)
        if data.empty:
            continue
            
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['RSI'] = calcular_rsi(data['Close'])
        poc = calcular_poc(data.tail(20)) # POC de las últimas 20 ruedas
        
        ultimo_cierre = float(data['Close'].iloc[-1])
        sma20 = float(data['SMA20'].iloc[-1])
        sma50 = float(data['SMA50'].iloc[-1])
        rsi = float(data['RSI'].iloc[-1])
        
        # Algoritmo de señales simplificado
        estado = "HOLD"
        tipo = "Continuación"
        fundamento = f"Precio actual: ${ultimo_cierre:.2f}. POC situado en ${poc:.2f}. "
        
        if ultimo_cierre > sma20 and rsi > 55:
            estado = "BUY"
            tipo = "Aceleración"
            fundamento += "Tendencia alcista confirmada sobre SMA20. Volumen avala el movimiento."
        elif ultimo_cierre < sma50 and rsi < 45:
            estado = "SELL"
            tipo = "Reversión"
            fundamento += "Pérdida de SMA50 con deterioro de momentum. Riesgo de caída profunda."
        elif rsi > 75:
            estado = "WARNING"
            tipo = "Evaluación"
            fundamento += "Niveles de sobrecompra extrema (RSI > 75). Precaución ante retrocesos."
        else:
            fundamento += "Consolidando cerca del área de valor. Sin catalizadores técnicos inmediatos."

        resultados.append({
            "ticker": ticker,
            "exchange": "NYSE/NASDAQ",
            "fullName": meta["fullName"],
            "operability": meta["operability"],
            "risk": meta["risk"],
            "type": tipo,
            "status": estado,
            "techInfo": fundamento
        })
    except Exception as e:
        print(f"Error procesando {ticker}: {e}")

# Exportar JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)
