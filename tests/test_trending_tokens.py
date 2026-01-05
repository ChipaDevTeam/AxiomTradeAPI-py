from axiomtradeapi.client import AxiomTradeClient

import dotenv
import os

dotenv.load_dotenv()

access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')

client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token,
    use_saved_tokens=True
)

trending = client.get_trending_tokens()
print(trending)