import time
import User_Defined_Variables as user_variable

class Check_Crawler():
    def crawler_status(self):
        response = user_variable.GLUE_CLIENT.get_crawler(Name='CSVCrawler')
        return response['Crawler']['State']
     
    # it check if the crawler is working and waits till it is in ready state
    
    def run_crawler(self):
        print("crawler started")
        time.sleep(6)
        while self.crawler_status() != 'READY':
            time.sleep(3)
            print("crawler running")
        print("crawler completed")
