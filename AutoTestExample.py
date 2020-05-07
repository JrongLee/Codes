import os,time
import pyautogui
import _thread
from PIL import Image
import cv2
import numpy
from io import BytesIO
from aip import AipOcr
from functools import reduce
     

class Config(object):

    def __init__(self):
        self.loop_number = 100                        # 整套动作循环的次数
        self.failsafe = True                        # GUI保险
        self.action_interval = 0.3                    # 每个模拟动作间隔的时间
        self.enable_file_storage = False            # 是否启用文件存储,点击目标位置
        self.click_positions = []
        self.file_name = "./1.txt"
        self.window_title = "MuMu模拟器"
        self.__win = None
        self.__baidu = None

    def initConfig(self):
        pyautogui.PAUSE = self.action_interval
        pyautogui.FAILSAFE = self.failsafe
            

    def start(self):
        menu = """
        =========== Menu ===========
        1.Run and collect
        2.Run and read file
        3.Run and find switch position
	4.Run and image match all position
        """
        self.activeWindow()
        while True:
            print(menu)
            res = input("Please Enter: ")
            if res.lower() == "exit":
                exit()
            if res == "1":
                self.__collect()
                _thread.start_new_thread(self.__saveToFile,())
                self.__run()
                break
            if res == "2":
                if os.path.exists(self.file_name):
                    try:
                        file = open(self.file_name, "r", encoding="UTF-8-sig")
                        filelines = file.readlines()
                        for l in filelines:
                            val = l.strip().split(",")
                            self.click_positions.append(val)

                        self.__run()                       
                    finally:
                        file.close()
                else:
                    print("File not found")
                    self.__collect()
                    _thread.start_new_thread(self.__saveToFile,())
                    self.__run()
                break
            if res == "3":
                self.findSiwtchPostion()
                self.__run()
                break
            if res == "4":
                self.findImagePosition()
                self.__run()
                break
            
    def __saveToFile(self):
        try:
            file = open(self.file_name, "w", encoding="UTF-8")
            for e in self.click_positions:
                file.write("%d,%d\n"%(e[0],e[1]))

            file.flush()
        finally:
            file.close()
        


    def __run(self):
        
        print("        =========== Run ===========")
        beginTime = time.time()
        
        mode = []
        no = 0
        globalLastClickTime = None
        for e in self.click_positions:
            mode.append({
                "x":int(e[0]),
                "y":int(e[1]),
                "index":(no * 2 + 1),
                "oldStatusText":"关闭",
                "targetStatusText": "已打开",
                "clickCount":0,
                "matchCount":0,
                "matchStatusErrorCount":0,
                "lastClickTime":None,
            })
            no = no + 1

        def _click_(e, changeStatusText=True, globalLastClickTime=None):
            if not self.__win.isActive:
                self.__win.activate()
                
            pyautogui.click(e.get("x"), e.get("y"))
            e["clickCount"] = e.get("clickCount") + 1
            cur_time = time.time()
            #
            log = "Switch-ID[%d], First click"%e.get("index") if e.get("lastClickTime") is None or globalLastClickTime is None else "Switch-ID[%d], Click count[%d], Global interval[%f], Same switch interval[%f]"%(e.get("index"), e.get("clickCount"), cur_time - globalLastClickTime, cur_time - e.get("lastClickTime"))
            print(log)

            e["lastClickTime"] = cur_time
            if changeStatusText:
                e["oldStatusText"],e["targetStatusText"] = e["targetStatusText"],e["oldStatusText"]

            return cur_time

        while reduce(lambda a,b: a + b.get("clickCount"), mode, 0) < self.loop_number:
            
            for e in mode:
                e["matchCount"] = e.get("matchCount") + 1
                
                if e.get("lastClickTime") is None:
                    globalLastClickTime = _click_(e, False, globalLastClickTime)
                else:
                    image_text = self.baiduDistinguish()
                    if image_text[e.get("index")] == e.get("targetStatusText"):
                        globalLastClickTime = _click_(e, globalLastClickTime=globalLastClickTime)
                    else:
                        e["matchStatusErrorCount"] = e.get("matchStatusErrorCount") + 1
                        #pyautogui.sleep(0.25)
                        pyautogui.sleep(0.3)

        print("        =========== End ===========")
        print("Total time: %f"%(time.time() - beginTime))
                                

    def __collect(self):
        while input("Enter any key to collect mouse posiont:") != "exit":
            self.click_positions.append(pyautogui.position())

    def activeWindow(self):
        if self.__win is None:
            wins = pyautogui.getWindowsWithTitle(self.window_title)
            if len(wins) > 0:
                self.__win = wins[0]
        
        if self.__win is not None:
            self.__win.restore()
            self.__win.activate()
        

    def findSiwtchPostion(self):
        if self.__win is not None:
            window_img = switch_img = None
            try:
                window_img = pyautogui.screenshot(region=self.__win.box)
                switch_img = Image.open("D:\\py_pro\\3.jpg")
                topleft = self.__win.topleft
                for e in pyautogui.locateAll(switch_img, window_img, grayscale=True):
                    print(e)
                    p = (topleft.x + e.left + e.width // 2, topleft.y + e.top + e.height // 2)
                    self.click_positions.append(p)
            finally:
                if window_img:
                    window_img.close()
                if switch_img:
                    switch_img.close()


    def findImagePosition(self):
        switch_img_path = "D:\\py_pro\\switch_img\\IU-CS90.png"
        main_img_path = "D:\\py_pro\\main.png"
        pyautogui.screenshot(main_img_path, region=self.__win.box).close()
        pyautogui.sleep(1)
        switch_img = cv2.imread(switch_img_path)
        main_img = cv2.imread(main_img_path)
        h, w = switch_img.shape[:2]
        
        res = cv2.matchTemplate(main_img, switch_img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.955
        loc = numpy.where(res >= threshold)
        topleft = self.__win.topleft
        
        for x,y in zip(*loc[::-1]):
            self.click_positions.append((topleft.x + x + w // 2, topleft.y + y + h // 2))

    def baiduDistinguish(self):
        if self.__win is None:
            return
        topleft = self.__win.topleft
        pos = (70 + topleft.x, 470 + topleft.y, 70, 220)

        with pyautogui.screenshot(region=pos) as src_img, BytesIO() as bytes_io:
            src_img.save(bytes_io, format="PNG")
            img_data = bytes_io.getvalue()
            res = self.__getBaiduApi().basicGeneral(img_data);
            if res:
                words = res.get("words_result")
                new_words = []
                for e in words:
                    new_words.append(e.get("words"))

                return new_words
                
                
            return []

    def __getBaiduApi(self):
        if self.__baidu is None:
            APP_ID = '18230453'
            API_KEY = '0Ta3UXtolXOejWNRyUiYsdnC'
            SECRET_KEY = '69YopBTG6YkYXGZ3nWtBbLdXRRnp2Nee'
            self.__baidu = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        return self.__baidu
            
              
        
        
        
        

def main():

    config = Config()
    config.initConfig()
    config.start()
    
        

if __name__ == "__main__":
    main()






    
