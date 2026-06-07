# 🤖 Axiom Trade Telegram Token Monitor

A comprehensive Telegram bot that monitors new Solana tokens from Axiom Trade and sends real-time alerts with detailed token information, including market metrics, social links, and distribution data.

## 📋 Features

- **Real-time Token Monitoring**: Connects to Axiom Trade WebSocket for instant new token alerts
- **Comprehensive Token Data**: Displays FDV, volume, holders, token age, and distribution metrics
- **Social Integration**: Includes Twitter, Telegram, and website links when available
- **Professional Formatting**: Clean, emoji-rich messages similar to popular meme coin trackers
- **Error Handling**: Robust error handling and reconnection logic
- **Status Updates**: Periodic bot status and statistics reporting
- **Easy Configuration**: Simple `.env` file configuration

## 🖼️ Message Format

The bot sends formatted messages that include:

```
💊 **TokenName** / TICKER

💰 **FDV**: $123,456.78
🌊 **Volume**: $45,678.90 USD
👥 **Holders**: 137
⚫ **Top 10**: 15.23%
📦 **Bundle**: 0.00%
🧑‍💻 **Dev**: 5.67%
🎯 **Snipers**: 1

⏰ **Token Age**: 5m

🔗 **Links**:
👨‍💻 **Dev**: `AbC123dEf456...`
🐦 **Twitter**: [Link](https://twitter.com/...)
💬 **Telegram**: [Link](https://t.me/...)
🌐 **Website**: [Link](https://example.com)

`TokenAddress123456789...`

🏭 **Protocol**: Pump.fun
```

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have Python 3.7+ installed and the Axiom Trade API properly configured.

### 2. Install Dependencies

```bash
pip install python-telegram-bot python-dotenv
```

### 3. Create a Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the instructions
3. Save your bot token (looks like `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 4. Get Your Chat ID

**For personal messages:**
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your user ID

**For channels:**
1. Add your bot to the channel as an admin
2. Send a message to the channel
3. Visit `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. Look for your channel ID (starts with `-100`)

**For groups:**
1. Add your bot to the group
2. Send a message in the group
3. Visit `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. Look for your group ID (negative number)

### 5. Configure Environment

1. Copy the template:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` with your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   TELEGRAM_CHAT_ID=123456789
   auth-access-token=your_axiom_access_token
   auth-refresh-token=your_axiom_refresh_token
   ```

### 6. Run the Bot

```bash
python telegram_token_bot.py
```

## 📁 File Structure

```
examples/
├── telegram_token_bot.py    # Main bot implementation
├── .env.template           # Environment configuration template
└── README.md              # This documentation
```

## 🛠️ Configuration Options

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | `123456789:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Target chat/channel ID for messages | `123456789` or `-1001234567890` |
| `auth-access-token` | Axiom Trade API access token | `eyJhbGciOiJIUzI1NiIs...` |
| `auth-refresh-token` | Axiom Trade API refresh token | `eyJhbGciOiJIUzI1NiIs...` |

### Optional Configuration

You can add these to your `.env` file for additional customization:

```env
# How often to send status updates (in seconds)
STATUS_UPDATE_INTERVAL=3600

# Maximum tokens to track per hour
MAX_TOKENS_PER_HOUR=100

# Minimum liquidity threshold for alerts (in SOL)
MIN_LIQUIDITY_THRESHOLD=5.0
```

## 🔧 Code Architecture

### Main Components

1. **TelegramTokenBot**: Main bot class handling all operations
2. **Token Formatting**: Converts raw token data into formatted messages
3. **WebSocket Handler**: Manages real-time token data reception
4. **Error Handling**: Comprehensive error management and logging

### Key Methods

- `format_token_message()`: Formats token data into Telegram message
- `send_token_alert()`: Sends formatted alert to Telegram
- `token_callback()`: Handles new token data from WebSocket
- `run()`: Main execution loop

## 📊 Bot Features in Detail

### Real-Time Token Monitoring

The bot connects to the Axiom Trade WebSocket endpoint and receives live updates about new Solana tokens. Each new token triggers an immediate alert.

### Comprehensive Token Information

For each token, the bot displays:

- **Financial Metrics**: FDV, volume, market cap estimations
- **Distribution Data**: Top holder percentages, dev holdings
- **Token Age**: Time since token creation
- **Social Links**: Twitter, Telegram, website when available
- **Protocol Info**: Creation protocol (Pump.fun, etc.)
- **Developer Info**: Deployer address and verification

### Professional Message Formatting

Messages are formatted with:
- Emoji indicators for quick visual scanning
- Markdown formatting for emphasis
- Clickable links for social media
- Monospace formatting for addresses
- Clean structure matching popular trackers

## 🔍 Troubleshooting

### Common Issues

**Bot not receiving messages:**
- Verify bot token is correct
- Check chat ID is correct
- Ensure bot has permission to send messages

**Authentication errors:**
- Verify Axiom Trade tokens are valid and not expired
- Check token format (should start with `eyJ`)
- Ensure tokens have proper permissions

**WebSocket connection issues:**
- Check internet connection
- Verify Axiom Trade service status
- Review bot logs for specific error messages

### Debug Mode

For detailed logging, modify the logging level in the code:

```python
logger.setLevel(logging.DEBUG)
```

This will show detailed WebSocket and API communication logs.

### Testing the Bot

1. Start the bot and verify the startup message
2. Check logs for "Connected to Axiom Trade WebSocket"
3. Monitor for new token alerts
4. Verify message formatting and links

## 🔐 Security Considerations

- Keep your `.env` file secure and never commit it to version control
- Use environment variables for all sensitive data
- Consider running the bot on a secure server
- Regularly rotate your API tokens
- Monitor bot logs for suspicious activity

## 📈 Performance

The bot is designed to handle:
- Continuous WebSocket connections
- Real-time message processing
- Multiple tokens per minute
- Automatic reconnection on failures

For high-volume usage, consider:
- Rate limiting token alerts
- Using a message queue for buffering
- Running multiple bot instances
- Implementing database logging

## 🤝 Contributing

To improve the bot:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the main project LICENSE file for details.

## 🆘 Support

For support:
1. Check this README for common solutions
2. Review the bot logs for error messages
3. Verify your configuration in `.env`
4. Check Axiom Trade API status
5. Test with a minimal configuration

## 🔗 Related Documentation

- [Axiom Trade API Documentation](../docs/)
- [WebSocket Guide](../docs/websocket-guide.md)
- [Authentication Guide](../docs/authentication.md)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## ✍️ Build These Bots Faster with ChipaEditor

**[ChipaEditor](https://chipaeditor.com/?utm_source=code&utm_medium=example&utm_campaign=axiomtradeapi&utm_term=advanced&utm_content=examples_readme)** is the AI-powered code editor made for DeFi developers. Get AI completions for Solana trading patterns, one-click bot deployment, and built-in DeFi debugging.

👉 **[Try ChipaEditor Free →](https://chipaeditor.com/?utm_source=code&utm_medium=example&utm_campaign=axiomtradeapi&utm_term=advanced&utm_content=try_free)**

## 🔗 Ready to Trade?

Deploy your bot and **[start trading on Axiom →](https://axiom.trade/@chipadev)**

---

*Built with ❤️ for the Solana community*
