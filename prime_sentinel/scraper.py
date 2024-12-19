# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from time import time
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

from selenium_stealth import stealth

chrome_options = Options()

# UA偽装が必要ないため削除
# chrome_options.add_argument('--headless')
# # chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1")
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://httpbin.org/user-agent")
# ua = driver.find_element(By.TAG_NAME, "body").text
# ua = ua.replace("Headless","");
# ua =  json.loads(ua)
# chrome_options.add_argument("--user-agent=%s"%ua["user-agent"])




def amazon_screenshot(driver:ChromiumDriver,asin,fileName):
    """
    現在のスクリーンショットを実行中のファイルと同じ階層に保存します

    Args:
        driver: スクリーンショットを行うSeleniumDriver
        asin: 撮影中のasin
        fileName: 拡張子を除いた保存したいファイル名
    """
    dirname = "%s/%s"%(os.path.dirname(__file__),asin)
    if not (os.path.isdir(dirname)):
        os.mkdir(dirname)
    driver.save_screenshot("%s/%s.png"%(dirname,fileName))

#move to other sellers
def other_sellers(driver:ChromiumDriver):
    """
    他の出品者一覧に移動します

    Args: 
        driver: 操作中のSeleniumDriver

    Returns:
        bool: 操作完了の如何
    """
    try:
        other_seller_box = driver.find_element(By.ID,"dynamic-aod-ingress-box")
        findSellers = other_seller_box.find_element(By.CLASS_NAME,"a-link-normal")
        findSellers.click()
        return True
    except Exception as e:
        print(e)
        return False

def screenCheck(driver:ChromiumDriver,rec=False):
    try:
        section = driver.find_element(By.ID,"all-offers-display")
        print(section.get_attribute("style"));
        if(section.get_attribute("style") == "right: -652px; display: none;"):
            raise
        return True
    except Exception as e:
        other_sellers(driver)
        sleep(4)
        if not (rec):
            return screenCheck(driver,rec=True)
        else:
            print(e)
            return False


# main(void)
if(__name__ == "__main__"):
    #path to display
    os.environ["DISPLAY"] = ":99"

    # optional auguments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument('--disable-gpu') 
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
        )
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    stealth(
        driver,
        languages=["ja", "en-US", "en"],         # ブラウザの言語設定
        vendor="Google Inc.",                    # Google Chromeのベンダー名
        platform="MacIntel",                     # Mac環境のプラットフォーム名
        webgl_vendor="WebKit",                   # WebGLベンダーとしてWebKitを指定
        renderer="WebKit WebGL",                 # WebGLレンダラーとしてWebKit WebGLを指定
        fix_hairline=True                        # 微小な描画の問題を修正
    )
    driver.set_window_size(1920,1080)
    # driver.maximize_window()
    driver.implicitly_wait(20)
    
    # テスト用asinリストの取得
    cur = Path("/Library/WebServer/Documents/Heloku/Heloku/prime_sentinel/list.csv").read_text(encoding="utf-8").split("\n")
    for i in cur:
        print(i)

        driver.get("https://amazon.co.jp/dp/%s"%i)
        
        sleep(20)
        # !!!!Wait until the rendering is completely finished!!!!
        #todo: detect rendering is finished
        # 商品トップページの撮影
        
        amazon_screenshot(driver,i,"top_page")

        #出品者一覧のアクティベート
        other_sellers(driver)
        sleep(10)
        print(screenCheck(driver))
        amazon_screenshot(driver,i,"otherSellers")

        
        # sleep(2)
        driver.quit()
    
