import telebot
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

BASE = "http://127.0.0.1:5000"


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Welcome to ShopRich Bot\n"
        "/products\n"
        "/cart <id>\n"
        "/order <id>\n"
        "/myorders"
    )


@bot.message_handler(commands=["products"])
def products(message):
    response = requests.get(f"{BASE}/products")
    items = response.json()

    msg = "Products:\n\n"
    for item in items:
        msg += f"{item['id']}. {item['name']} - GHS {item['price']}\n"

    bot.reply_to(message, msg)


@bot.message_handler(commands=["cart"])
def cart(message):
    try:
        product_id = int(message.text.split()[1])

        data = {
            "username": message.from_user.username or "user",
            "product_id": product_id
        }

        requests.post(f"{BASE}/cart", json=data)
        bot.reply_to(message, "Added to cart")

    except:
        bot.reply_to(message, "Usage: /cart product_id")


@bot.message_handler(commands=["order"])
def order(message):
    try:
        product_id = int(message.text.split()[1])

        data = {
            "username": message.from_user.username or "user",
            "product_id": product_id
        }

        requests.post(f"{BASE}/order", json=data)
        bot.reply_to(message, "Order placed")

    except:
        bot.reply_to(message, "Usage: /order product_id")


@bot.message_handler(commands=["myorders"])
def myorders(message):
    username = message.from_user.username or "user"

    response = requests.get(f"{BASE}/orders/{username}")
    orders = response.json()

    if not orders:
        bot.reply_to(message, "No orders found")
        return

    msg = "Your Orders:\n\n"
    for order in orders:
        msg += f"Order #{order['id']} - Product {order['product_id']} - {order['status']}\n"

    bot.reply_to(message, msg)


bot.infinity_polling()
