import yfinance as yf
import pandas as pd
import numpy as np
import json
import re

# UNIVERSO AMPLIADO DE ACTIVOS (~120 TIKKERS)
UNIVERSO = {
    # Cartera
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
    
    # Tech & Semiconductores
    "NVDA": {"fullName": "NVIDIA Corp.", "operability": "CEDEAR", "risk": "Moderado"},
    "TSLA": {"fullName": "Tesla Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "AAPL": {"fullName": "Apple Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "MSFT": {"fullName": "Microsoft Corp.", "operability": "CEDEAR", "risk": "Bajo"},
    "AMZN": {"fullName": "Amazon.com", "operability": "CEDEAR", "risk": "Moderado"},
    "GOOGL": {"fullName": "Alphabet Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "META": {"fullName": "Meta Platforms", "operability": "CEDEAR", "risk": "Moderado"},
    "AMD": {"fullName": "Advanced Micro Devices", "operability": "CEDEAR", "risk": "Alto"},
    "INTC": {"fullName": "Intel Corp.", "operability": "CEDEAR", "risk": "Alto"},
    "AVGO": {"fullName": "Broadcom Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "QCOM": {"fullName": "QUALCOMM Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "ARM": {"fullName": "Arm Holdings", "operability": "CEDEAR", "risk": "Alto"},
    "SMCI": {"fullName": "Super Micro Computer", "operability": "CEDEAR", "risk": "Alto"},
    "ASML": {"fullName": "ASML Holding", "operability": "CEDEAR", "risk": "Moderado"},
    "LRCX": {"fullName": "Lam Research", "operability": "CEDEAR", "risk": "Moderado"},

    # Software, Cloud & Ciberseguridad
    "PLTR": {"fullName": "Palantir Tech", "operability": "CEDEAR", "risk": "Alto"},
    "CRWD": {"fullName": "CrowdStrike", "operability": "CEDEAR", "risk": "Alto"},
    "NET": {"fullName": "Cloudflare Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "DDOG": {"fullName": "Datadog Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "SNOW": {"fullName": "Snowflake Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "PANW": {"fullName": "Palo Alto Networks", "operability": "CEDEAR", "risk": "Moderado"},
    "FTNT": {"fullName": "Fortinet Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "ZS": {"fullName": "Zscaler Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "MDB": {"fullName": "MongoDB Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "NOW": {"fullName": "ServiceNow Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "CRM": {"fullName": "Salesforce Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "ORCL": {"fullName": "Oracle Corp.", "operability": "CEDEAR", "risk": "Bajo"},
    "ADBE": {"fullName": "Adobe Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "UBER": {"fullName": "Uber Technologies", "operability": "CEDEAR", "risk": "Moderado"},
    "ABNB": {"fullName": "Airbnb Inc.", "operability": "CEDEAR", "risk": "Alto"},

    # Fintech, E-Commerce & Consumo
    "MELI": {"fullName": "MercadoLibre Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "SHOP": {"fullName": "Shopify Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "BABA": {"fullName": "Alibaba Group", "operability": "CEDEAR", "risk": "Alto"},
    "JD": {"fullName": "JD.com Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "PDD": {"fullName": "PDD Holdings", "operability": "CEDEAR", "risk": "Alto"},
    "PYPL": {"fullName": "PayPal Holdings", "operability": "CEDEAR", "risk": "Moderado"},
    "SQ": {"fullName": "Block Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "HOOD": {"fullName": "Robinhood Markets", "operability": "Lemon", "risk": "Alto"},
    "COIN": {"fullName": "Coinbase Global", "operability": "CEDEAR", "risk": "Alto"},
    "ROKU": {"fullName": "Roku Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "NFLX": {"fullName": "Netflix Inc.", "operability": "CEDEAR", "risk": "Alto"},
    "DIS": {"fullName": "Walt Disney Co.", "operability": "CEDEAR", "risk": "Bajo"},
    "SBUX": {"fullName": "Starbucks Corp.", "operability": "CEDEAR", "risk": "Bajo"},
    "NKE": {"fullName": "NIKE Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "COST": {"fullName": "Costco Wholesale", "operability": "CEDEAR", "risk": "Bajo"},
    "WMT": {"fullName": "Walmart Inc.", "operability": "CEDEAR", "risk": "Bajo"},

    # Salud & Biotecnología
    "LLY": {"fullName": "Eli Lilly and Co.", "operability": "CEDEAR", "risk": "Moderado"},
    "NVO": {"fullName": "Novo Nordisk", "operability": "CEDEAR", "risk": "Moderado"},
    "PFE": {"fullName": "Pfizer Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "JNJ": {"fullName": "Johnson & Johnson", "operability": "CEDEAR", "risk": "Bajo"},
    "UNH": {"fullName": "UnitedHealth Group", "operability": "CEDEAR", "risk": "Bajo"},
    "ABBV": {"fullName": "AbbVie Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "MRK": {"fullName": "Merck & Co.", "operability": "CEDEAR", "risk": "Bajo"},
    "GILD": {"fullName": "Gilead Sciences", "operability": "CEDEAR", "risk": "Bajo"},

    # Financieros, Industriales & Energía
    "JPM": {"fullName": "JPMorgan Chase", "operability": "CEDEAR", "risk": "Bajo"},
    "BAC": {"fullName": "Bank of America", "operability": "CEDEAR", "risk": "Bajo"},
    "C": {"fullName": "Citigroup Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "GS": {"fullName": "Goldman Sachs", "operability": "CEDEAR", "risk": "Moderado"},
    "MS": {"fullName": "Morgan Stanley", "operability": "CEDEAR", "risk": "Moderado"},
    "V": {"fullName": "Visa Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "MA": {"fullName": "Mastercard Inc.", "operability": "CEDEAR", "risk": "Bajo"},
    "CAT": {"fullName": "Caterpillar Inc.", "operability": "CEDEAR", "risk": "Moderado"},
    "DE": {"fullName": "Deere & Co.", "operability": "CEDEAR", "risk": "Moderado"},
    "GE": {"fullName": "GE Aerospace", "operability": "CEDEAR", "risk": "Moderado"},
    "BA": {"fullName": "Boeing Co.", "operability": "CEDEAR", "risk": "Alto"},
    "XOM": {"fullName": "Exxon Mobil", "operability": "CEDEAR", "risk": "Bajo"},
    "CVX": {"fullName": "Chevron Corp.", "operability": "CEDEAR", "risk": "Bajo"},
    "OXY": {"fullName": "Occidental Petroleum", "operability": "CEDEAR", "risk": "Moderado"},
    
    # ETFs
    "SPY": {"fullName": "SPDR S&P 500 ETF", "operability": "CEDEAR", "risk": "Bajo"},
    "QQQ": {"fullName": "Invesco QQQ Trust", "operability": "CEDEAR", "risk": "Moderado"},
    "IWM": {"fullName": "iShares Russell 2000", "operability": "CEDEAR", "risk": "Alto"},
    "XLF": {"fullName": "Financial Select Sector", "operability": "Activo USA", "risk": "Bajo"},
    "SOXX": {"fullName": "iShares Semiconductor ETF", "operability": "Activo USA", "risk": "Alto"},
    "ARKK": {"fullName": "ARK Innovation ETF", "operability": "CEDEAR", "risk": "Alto"}
}

def calcular_rsi(series, period=14):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calcular_poc(df, bins=12):
    precios = df['Close']
    volumenes = df['Volume']
    rango = np.linspace(precios.min(), precios.max(), bins+1)
    perfil = np.zeros(bins)
    for i in range(bins):
        condicion = (precios >= rango[i]) & (precios < rango[i+1])
        perfil[i] = volumenes[condicion].sum()
    poc_idx = np.argmax(perfil)
    return (rango[poc_idx] + rango[poc_idx+1]) / 2

print("Descargando cotizaciones y procesando métricas...")
tickers_list = list(UNIVERSO.keys())
data_batch = yf.download(tickers_list, period="100d", interval="1d", group_by='ticker', progress=False)

resultados = []

for ticker in tickers_list:
    try:
        df = data_batch[ticker].dropna() if len(tickers_list) > 1 else data_batch.dropna()
        if df.empty or len(df) < 50:
            continue
            
        close = df['Close']
        sma20 = close.rolling(window=20).mean().iloc[-1]
        sma50 = close.rolling(window=50).mean().iloc[-1]
        rsi = calcular_rsi(close).iloc[-1]
        poc = calcular_poc(df.tail(20)) # POC del último mes
        
        cierre = close.iloc[-1]
        meta = UNIVERSO[ticker]
        
        # Lógica de detección de señales
        estado = "HOLD"
        tipo = "Continuación"
        fundamento = f"Cierre en ${cierre:.2f}. POC (20d) en ${poc:.2f}. "
        
        if cierre > sma20 and rsi > 55:
            estado = "BUY"
            tipo = "Aceleración"
            fundamento += f"Impulso alcista sobre SMA20. RSI en {rsi:.0f} avala la aceleración."
        elif cierre < sma20 and cierre > sma50 and rsi > 45:
            estado = "BUY"
            tipo = "Reversión"
            fundamento += f"Rebote sobre zona de soporte. POC (${poc:.2f}) actuando como base comprador."
        elif cierre < sma50 and rsi < 45:
            estado = "SELL"
            tipo = "Reversión"
            fundamento += f"Pérdida de SMA50. RSI debilitado ({rsi:.0f}); riesgo de buscar soportes inferiores."
        elif rsi > 72:
            estado = "WARNING"
            tipo = "Evaluación"
            fundamento += f"RSI en sobrecompra ({rsi:.0f}). Distancia elevada con el POC; vigilar toma de ganancias."
        else:
            fundamento += f"Consolidación en área de valor. RSI neutro ({rsi:.0f}). Sin definición inminente."

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
        pass

print(f"Procesados {len(resultados)} activos exitosamente.")

# Inyección directa dentro del archivo HTML
archivo_html = "Terminal.html"

try:
    with open(archivo_html, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Reemplaza el array MASTER_DB estático por el generado en vivo
    json_str = json.dumps(resultados, ensure_ascii=False, indent=12)
    nuevo_contenido = re.sub(
        r'const MASTER_DB = \[.*?\];',
        f'const MASTER_DB = {json_str};',
        contenido,
        flags=re.DOTALL
    )

    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

    print(f"¡Éxito! {archivo_html} ha sido actualizado con los datos del último cierre.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{archivo_html}' en este directorio.")