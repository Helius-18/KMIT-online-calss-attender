import time
import subprocess
import webbrowser
import schedule
import requests


def discorder(status,link):
    url = "https://discord.com/api/webhooks/850621284059840553/QBywwPw-BsvKVud2VYDIKoNM3WwJd9G3uU_T0Q1qxq1_EtfOM5SfHyfc6PPlUj9VPOzX" #webhook url, from here: https://i.imgur.com/f9XnAew.png

    data = {
        "content" : status,
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



def main(flag):
    flag+=1
    def joinclass(k):
        try:
            driver.find_element_by_link_text("JOIN").click()
            driver.switch_to.window(driver.window_handles[-1])
            opener(driver.current_url)
        except:
            print("Join button not found, trying again")
            time.sleep(1)
            driver.refresh()
            if(k<1):
                print("trying again...",k)
                k+=1
                joinclass(k)
            print("Seems like there is no class today")
            discorder("Class link not found",driver.current_url)

    def opener(link):
        link=driver.current_url
        print("Url found:  ",link)
        print("opening class...")
        webbrowser.open(link)
        time.sleep(3)
        print("closing driver...")
        print("sending msg to discord..")
        discorder("class join successfull",link)
        driver.quit()

    def installer(cmd_line):
        p = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()
        print(out)

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
        k=0
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
            discorder("Class join falied","http://kmitonline.com/login/index.php")
            driver.quit()

    print("minimizing window...")
    driver.minimize_window()
    Login()
    print("The End")




day={"mon":["09:00","11:00","14:00"],"tue":["09:00","11:00"],"wed":["09:00","11:00","14:00"],"thu":["09:00","11:00","14:00"],"fri":["09:00","11:00","14:00","15:00"],"sat":["09:00","11:00"]}
n=input("Enter day:")
i=int(input("start from which class:"))
i=i-1
start_time=day[n]

schedule.every().monday.at(start_time[i]).do(main,i)
schedule.every().tuesday.at(start_time[i]).do(main,i)
schedule.every().wednesday.at(start_time[i]).do(main,i)
schedule.every().thursday.at(start_time[i]).do(main,i)
schedule.every().friday.at(start_time[i]).do(main,i)
schedule.every().saturday.at(start_time[i]).do(main,i)

while(i<len(start_time)):
	schedule.run_pending()
	time.sleep(3)