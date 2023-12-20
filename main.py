import csv
import requests
from time import sleep

def check_airdrop(_wallet: str, proxy: str = None):
    url = f'https://api.zkfair.io/data/api/community-airdrop?address={_wallet}'

    if proxy:
        _proxies = {
            "http": proxy,
            "https": proxy
        }
        response = requests.get(url, proxies=_proxies)
    else:
        response = requests.get(url)

    return response.json().get("community_airdrop", {})

def is_valid_value(value):
    return value not in ["0E-18", 0]

if __name__ == "__main__":
    with open("wallets.txt", "r") as file:
        wallets = [w.strip() for w in file]

    with open("proxies.txt", "r") as file:
        proxies = [p.strip() for p in file]

    with open("results.csv", "w", newline='') as csvfile:
        fieldnames = ["#", "wallet", "Polygon zkEVM reward", "Lumoz reward", "zkRollups reward"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, wallet in enumerate(wallets):
            try:
                response_data = check_airdrop(wallet, proxies[i] if i < len(proxies) else None)

                # Обработка response_data
                polygon_zkevm_data = response_data.get("Polygon zkEVM", {})
                lumoz_data = response_data.get("Lumoz", {})
                zkrollups_data = response_data.get("zkRollups", {})

                data = {
                    "#": i + 1,
                    "wallet": wallet,
                    "Polygon zkEVM reward": polygon_zkevm_data.get("value_decimal") if is_valid_value(polygon_zkevm_data.get("value_decimal")) else 0,
                    "Lumoz reward": lumoz_data.get("value_decimal") if is_valid_value(lumoz_data.get("value_decimal")) else 0,
                    "zkRollups reward": zkrollups_data.get("value_decimal") if is_valid_value(zkrollups_data.get("value_decimal")) else 0
                }

                writer.writerow(data)
                print(f"Wallet: {wallet}, Data: {data}")
            except Exception as e:
                print(f'Failed to check wallet {wallet}, reason: {e}')
            finally:
                sleep(1)
