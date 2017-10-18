# coding=utf-8
import os
import re
import time
from selenium import webdriver
from urllib.request import urlretrieve 

def download_pic(weibo_id):
    path = weibo_id + '.jpg'
    driver.get('https://weibo.cn/mblog/picAll/' + weibo_id)
    try:
        pic_href = driver.find_elements_by_xpath("//a[text()='原图'] ")
        for pic in pic_href:
            pic_id = re.findall(".*u[=](.*)[&]rl.*",pic.get_attribute('href'))[0]
#           print (pic_id)
            path = weibo_id + '_' + pic_id + '.jpg'
            pic_link = 'https://ww1.sinaimg.cn/large/' + pic_id + '.jpg'
#           print (pic_link)
#           print (path)
            urlretrieve(pic_link, path)
    except:
        print ('无')

def cache_weibo(username,password,uid):
    driver.get('https://passport.weibo.cn/signin/login')
    time.sleep(1)
    driver.find_element_by_id("loginName").send_keys(username)  
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_xpath("//*[@id='loginAction']").click()
    #登陆
    time.sleep(1)
    driver.get('https://weibo.cn/' + str(uid) + '/profile')
    end_page = int(driver.find_elements_by_xpath("//*[@id='pagelist']/form/div/input[1]")[0].get_attribute('value'))
    #获取微博页面总数
    page = 1
    for page_num in range(1,end_page):
        print('page' + str(page))
        driver.get('https://weibo.cn/' + str(uid) + '/profile?page=' + str(page))
        info = driver.find_elements_by_xpath("//div[@class='c']")
        weibo_list = []
        for value in info:    
            weibo_id = value.get_attribute('id')[2:11]
            if weibo_id == "" :
                continue
            else :
                weibo_list.append(weibo_id)
        #获取当前页面所有微博的ID
        for weibo_id in weibo_list:
            print (weibo_id)
            weibo_url = 'https://weibo.cn/repost/' + weibo_id
            driver.get(weibo_url)
            if driver.page_source.find('原文评论') == -1:
                print('原创')
                download_pic(weibo_id)
            else:
                print('转发')
                source_weibo_id = re.findall(".*comment[/](.*)[#]cmtfrm\" class[=]\"cc.*",driver.page_source)[0]
                print (source_weibo_id)
                download_pic(source_weibo_id)
            #区分是否为原创微博，并找到原微博的ID
            driver.get('https://m.weibo.cn/status/' + weibo_id)
            time.sleep(5)
            pic_name = weibo_id + '.png'
            driver.save_screenshot(pic_name)
            #截图
        print('page' + str(page) +'complete')
        page = page + 1
    print ('end')
    driver.close()  
    driver.quit()
    
if __name__ == '__main__':
    driver = webdriver.PhantomJS(executable_path="E:\phantomjs-2.1.1-windows\phantomjs.exe")
    #设置环境
    username = ''
    password = ''
    #设置账号
    uid = input("userid:")
    cache_weibo(username,password,uid)