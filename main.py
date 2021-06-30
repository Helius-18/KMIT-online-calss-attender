import time
import subprocess
import webbrowser

def installer(cmd_line):
        p = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()
        print(out)

try:
    import requests
except:
    print("requests library not found")
    print("installing...requests...")
    installer("pip install requests")


try:
    import schedule
except:
    print("schedule library not found")
    print("installing...schedule...")
    installer("pip install schedule")


def discorder(status,link,tried):
    url = "https://discord.com/api/webhooks/850621284059840553/QBywwPw-BsvKVud2VYDIKoNM3WwJd9G3uU_T0Q1qxq1_EtfOM5SfHyfc6PPlUj9VPOzX" #webhook url, from here: https://i.imgur.com/f9XnAew.png

    data = {
        "content" : status,
        "content" : status+"\n"+str(tried)+" try",
        "username" : "Hori"
    }

    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "title" : "Class link",
            "url" : link
        }
    ]

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


k=1
def main():
    def joinclass(k):
        try:
            driver.find_element_by_link_text("JOIN").click()
            driver.switch_to.window(driver.window_handles[-1])
            opener(driver.current_url)
        except:
            print("Join button not found, trying again")
            time.sleep(60)
            driver.refresh()
            if(k<15):
                print("trying again...",k)
                k+=1
                joinclass(k)
            print("Seems like there is no class today")
            discorder("Class link not found",driver.current_url,k)

    def opener(link):
        link=driver.current_url
        print("opening class...")
        if "zoom" in link:
            s=link.split("#")
            link=s[0]
        webbrowser.open(link)
        print("Url found:  ",link)
        time.sleep(3)
        print("closing driver...")
        print("sending msg to discord..")
        discorder("class join successfull",link,k)
        driver.quit()


    try:
        from selenium import webdriver
    except:
        print("Selenium is not found, no prob..")
        print("Installing selenium.....")
        installer("pip install selenium")
        time.sleep(2)
        from selenium import webdriver
    else:
        print("selenium is ready")


    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver=webdriver.Chrome(ChromeDriverManager().install())
    except:
        print("driver has failed")
        print("installing webdriver_manager....")
        installer("pip install webdriver-manager")
        time.sleep(2)
        from webdriver_manager.chrome import ChromeDriverManager
        driver=webdriver.Chrome(ChromeDriverManager().install())
    else:       
        print("driver is ready...")
    
    def Login():
        try:
            driver.get("http://kmitonline.com/login/index.php")
            username="19bd1a0573"
            password="resetme@1"
            driver.find_element_by_id("username").send_keys(username)
            driver.find_element_by_id("password").send_keys(password)
            driver.find_element_by_id("loginbtn").click()
            driver.implicitly_wait(10)
            time.sleep(2)
            joinclass(k)
        except:
            print("An error has occured....so get out!!!!")
            discorder("Class join falied","http://kmitonline.com/login/index.php",k)
            driver.quit()

    print("minimizing window...")
    driver.minimize_window()
    Login()
    print("The End")


ttable={"mon":["09:05","11:05","14:05"],"tue":["09:05","11:05"],"wed":["09:05","11:05","14:05"],"thu":["09:05","11:05","14:05"],"fri":["12:43","12:44"],"sat":["09:05","11:05"]}
day=input("Enter the day:")
n=int(input("Enter the class:"))-1
for i in range (len(ttable[day])-n):
    print("class at ",ttable[day][n])
    running = True
    def test():
        global running
        running = False
        main()
        print("Stopped")
        return schedule.CancelJob
    schedule.every().day.at(ttable[day][n]).do(test)
    while running:
        schedule.run_pending()
        time.sleep(1)
    print("done")
    n+=1
