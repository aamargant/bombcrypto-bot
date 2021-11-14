from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time
import os
import yaml
import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


headers = {
    'authority': 'plausible.io',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'content-type': 'text/plain',
    'accept': '*/*',
    'sec-gpc': '1',
    'origin': 'https://mpcabete.xyz',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://mpcabete.xyz/',
    'accept-language': 'en-US,en;q=0.9',
}

data = '{"n":"pageview","u":"https://mpcabete.xyz/bombcrypto/","d":"mpcabete.xyz","r":"https://mpcabete.xyz/","w":1182}'

response = requests.post('https://plausible.io/api/event', headers=headers, data=data)

if __name__ == '__main__':

    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)
    
ct = c['trashhold']

pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0

go_work_img = cv2.imread('targets/go-work.png')
commom_img = cv2.imread('targets/commom-text.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
sign_btn_img = cv2.imread('targets/select-wallet-2.png')
new_map_btn_img = cv2.imread('targets/new-map.png')
full_img = cv2.imread('targets/is-full.png')
server_overload_img = cv2.imread('targets/server_overload.png')
coins_img = cv2.imread('targets/coins.png')
legend_hero_img = cv2.imread('targets/legend_hero.png')
rare_hero_img = cv2.imread('targets/rare_hero.png')
common_hero_img = cv2.imread('targets/commom-text.png')





def start(update, context):
    update.message.reply_text('Welelcome to the bomb crypto bot!')
    main(update)

def clickBtn(img,name=None, timeout=3, trashhold = ct['default']):
    if not name is None:
        print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, trashhold=trashhold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    print('timed out')
                return False
            # print('button not found yet')
            continue

        x,y,w,h = matches[0]
        pyautogui.moveTo(x+w/2,y+h/2,0.5)
        pyautogui.click()
        return True

def printSreen():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        #sct_img = np.array(sct.grab(monitor))
        sct_img = np.array(sct.grab(sct.monitors[0]))
        return sct_img[:,:,:3]

def positions(target, trashhold=ct['default']):
    img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= trashhold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():

    commoms = positions(commom_img, trashhold = ct['commom'])
    if (len(commoms) == 0):
        print('no commom text found')
        return
    x,y,w,h = commoms[len(commoms)-1]
    print('moving to {},{} and scrolling'.format(x,y))
    pyautogui.moveTo(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-340,duration=1)

def checkCoin(update):
    if clickBtn(coins_img, name='checkCoins', timeout = 2):
        update.message.reply_text('COINS:')
        img = pyautogui.screenshot()
        img.save(r'remove.png')
        update.message.bot.send_photo(update.message.chat.id, open('remove.png', 'rb'))
        os.remove('remove.png')
        clickBtn(x_button_img)
    
def clickButtons(update):
    buttons = positions(go_work_img, trashhold=ct['go_to_work_btn'])
    full = positions(full_img, trashhold=ct['go_to_work_btn'])
    common = positions(common_hero_img, trashhold=ct['go_to_work_btn'])
    rare = positions(rare_hero_img, trashhold=ct['go_to_work_btn'])
    legend = positions(legend_hero_img, trashhold=ct['go_to_work_btn'])
    #print('buttons: {}'.format(len(buttons)))
    #print('full: {}'.format(len(full)))
    for (fx, fy, fw, fh) in full:
        for (x, y, w, h) in buttons:
            print('full fx= {} fy= {} fw= {} fh= {} / work x= {} y= {} w= {} h= {}'.format(fx, fy, fw, fh, x, y, w, h))
            if (fy + 4 == y or fy + 5 == y):
                print()
                #print('IN')
                # when click maybe the server says is overload, fix it
                pyautogui.moveTo(x+(w/2),y+(h/2),1)
                pyautogui.click()
                global hero_clicks
                hero_clicks = hero_clicks + 1
                if clickBtn(server_overload_img, name='server_overload', timeout = 3):
                    clickBtn(x_button_img, name='server_overload', timeout = 8)
                    print()
                    time.sleep(11)
                update.message.reply_text(str(hero_clicks) + ' heroes sent to work so far')

                #for (cx, cy, cw, ch) in common:
              #       print('commonx= {} y= {} w= {} h= {} '.format(cx, cy, cw, ch))

              #  for (rx, ry, rw, rh) in rare:
             #        print('rare: +rx, ry, rw, rh'.format(rx, ry, rw, rh))

             #   for (lx, ly, lw, lh) in legend:
             #        print('legend: +lx, ly, lw, lh'.format(lx, ly, lw, lh))
                #print('{} heroes sent to work so far'.format(hero_clicks))
           # else:
                #print('OUT')

def goToGame():
    clickBtn(x_button_img)
    clickBtn(teasureHunt_icon_img)

def login(update):
    global login_attempts

    if login_attempts > 3:
        print('too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.press('f5')
        return

    update.message.reply_text('Connecting wallet...')
    if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout = 3):
        print('connect wallet button clicked')

    if not clickBtn(select_metamask_no_hover_img, name='selectMetamaskBtn'):
        print('SDGFH;MDGNFSBADEGG')
        if clickBtn(select_wallet_hover_img, name='selectMetamaskHoverBtn', trashhold = ct['select_wallet_buttons'] ):
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            print('sleep in case there is no metamask text removed')
            # time.sleep(20)
        else:
            print('sleep in case there is no metamask text removed')
            # time.sleep(20)

    if clickBtn(sign_btn_img, name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
        print('sign button clicked')
        update.message.reply_text('Loading game...')
        print('{} login attempt'.format(login_attempts))
        
def refreshHeroes(update):
    if clickBtn(hero_img, name='heroBtn', timeout=25):
        global login_attempts
        login_attempts = 0
        buttonsClicked = 2
        while(buttonsClicked > 0):
            clickButtons(update)
            scroll()
            time.sleep(4)
            buttonsClicked -= 1
        clickButtons(update)
        goToGame()
    else:
        print('Heroes button timeout')


def letsgo():
    global updater
    updater = Updater("2109978508:AAGphFKYkYOd860bKrMPX7zRh-lkVZFE9kA", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()
    updater.idle()


def main(update):
    print()
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "refresh_heroes" : 0,
    "coin" : 0
    }
    
    while True:
        now = time.time()

        if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout = 1):
            print('connect wallet button clicked')
            login(update)

        if now - last["coin"] > t['send_heroes_for_work'] * 60:
            last["coin"] = now
            print('checking the amount of coins')
            checkCoin(update)

        if now - last["heroes"] > t['send_heroes_for_work'] * 60:
            last["heroes"] = now
            print('sending heroes to work')
            clickBtn(arrow_img, name='go_back_arrow_img', timeout=1)
            refreshHeroes(update)

        if clickBtn(ok_btn_img, name='okBtn', timeout=1):
            print('ok button clicked')
            update.message.reply_text('OK button clicked')
            time.sleep(15)
            login(update)

        if clickBtn(new_map_btn_img, name='new_map', timeout=1):
            print('new map button clicked')
            update.message.reply_text('New map button clicked')

        #clickBtn(teasureHunt)
        time.sleep(15)

letsgo()