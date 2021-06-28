from setup import main
import schedule
import time



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
