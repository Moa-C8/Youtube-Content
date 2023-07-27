from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pgm.func import *
from pgm.funcDomoticz import *
import datetime
import pytz

async def priceCrypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    today = datetime.datetime.now()
    cet = pytz.timezone('CET')
    now_cet = today.astimezone(cet)
    dat = now_cet.strftime("%Y-%m-%d-%H")
    autoInvest = ['BTC','ETH','AAVE','LINK','MATIC','SUI','LTC']

    if len(args) == 0:
        await update.message.reply_text(f'{dat}h\n{str(get_crypto_price(1))}')
    else:
        if (args[0] == 'Auto' or args[0] == 'auto'):
            await update.message.reply_text(f"{dat}h\n{str(get_crypto_price(autoInvest))}")
        else:
            try:
                await update.message.reply_text(f"{str(args[0]).capitalize()} : ${str(get_crypto_price(args[0]))} 24h : {get_exchange_rate(args[0])}")
            except:
                await update.message.reply_text("Error Try another crypto")

async def MyWallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(get_info_GSheet()))

async def light(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args

    if(len(args) == 0):
        await update.message.reply_text(str(getStatusDomo()))
    elif(args[0] == 'on' or args[0] == 'On'):
        await update.message.reply_text(str(switchLight(1,'On')))
    else:
        await update.message.reply_text(str(switchLight(1,'Off')))

async def listDomoticz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(getListDomo()))

async def pileOuFace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(pileFace()))

def main():
    # Arguments prédéfinis pour le test
    app = ApplicationBuilder().token('6332232715:AAGokeIY5X06lGY1wDQKQPrFi6Rma8UgGKs').build()

    app.add_handler(CommandHandler("pricec", priceCrypto))
    app.add_handler(CommandHandler("light", light))
    app.add_handler(CommandHandler("mywallet", MyWallet))
    app.add_handler(CommandHandler("pof", pileOuFace))
    app.add_handler(CommandHandler("domoticz", listDomoticz))

    app.run_polling()


if __name__ == "__main__":
    main()

