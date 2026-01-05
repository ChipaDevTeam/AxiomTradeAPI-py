from axiomtradeapi.client import AxiomTradeClient

import dotenv
import os

dotenv.load_dotenv()

access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')

client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token
)

pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"
wallet_address = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"
token_ticker = "green"

token_info = client.get_token_info_by_pair(pair_address)
print(token_info)

last_tx = client.get_last_transaction(pair_address)
print(last_tx)

pair_info = client.get_pair_info(pair_address)
print(pair_info)

pair_stats = client.get_pair_stats(pair_address)
print(pair_stats)

positions = client.get_meme_open_positions(wallet_address)
print(positions)

holder_data = client.get_holder_data(pair_address, only_tracked_wallets=False)
print(holder_data)

dev_tokens = client.get_dev_tokens(dev_address)
print(dev_tokens)

token_analysis = client.get_token_analysis(dev_address, token_ticker)
print(token_analysis)

