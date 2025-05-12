from datetime import datetime

def clean_price(value):
    try:
        return float(str(value).strip().replace("₹", "").replace(",", ""))
    except:
        return None

def compare_prices(data, product, date):
    prices = {}
    for store, df in data.items():
        df["Product"] = df["Product"].astype(str).str.strip().str.lower()
        row = df[df["Product"] == product.lower().strip()]
        if not row.empty and date in df.columns:
            price = clean_price(row[date].values[0])
            if price is not None:
                prices[store] = price
    return prices

def get_price_change(data, product, current_date):
    changes = {}
    try:
        date_index = list(data.values())[0].columns.tolist().index(current_date)
        if date_index <= 1:
            return changes
        prev_date = list(data.values())[0].columns[date_index - 1]
    except Exception:
        return changes

    for store, df in data.items():
        df["Product"] = df["Product"].astype(str).str.strip().str.lower()
        row = df[df["Product"] == product.lower().strip()]
        if not row.empty:
            current_price = clean_price(row[current_date].values[0])
            prev_price = clean_price(row[prev_date].values[0])
            if current_price is not None and prev_price is not None:
                changes[store] = current_price - prev_price
    return changes

def get_price_trend(data, product, selected_stores=None):
    trend_data = []
    for store, df in data.items():
        if selected_stores and store not in selected_stores:
            continue
        df["Product"] = df["Product"].astype(str).str.strip().str.lower()
        row = df[df["Product"] == product.lower().strip()]
        if not row.empty:
            for date, value in row.iloc[0].items():
                if date != "Product":
                    price = clean_price(value)
                    if price is not None:
                        try:
                            parsed_date = datetime.strptime(date, "%d %b")
                            trend_data.append({"Store": store, "Date": parsed_date, "Price": price})
                        except:
                            continue
    return pd.DataFrame(trend_data)
