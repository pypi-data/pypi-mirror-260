import Botte

bot = Botte.Botte("5102778034:AAHKfcC9PVm_1DHlSgE7nLP-7W0aSvv_zCM")

@bot.handle_msg(commands=['start', 'help'])
def swagatam(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.handle_msg(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.runthebot()