import numpy as np
import cv2 as cv
import logging

from mss.linux import MSS as mss
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

driver = webdriver.Firefox(log_path='NUL')
driver.get("https://chromedino.com/")
action = ActionChains(driver)

src = mss()
capture_box = {'left':3051,'top':284,'width':600,'height':150} #1131

font = cv.FONT_HERSHEY_SIMPLEX

while True:

  grab = src.grab(capture_box)
  cap = Image.frombytes('RGB', grab.size, grab.bgra, 'raw', 'BGRX')
  frame = np.asanyarray(cap)

  frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  placement=[]
  def detect(image, thd=0.8, colour=(0,255,255), player=False):
    template = cv.imread(image ,0)
    w,h = template.shape[::-1]
    res = cv.matchTemplate(frame_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = thd
    loc = np.where( res >= threshold )
    for pt in zip(*loc[::-1]):
      cv.rectangle(frame, pt, (pt[0] + w, pt[1] + h), colour, 2)
      cv.putText(frame,image,(w,h),font,1,colour,2,cv.LINE_AA)
      if player != True:
        placement.append((image,pt[0],pt[1]))

  #detect('player.png', 0.71, (108,105,255), True)

  detect('k.png', 0.88, (10,154,9))
  detect('lk.png', 0.9, (20,144,10))
  detect('2k.png', 0.8, (210,44,80))
  detect('3k.png', 0.8, (210,210,20))
  detect('4k.png', 0.8, (77,44,188))

  detect('bird.png', 0.7, (44,41,255))

  placement = sorted(placement, key=lambda x: x[1], reverse=False)

  try:

    if placement[0][1] < 140 and placement[0][0] == "k.png" \
        or placement[0][0] == "lk.png" and placement[0][1] < 140 \
        or placement[0][0] == "bird.png" and placement[0][1] < 145 and placement[0][2] > 113 \
        or placement[0][0] == "2k.png" and placement[0][1] < 132:
      action.send_keys(u'\ue00d').perform()

    elif placement[0][1] < 126 and placement[0][0] == "3k.png" \
        or placement[0][0] == "4k.png" and placement[0][1] < 129:
      action.send_keys(u'\ue013').perform()

    elif placement[0][1] < 100 and placement[0][0] == "bird.png" and placement[0][2] < 113:
      action.send_keys(u'\ue015').perform()

  except:pass

  cv.imshow("Detected", frame)

  if cv.waitKey(1) & 0xFF == ord('q'):
    break

cv.destroyAllWindows()
driver.close()
