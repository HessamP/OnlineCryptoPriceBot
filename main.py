from telegram import *  # python-telegram-bot ver 13.11 Author: Leandro Toledo
from telegram.ext import *  # python-telegram-bot ver 13.11 Author: Leandro Toledo
import datetime
import requests
import json

import key

updater = Updater(key.bot_token)
dispatcher = updater.dispatcher


def symbol_to_id(symbol):
    try:  # based on API some keys are lower and some are upper case so handle this with try and except
        cleaned_symbol = str(symbol).strip().lower()
        symbol_url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
        id_request = json.loads(requests.get(url=symbol_url).text)
        find = {y["symbol"]: x for x, y in list(enumerate(id_request))}
        location = find[cleaned_symbol]

        coin_id = id_request[location]["id"]

        return coin_id
    except:
        cleaned_symbol = str(symbol).strip().upper()
        symbol_url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
        id_request = json.loads(requests.get(url=symbol_url).text)
        find = {y["symbol"]: x for x, y in list(enumerate(id_request))}
        location = find[cleaned_symbol]

        coin_id = id_request[location]["id"]

        return coin_id


def symbol_to_name(symbol):
    try:
        cleaned_symbol = str(symbol).strip().lower()
        symbol_url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
        id_request = json.loads(requests.get(url=symbol_url).text)
        find = {y["symbol"]: x for x, y in list(enumerate(id_request))}
        location = find[cleaned_symbol]

        coin_name = id_request[location]["name"]

        return coin_name
    except:
        cleaned_symbol = str(symbol).strip().upper()
        symbol_url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
        id_request = json.loads(requests.get(url=symbol_url).text)
        find = {y["symbol"]: x for x, y in list(enumerate(id_request))}
        location = find[cleaned_symbol]

        coin_name = id_request[location]["name"]

        return coin_name


def rounded_thousands_seperator_usd(dollars):
    try:
        if str(dollars).lower().__contains__("e"):
            return "$" + f"{dollars :.12f}"
        else:
            return "$" + f"{round(dollars, 5):,}"
    except:
        if str(dollars).upper().__contains__("e"):
            return "$" + f"{dollars :.12f}"
        else:
            return "$" + f"{round(dollars, 5):,}"


def rounded_thousands_seperator_percent(percent):
    return f"{round(percent, 2):,}" + "%"


def get_price(message):
    symbol = str(message).strip().replace("$", "")
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

        return symbol.title() + " - " + symbol_to_name(
            symbol) + "\n" + "Price: " + price + "\n" + "24h Change: " + usd_24h_change


def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Use any coin/ token symbol to get live price, for example send btc$ to have "
                                  "Bitcoin price per USD or send btceth to have Bitcoin price per Ethereum, for more options /help")


def help_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="It is help")


def btc_price_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="btc$")


def response(input_text):
    user_message = str(input_text).lower().strip()
    if user_message.__contains__("$"):
        print(user_message)
        return get_price(user_message)


def handle_message(update: Update, context: CallbackContext):
    text = str(update.message.text).lower()
    update.message.reply_text(str(response(text)))


dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("btc", btc_price_command))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

updater.start_polling()
