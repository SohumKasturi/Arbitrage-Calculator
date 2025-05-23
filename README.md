---

# 🏀 NBA Arbitrage Betting Script

This Python script scans NBA betting odds from **FanDuel** and **DraftKings** using **The Odds API** and detects risk-free arbitrage opportunities in **Over/Under markets**. When a profitable opportunity is found, it calculates the stake distribution and sends an **SMS alert** via **Twilio**.

---

## 📌 Features

* Pulls real-time NBA odds from FanDuel and DraftKings
* Scans Over/Under odds for arbitrage opportunities (true profit < 1.0 sum of inverse odds)
* Calculates optimal stake distribution for guaranteed profit
* Sends instant SMS alerts via Twilio
* Rotates through multiple API keys automatically to avoid quota issues
* Runs continuously with 20-second intervals

---

## 🔧 Requirements

* Python 3.7+
* A valid [The Odds API](https://the-odds-api.com/) key (can rotate multiple)
* A [Twilio](https://www.twilio.com/) account for SMS alerts

---

## 📁 Setup

1. **Install Dependencies**

```bash
pip install requests twilio
```

2. **Configure API Keys**

Create a file named `api.txt` in the same directory and list your Odds API keys (one per line):

```
# List of Odds API keys
key_1_here
key_2_here
```

3. **Set Your Twilio Credentials**

In the script, replace the placeholders:

```python
TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio phone number
YOUR_PHONE_NUMBER = '+1234567890'    # Your personal phone number
```

---

## 🚀 Running the Script

To start the continuous arbitrage checker:

```bash
python arbitrage_detector.py
```

The script will:

* Pull odds data from FanDuel and DraftKings
* Detect arbitrage by comparing inverse odds combinations
* Print profitable scenarios and send SMS alerts

---

## 📈 Example Output

```
Starting arbitrage checker. Press Ctrl+C to stop.
==================================================
Checking odds at 15:32:45
bet on DK over and FD under
Bet on DK over: 1.95
Bet on FD under: 2.05
Stake A: 50.63
Stake B: 49.36
profit: 2.95
SMS alert sent successfully
Waiting 20 seconds before next check...
```

---

## 💡 How Arbitrage Is Calculated

If the sum of the inverse odds from two different outcomes (from different sportsbooks) is **less than 1.0**, an arbitrage exists:

```
1/odd_A + 1/odd_B < 1.0
```

The script explores all combinations of Over/Under odds across FanDuel and DraftKings.

---

## ⚠️ Notes

* Make sure you stay within the free limits of The Odds API (or provide multiple keys).
* Keep `api.txt` in the same directory as the script.
* SMS alerts may incur costs depending on your Twilio usage.

---

## 📄 License

This project is for personal and educational use only. Use responsibly and at your own risk when betting.

---
