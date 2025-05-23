import requests
import time
from twilio.rest import Client
import os

def get_next_api_key():
    api_keys_file = os.path.join(os.path.dirname(__file__), 'api.txt')
    with open(api_keys_file, 'r') as f:
        api_keys = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    while True:
        for key in api_keys:
            yield key

# Initialize API key generator
api_key_generator = get_next_api_key()
API_KEY = next(api_key_generator)

def get_fresh_api_key():
    global API_KEY
    API_KEY = next(api_key_generator)
    return API_KEY

SPORT = 'basketball_nba'
REGION = 'us'  # us = United States
MARKETS = 'h2h,spreads,totals'  # Options: h2h, spreads, totals
BOOKMAKERS = 'fanduel,draftkings'

url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'

params = {
    'apiKey': API_KEY,
    'regions': REGION,
    'markets': MARKETS,
    'bookmakers': BOOKMAKERS,
    'oddsFormat': 'decimal'
}

# Twilio credentials - replace with your actual credentials
TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_PHONE_NUMBER = '+1234567890'  # Replace with your Twilio number
YOUR_PHONE_NUMBER = '+1234567890'  # Replace with your phone number

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def profit_margin(odds1, odds2):
    implied_prob1 = 1 / odds1
    implied_prob2 = 1 / odds2
    total_prob = implied_prob1 + implied_prob2
    Stake_A = (implied_prob1/total_prob) * 100
    Stake_B = (implied_prob2/total_prob) * 100
    Stake = (Stake_A*odds1)
    profit = Stake - 100
    print("Stake A: " + str(Stake_A))
    print("Stake B: " + str(Stake_B))
    print("profit: " + str(profit))
    return

def send_sms_alert(message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print("SMS alert sent successfully")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def check_arbitrage():
    global API_KEY
    FDodds = []
    DKodds = []
    FDover = []
    FDcounter = 0
    FDunder = []
    DKover = []
    DKcounter = 0
    DKunder = []
    i = 0
    j = 0
    m1 = 'Fanduel'
    counter = 0
    arb = []

    response = requests.get(url, params=params)

    if response.status_code == 429:  # Too Many Requests
        print("API key quota exceeded, switching to next key...")
        API_KEY = get_fresh_api_key()
        params['apiKey'] = API_KEY
        response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return

    data = response.json()
    for game in data:
        print(f"{game['home_team']} vs {game['away_team']}")
        for bookmaker in game['bookmakers']:
            print(f"  {bookmaker['title']}")
            for market in bookmaker['markets']:
                print(f"    Market: {market['key']}")
                for outcome in market['outcomes']:
                    print(f"      {outcome['name']}: {outcome['price']}")

    for game in data:
        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    m1 = bookmaker['title']
                    if m1 == 'FanDuel':
                        FDodds.append(outcome['price'])
                    elif m1 == 'DraftKings':
                        DKodds.append(outcome['price'])

    if len(FDodds) != len(DKodds):
        print("Error: The number of odds from FanDuel and DraftKings do not match.")
        return

    while i < (len(FDodds))/2:
        FDover.append(FDodds[FDcounter])
        FDcounter += 2
        if FDcounter != 0:
            FDunder.append(FDodds[FDcounter-1])
        i += 1

    while j < (len(DKodds))/2:
        DKover.append(DKodds[DKcounter])
        DKcounter += 2
        if DKcounter != 0:
            DKunder.append(DKodds[DKcounter-1])
        j += 1

    for x in FDover:
        hi = []
        hi.append(1/DKover[counter]+1/FDunder[counter])
        hi.append(1/DKover[counter]+1/DKunder[counter])
        hi.append(1/FDover[counter]+1/FDunder[counter])
        hi.append(1/FDover[counter]+1/DKunder[counter])
        for sum in hi:
            if sum < 1:
                arb_message = "Arbitrage opportunity found!\n"
                if sum == 1/DKover[counter]+1/FDunder[counter]:
                    arb_message += f"DK over: {DKover[counter]}\nFD under: {FDunder[counter]}\n"
                    print("bet on DK over and FD under")
                    print("Bet on DK over: " + str(DKover[counter]))
                    print("Bet on FD under: " + str(FDunder[counter]))
                    profit_margin(DKover[counter], FDunder[counter])
                    arb.append((DKover[counter], FDunder[counter]))
                    send_sms_alert(arb_message)
                elif sum == 1/DKover[counter]+1/DKunder[counter]:
                    arb_message += f"DK over: {DKover[counter]}\nDK under: {DKunder[counter]}\n"
                    print("bet on DK over and DK under")
                    print("Bet on DK over: " + str(DKover[counter]))
                    print("Bet on DK under: " + str(DKunder[counter]))
                    profit_margin(DKover[counter], DKunder[counter])
                    arb.append((DKover[counter], DKunder[counter]))
                    send_sms_alert(arb_message)
                elif sum == 1/FDover[counter]+1/FDunder[counter]:
                    arb_message += f"FD over: {FDover[counter]}\nFD under: {FDunder[counter]}\n"
                    print("bet on FD over and FD under")
                    print("Bet on FD over: " + str(FDover[counter]))
                    print("Bet on FD under: " + str(FDunder[counter]))
                    profit_margin(FDover[counter], FDunder[counter])
                    arb.append((FDover[counter], FDunder[counter]))
                    send_sms_alert(arb_message)
                elif sum == 1/FDover[counter]+1/DKunder[counter]:
                    arb_message += f"FD over: {FDover[counter]}\nDK under: {DKunder[counter]}\n"
                    print("bet on FD over and DK under")
                    print("Bet on FD over: " + str(FDover[counter]))
                    print("Bet on DK under: " + str(DKunder[counter]))
                    profit_margin(FDover[counter], DKunder[counter])
                    arb.append((FDover[counter], DKunder[counter]))
                    send_sms_alert(arb_message)
        counter += 1
    print("Arbitrage opportunities: ", arb)

def main():
    print("Starting arbitrage checker. Press Ctrl+C to stop.")
    while True:
        try:
            print("\n" + "="*50)
            print(f"Checking odds at {time.strftime('%H:%M:%S')}")
            check_arbitrage()
            print("Waiting 20 seconds before next check...")
            time.sleep(20)
        except KeyboardInterrupt:
            print("\nStopping arbitrage checker...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            if "429" in str(e):  # Check if error is due to rate limiting
                print("API key quota exceeded, switching to next key...")
                API_KEY = get_fresh_api_key()
            print("Retrying in 20 seconds...")
            time.sleep(20)

if __name__ == "__main__":
    main()