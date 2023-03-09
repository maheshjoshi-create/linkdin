# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:46:12 2023

@author: user
"""

import pandas as pd


# import os
# from glob import glob
import os, glob



from datetime import date
import time
from datetime import datetime,timedelta

# import os
# from glob import glob

from selenium.webdriver.common.by import By

today = date.today()
from Send_Email import send_the_data



def extract_data(domain_name,location,driver,duration):
    print('-'*50)
    # domain_name = "ElectroNeek, Blue Prism"
    # location = 'Denmark'
    # ["United States", "United Kingdom", "Norway", "France", "Sweden",
    # "Denmark", "Australia"]
    # domain_name = domain_name_list[0].strip()
    # location = locations[0].strip()
    # wait = WebDriverWait(driver, 25)
    # driver.get("https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=artificial%20intelligence&location=United%20States")
    try:
        # domain_name = "tosca"
        # location = 'canada'
        print(f"Execution start and domain name is {domain_name}")
        driver.get("https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=artificial%20intelligence&location=United%20States")
# #jobs-search-box-keyword-id-ember354 /html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]
        time.sleep(5)
        # JOB SEARCH INPUT FIELD
        driver.find_element(By.XPATH,"//input[@aria-label='Search by title, skill, or company']").clear()
        driver.find_element(By.XPATH,"//input[@aria-label='Search by title, skill, or company']").send_keys(domain_name)#("UiPath")#
        # LOCATION SEARCH INPUT
        driver.find_element(By.XPATH,"//input[@aria-label='City, state, or zip code']").clear()
        driver.find_element(By.XPATH,"//input[@aria-label='City, state, or zip code']").send_keys(location)#("India")#
        time.sleep(5)
        #COLLECTION SEARCH BAR WHICH CONTAIN SEARCH BUTTON
        search_box = driver.find_element(By.CLASS_NAME,'jobs-search-box')
        search_box.find_element(By.TAG_NAME,'button').click()
        time.sleep(5)
        #COLLECTION OF NAV BAR WHICH CONTAIN DATE POSTED FILTER
        filter_box = driver.find_element(By.XPATH,"//section[@aria-label='search filters']")
        tf = filter_box.find_elements(By.TAG_NAME,'li')
        for i in range(len(tf)):
            if tf[i].text.lower() == 'Date Posted'.lower():
                tf[i].click()
                break
            

        store = driver.find_element(By.ID,'hoverable-outlet-date-posted-filter-value')
        time.sleep(7)
        #duration
        if duration =="24 hrs":
        #     #PAST 24 HOURS
           # store.find_element(By.XPATH,"//*[text()='Past 24 hours']").click()
           store.find_element(By.XPATH,"//*[text()='Past 24 hours']").click()
        elif duration =="past week":
            #PAST WEEK
            store.find_element(By.XPATH,"//*[text()='Past week']").click()
        
        elif duration =="past month":
            #PAST MONTH
            store.find_element(By.XPATH,"//*[text()='Past month']").click()
        else:
            pass
        
        # TIME FILTER OKAY BUTTON
        # store.find_element(By.XPATH,"//button[@data-control-name='filter_show_results']").click()
       
        show_button = store.find_elements(By.TAG_NAME,"button")
        show_button[-1].click()
        time.sleep(5)
        
        try:
            nojob= driver.find_element(By.CLASS_NAME,"jobs-search-no-results-banner")
            nojob.find_element(By.XPATH,"//*[text()='No matching jobs found.']")
            return pd.DataFrame()
        except:
              print("No element Found")
            
        
        print("Extracting jobs......")
        for i in range(0,10):
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          # to scroll at first position
            
       
        for _ in range(0,10):
            time.sleep(1)
            fBody = driver.find_element(By.CLASS_NAME,"jobs-search-results-list")
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                fBody)        
        try:
            temp_page = driver.find_element(By.XPATH,"//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']").text
            temp_page = temp_page.split()
            page_num = int(temp_page[-1])
        except:
            page_num = 2
        list_items = driver.find_elements(By.CLASS_NAME,"occludable-update")
        
        loc_list=[];company_list=[];job_title_list=[];state=[];jobs_desc_list=[];date_time_list=[]
        current_url=[];senior=[];emp_type=[];ind=[];page_number_list=[]
     # initialize lists
        seniority_level = ['Internship','Entry level','Associate','Mid-Senior level','Director','Executive']
        empl_type =['Full-time','Part-time','Contract','Temporary','Volunteer','Internship','Other']
        # if page_num>10:
        #     page_num = 10
        flags = False;flags_2=False
     
        for page_num_i in range(2,page_num+1):
            for _ in range(0,10):
                time.sleep(1)
                fBody = driver.find_element(By.CLASS_NAME,"jobs-search-results-list")
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                    fBody)
    
            list_items = driver.find_elements(By.CLASS_NAME,"occludable-update")
                    
    
            time.sleep(2)
                        
            for job in list_items:
                if job.text !='':
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", job)
                        time.sleep(2)
                        job.click()
                        time.sleep(2)
                        try:
                            time.sleep(2)
                            link = driver.find_element(By.CLASS_NAME,'jobs-unified-top-card__content--two-pane')
                            time.sleep(2)
                        except Exception as e:
                            print(e)
                            flags = True
                            driver.back()
                            pass
                    except Exception as e:
                        print(e)
                        pass
         
                    try:
                        try:
                            time.sleep(2)
                            type_job = link.text.split('\n')[2]
                            type_job = type_job.split(' · ')
                            s = type_job[-1]
                          
                            e = type_job[0]
                            if s in seniority_level: pass
                            else: s= "Not Present"
                            
                            if e in empl_type: pass
                            else: e= "Not Present"
                        except:
                            s= "Not Present"; e= "Not Present"
    
                        try:
                            type_job = link.text.split('\n')[3].split(' · ')
                            ind1 = type_job[-1]
                            if 'employees' not in ind1: pass
                            else:ind1= "Not Present"
                        except:
                            ind1= "Not Present"
                        
                        time.sleep(1)
                        
                        time.sleep(2)
                        try:
                            a=link.find_element(By.TAG_NAME,'a').get_attribute('href')
                            d = job.find_element(By.TAG_NAME,'time').get_attribute('datetime')
                        except:
                            d = 'Not Present'; a = 'Not Present'
                            print("date not present")
                       
                        time.sleep(1)
                        details = driver.find_element(By.ID,"job-details").text
                        time.sleep(1)
                        [position, company, location_temp] = job.text.split('\n')[:3]
                    except Exception as er:
                        print(er)
                        driver.back()
                        pass
                        break
                    
                    
                    senior.append(s)
                    emp_type.append(e)
                    ind.append(ind1)
                    current_url.append(a)
                    date_time_list.append(d)            
                    
                    
                 
        
                    job_title_list.append(position)
                    loc_list.append(location_temp)
                    company_list.append(company)
                    jobs_desc_list.append(details)
                    page_number_list.append(page_num_i -1)
            if flags == True: break
            #if flags_2 == True: break
            # time.sleep(20)
            try:
                # for i in range(0,10):
                #     time.sleep(2)
                #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # wait.until(EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Page {page_num_i}"]'))).click()
                time.sleep(5)
                driver.find_element(By.XPATH,f"//button[@aria-label='Page {page_num_i}']").click()
                print(f"page number {page_num_i -1} is executed properly")
                # page_num_c = driver.find_element_by_xpath("//section[@aria-label='pagination']").text
                # print("Page number capture sucessfully",page_num_c) 

            except Exception as e:
                print(f"page number {page_num_i - 1} is halted an error")
                print("Error in page number selections as ----->",e)
                pass
    
        # extract city frim location list
        
        city = [x.split(',')[0] for x in loc_list]
         
        # extract state from lication list 
        for loc in loc_list:
            try:
                s= loc.split(',')[1]
                state.append(s)
            except:
                state.append("Not Present")
                pass
        
                
        # create dataframe frame
        main_data = pd.DataFrame({"Domain Name": domain_name.title() ,'Job Title':job_title_list,'Page Link':current_url,
                               "Company":company_list,'City':city,'State':state,'Country':location,
                               "Posted Date":date_time_list,'Job Description': jobs_desc_list,
                               'Seniority level':senior,'Employment type':emp_type,
                               'Industries':ind, "page_number":page_number_list})
         
        # main_data.to_csv(f"Linkedin_Job_Today_{domain_name.title()}.csv", index = False)
        # print("csv...created..........")
        date_time=datetime.now()
        time_diff=timedelta(days=15,hours=0,minutes=0)
        req_date_time=date_time-time_diff
        req_date_time=req_date_time.strftime('%Y-%m-%d')
        
        temp_scrap_data = main_data.copy()
        
        filtered_df = temp_scrap_data.loc[(temp_scrap_data['Posted Date'].astype('str') >= req_date_time)]
        filtered_df=filtered_df.sort_values(by='Posted Date',ascending=False)
       
        
        #filtered_df.to_csv("Linkedin_Job_Today_temp.csv", index = False)
        return main_data
# except:
#       print("No element Found")

    except Exception as e:
                print(f"NO DATA IS FOUND FOR domain_name-> {domain_name} and locations-> {location}")
                columns_name = ['Job Title','Page Link',"Company",'City','State','Country',"Posted Date",'Job Description',
                'Seniority level','Employment type','Industries']
                main_data = pd.DataFrame(columns= columns_name)
                print("The Error is --->>", e)
                pass                    
            
                return main_data
       
def linkedin_output(driver,domain_name_list,locations,mail_id,duration):
    # domain_name_list = []
    # with open('Linkdin_code/domain.txt') as f:
    #     for dom in f:
    #         if dom:
    #             dom = dom[:-1].replace(',','')
    #             domain_name_list.append(dom)
   # domain_name_list=['Tosca','Uipath']
   # locations = ['canada','United States',]
   # with open('domain.txt') as f:
   #     dom = f.readline()
   # domain_name_list = dom.split(',')
   # location_list = []
   
   # with open('locations_list.txt') as f:
   #     loc = f.readline()
   # locations = loc.split(',')
   

   all_dd = pd.DataFrame()
   # duration =1
   curr = os.getcwd()  
   dir_data = curr+'\\Log_files'
   filelist = glob.glob(os.path.join(dir_data, "*"))
   for f in filelist:
       os.remove(f)


   curr = os.getcwd()
   if not os.path.exists(curr+'\\Log_files'):
       # os.chdir(curr)
       os.makedirs(curr+'\\Log_files')
   save_dir = curr+'\\Log_files'
   os.chdir(save_dir)
   for location in locations:
       
       for domain_name in domain_name_list:
           print(domain_name.strip(),location.strip())
           dd = extract_data(domain_name.strip(),location.strip(),driver,duration)
           if dd.shape[0]>0:
               all_dd = pd.concat([all_dd,dd],ignore_index = True)
               
               
               file_name =  'data_scrap'+today.strftime("%d_%m_%Y")+'.csv'
               
               # file_name= "data_scrap.csv"
               all_dd.to_csv(file_name,index=False)
           else: 
              print('Job not found for ', domain_name)
   
    
   # dir_data = curr+'\\Linked_in_job_output'
   # filelist = glob.glob(os.path.join(dir_data, "*"))
   # for f in filelist:
   #     os.remove(f)
       

   # curr = os.getcwd()
   # if not os.path.exists(curr+'\\Linked_in_job_output'):
   #     # os.chdir(curr)
   #     os.makedirs(curr+'\\Linked_in_job_output')
   # save_dir = curr+'\\Linked_in_job_output'
   # os.chdir(save_dir)
   # save_file_name =  'Linkedin_Job_'+today.strftime("%d_%m_%Y")+'.csv'
   # all_dd.to_csv(save_file_name,index=False)
   # filename = save_dir+'\\'+save_file_name
   os.chdir(curr)
   sender_list = []
   sender_list=mail_id.split(' ')
   # with open(r'C:\Users\user\Downloads\Linkdin_code\Linkden_code/sender_list.txt') as f:
   #      s_l = f.readline()
   # sender_list = s_l.split(',')
 
   receiver_email=''
   receiver_email = ','.join(sender_list)
    #=======================MAIL_CONTENT======
   dom_str = ""
   for ind,i in enumerate(domain_name_list):
       dom_str +=str(ind+1)+". "+i+"\n"
   
       loc_str = ""
   for ind,i in enumerate(locations):
        loc_str +=str(ind+1)+". "+i+"\n"

   mail_content = f"""Hi, \nPlease find the attachment.\n\nAttached excel data contains following Technologies:\n{dom_str.title()}
    \n and Location/s are :\n {loc_str.title()}\n\n
    Thanks and Regards
    Data Analytics Team
    """
   send_the_data(receiver_email,save_dir,file_name,curr,mail_content)
   print('mail sent successfully')
   driver.close()