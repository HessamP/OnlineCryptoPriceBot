from telegram import *  # python-telegram-bot ver 13.11 Author: Leandro Toledo
from telegram.ext import *  # python-telegram-bot ver 13.11 Author: Leandro Toledo
import datetime
import requests
import json

import key

updater = Updater(key.bot_token)
dispatcher = updater.dispatcher


def start_command(update: Update, context: CallbackContext):
    # buttons = [[KeyboardButton("hi")], [KeyboardButton("by")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Use any coin/ token symbol to get live price, for example send btc$ to have "
                                  "Bitcoin price per USD or send btceth to have Bitcoin price per Ethereum, for more options /help")


dispatcher.add_handler(CommandHandler("start", start_command))


def btc_price_command(update: Update, context: CallbackContext):
    # buttons = [[KeyboardButton("hi")], [KeyboardButton("by")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="btc$")


dispatcher.add_handler(CommandHandler("btc", btc_price_command))


#Main Code:
def symbol_to_id(symbol):
    cleaned_symbol = str(symbol).strip().lower()
    symbol_url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    id_request = json.loads(requests.get(url=symbol_url).text)
    find = {y["symbol"]: x for x, y in list(enumerate(id_request))}
    location = find[cleaned_symbol]

    coin_id = id_request[location]["id"]

    return coin_id


def rounded_thousands_seperator_usd(dollars):
    if str(dollars).lower().__contains__("e"):
        return "$" + f"{dollars :.12f}"
    else:
        return "$" + f"{round(dollars, 5):,}"


def rounded_thousands_seperator_percent(percent):
    return f"{round(percent, 2):,}" + "%"


def get_price(message):
    symbol = str(update.message.text).strip().replace("$", "")
    if 2 < len(symbol) <= 4:
        versus = "usd"
        coin_id = symbol_to_id(symbol)
        coingecko_price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={versus}&include_market_cap" \
                              "=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true "

        price_request = json.loads(requests.get(url=coingecko_price_url).text)
        price_output = price_request[coin_id]
        price = rounded_thousands_seperator_usd(price_output["usd"])
        usd_market_cap2 = rounded_thousands_seperator_usd(price_output["usd_market_cap"])
        print(price)

        usd_24h_change = rounded_thousands_seperator_percent(price_output["usd_24h_change"])
        print(usd_24h_change)

#End of Main Code




def message_handler(update: Update, context: CallbackContext):
    symbol = update.message.text



    context.bot.send_message(chat_id=update.effective_chat.id, text=get_price(update.message.text))


dispatcher.add_handler(MessageHandler(message_handler))

updater.start_polling()
