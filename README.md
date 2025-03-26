# ✈️ FareFinder – Detect Cheap or Mistake Airfares with Python

**FareFinder** is a Python-based tool that searches for unusually low airfare prices between specified routes. It's designed to help you find potential **error fares** or **deep discounts** by using the Kiwi.com API (Tequila) to scan flight data within a specified date range.

---

## 🚀 Features

- 🔍 Search for flights between two cities within a flexible date range
- 💸 Set a maximum price threshold to flag cheap or mistake fares
- 🌐 Uses Kiwi's Tequila API (free to sign up)
- 📄 Print results with date, price, and booking link
- ⚙️ Easy to customize and extend

---

## 📦 Requirements

- Python 3.7+
- `requests` library

Install dependencies:
```bash
pip install requests
```

---

## 🔑 Setup

1. Sign up for a **free Kiwi Tequila API key**:  
   [https://tequila.kiwi.com/](https://tequila.kiwi.com/)

2. Copy your API key into the script:
   ```python
   headers = {"apikey": "YOUR_KIWI_API_KEY"}
   ```

---

## 🧪 Usage

Update the values in the script or call the function like this:

```python
origin = "ATL"  # From Atlanta
destination = "LON"  # To London
date_from = "10/05/2024"
date_to = "10/06/2024"
max_price = 200  # USD

find_low_fares(origin, destination, date_from, date_to, max_price)
```

Example output:
```
✈️ Atlanta ➡️ London on 2024-06-05
💵 Price: $172
🔗 Link: https://www.kiwi.com/...
```

---

## 📌 Notes

- Prices and availability can change rapidly—check links immediately.
- This tool helps **detect low fares** but doesn't guarantee they are mistake fares.
- Respect Kiwi's API rate limits and terms of use.

---

## 🔧 Planned Features

- ✉️ Email alerts for new low fares
- 📆 Flexible date scanning
- 📊 CSV export and fare history tracking
- 🛫 Multi-destination search loop

---

## 📄 License

MIT License

---

## 🤝 Contributing

Pull requests and suggestions are welcome! If you find a cool fare with this, let me know 😄

---

## ✉️ Author

**[Your Name]**  
Feel free to reach out on GitHub or open an issue for feedback or questions.
