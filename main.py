import time
import telebot
from pars import avito_check_news_update, drom_check_news_update, avito_get_first_news, drom_get_first_news
#import warnings
#warnings.filterwarnings("ignore", message="Reloaded modules: <pars>")


def main():
    try:
        token = '5622271796:AAHCDoldrL8nJL8cXT0emla06tn_whV7ZTo'
        bot = telebot.TeleBot(token)
        CHANNEL_NAME = '@drombot22' 
        avito_get_first_news()
        drom_get_first_news()
        while True:
            avito_fresh = {}
            drom_fresh = {}
            avito_fresh = avito_check_news_update()
            drom_fresh = drom_check_news_update()
            if len(avito_fresh) != 0:
                for k, v in sorted(avito_fresh.items()):
                    news = f"АВИТО\n{v['name_m']}\n" \
                       f"{v['year']} год\n" \
                       f"{v['price']} рублей\n" \
                       f"{v['probeg']} км\n" \
                       f"{v['name_url']}\n" 
                    bot.send_message(CHANNEL_NAME, news)
            if len(drom_fresh) != 0:
                for k, v in sorted(drom_fresh.items()):
                    news = f"ДРОМ\n{v['name']}\n" \
                       f"{v['year']} год\n" \
                       f"{v['price']} рублей\n" \
                       f"{v['name_url']}\n" 
                    bot.send_message(CHANNEL_NAME, news)
            time.sleep(30)
    except:
        main()
        
        
        
if __name__ == '__main__':
    main()