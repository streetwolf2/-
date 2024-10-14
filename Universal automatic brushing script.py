from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchFrameException, NoSuchElementException, \
    NoSuchWindowException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re

import time
from tqdm import tqdm

'''//
//                       _oo0oo_
//                      o8888888o
//                      88" . "88
//                      (| -_- |)
//                      0\  =  /0
//                    ___/`---'\___
//                  .' \\|     |// '.
//                 / \\|||  :  |||// \
//                / _||||| -:- |||||- \
//               |   | \\\  - /// |   |
//               | \_|  ''\---/''  |_/ |
//               \  .-\__  '-'  ___/-. /
//             ___'. .'  /--.--\  `. .'___
//          ."" '<  `.___\_<|>_/___.' >' "".
//         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
//         \  \ `_.   \_ __\ /__ _/   .-` /  /
//     =====`-.____`.___ \_____/___.-`___.-'=====
//                       `=---='''

print("\033[31;40m本程序仅供学习交流使用，请勿用于任何商业用途\033[0m")
print("\033[31;40m以下为注意事项！！！\033[0m")
print("\033[31;40m在程序运行期间请不要乱关闭网页，这可能导致程序找不到网页元素而报错\033[0m")

wb = webdriver.Chrome(service=Service(r"D:\tools\chromedriver.exe"))

'''
以下代码负责检测用户是否添加过cookie
'''

'''
以下代码负责在cookie.txt 添加登录后的cookie信息，以及刷新代码
'''

'''
的、以上代码负责在cookie库存储以及刷新cookie
以下代码可以正常运行，切勿修改
选择cookie登录

'''


def cookiestone(abc, modle):
    if modle == 'r':
        with open('cookie.txt', 'rb') as f:
            cookies = f.read().decode()
            print(cookies)
            return eval(cookies)
    if modle == 'w':
        if os.path.exists('cookie.txt'):
            os.remove('cookie.txt')
            print(abc)

        with open('cookie.txt', 'wb') as f:
            f.write(abc.encode())


'''
使用cookie登录模式
'''


def cookie_loging():
    cookies = cookiestone('', 'r')
    try:
        wb.get(r'https://i.istudy.szpu.edu.cn/space/index')
        for cookie in cookies:
            wb.add_cookie(cookie)
        wb.refresh()
        print('\033[1;34m——\033[0m' * 80)
        print('\033[31cookie登录成功\033[0m')
    except Exception as e:
        print(e)
        print('cookie登录失败')
        print("\33[31;40error\33[0m")
        if os.path.exists('cookie.txt'):
            os.remove('cookie.txt')
        with open("cookie.txt", 'w') as f:
            pass


'''
input-username_and_pwd和no_cookie_login是负责登录模块
'''


def input_username_and_pwd(username1):
    wb.find_element(By.ID, 'username').send_keys(username1)
    wb.find_element(By.CLASS_NAME, 'getCodeText').click()
    password1 = input('请输入验证码(不小心在页面填写了直接回车)：')
    if password1 == '':
        pass
    else:
        try:
            wb.find_element(By.ID, 'dynamicCode').send_keys(password1)
            wb.find_element(By.ID, 'login_submit').click()
            print('登录成功，开始执行刷课程序')
        except Exception as e:
            print("\33[31;40error\33[0m")
            if os.path.exists('cookie.txt'):
                os.remove('cookie.txt')
            with open("cookie.txt", 'w') as f:
                pass


'''
以下为选择不使用cookie登录的模块
'''


def no_cookie_loging(number):
    print('正在验证码手动登录')
    wb.get(r'https://authserver.szpu.edu.cn/authserver/login?service=https://istudy.szpu.edu.cn/sso/szpu')
    input_username_and_pwd(number)
    cookies = wb.get_cookies()
    WebDriverWait(wb, 10)

    print(cookies)
    cookiestone(str(cookies), 'w')


'''
让用户自己选择是否cookie登录
'''
user_re = input('是否选择cookie登录？(y/n)')
if user_re == 'y':
    cookie_loging()
elif user_re == 'n':
    print('请手动登录')
    number_3 = input('请输入手机号码')
    no_cookie_loging(number_3)

'''
以下可以为刷课的父模块
'''

print('正在爬取个人信息。')

WebDriverWait(wb, 10)

# 获取姓名以及班级
frame1 = wb.page_source

student_name = re.findall('<span class="zt_u_name">(.*?)</span>', frame1)
print('正在爬取个人信息。。。')

try:
    wb.switch_to.frame(0)
    print('第一层框架登录成功')
except NoSuchFrameException:
    print('框架未定位成功')

print('正在获取源代码')
p_source = wb.page_source

print('\033[1;34m——\033[0m' * 80)
print('欢迎' + student_name[0] + '登录系统')
time.sleep(1)
print('\033[1;34m——\033[0m' * 80)

# 开始获取课程信息


try:
    result = re.findall(r'cname="(.*?)"', p_source)
    print("以下为你的课程：")
    time.sleep(0.5)
    for result_c in result:
        print(result_c)
        time.sleep(0.1)

except Exception as e:
    print("发生错误：", e)
    result = []

print('\033[1;34m——\033[0m' * 80)


def Universal_Course_Cramming_Program(class_name_1):
    print("course_page_list...")
    try:
        element_class = wb.find_element(By.XPATH, "//a[@title='" + class_name_1 + "']")

        wb.execute_script("arguments[0].click();", element_class)
        time.sleep(5)

        all_handles = wb.window_handles

        wb.switch_to.window(all_handles[1])

        print("Number of windows:", len(all_handles))

        # 点击章节
        zhangjie = WebDriverWait(wb, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/ul[1]/li[3]")))
        zhangjie.click()

        # 切换到任务表
        wb.switch_to.frame(0)
        # print(wb.page_source)

        WebDriverWait(wb, 10)

        kc_title_list = []
        kc_list = []

        # 获取所有课程名称
        kc_name = wb.find_elements(By.CLASS_NAME, 'chapter_item')
        # print(kc_name.__len__())
        for kc in kc_name:

            kc_title = kc.get_attribute('title')
            if kc_title.strip() != '':
                kc_title_list.append(kc_title)
                kc_list.append(kc)

        # 过滤列表中的空字符串

        # filtered_list = [item for item in kc_list if item.strip() != '']
        # print(filtered_list)
        print(kc_title_list)
        print(kc_title_list.__len__())
        print(kc_list)
        print(kc_list.__len__())

        # 修改以下数字可以选择选择刷课

        '''
        以下模块负责处理视频的播放和视频进度条获取
        '''
        wait = WebDriverWait(wb, 10)

        # 开始逐个切换列表中的的视频
        def click_video_numb():  # 负责切换到视频的页面
            # wb.switch_to.frame(video_element_in_frame[NO_video])  # 通过切换不同的框架来播放网页的视频
            print('\033[1;34m——\033[0m' * 80)
            print('\033[1;34m切换视频框架成功\033[0m')

            video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
            print('查找到视频')
            # 通过javastrip滑动到元素可见
            wb.execute_script("arguments[0].scrollIntoView();", video_element)
            print('滑动完成')
            WebDriverWait(wb, 10)
            play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "vjs-big-play-button")))
            play_button.click()
            print('播放视频成功')

        def get_video_time():
            try:
                target_element = WebDriverWait(wb, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "vjs-progress-holder"))
                )
                aria_value_text = target_element.get_attribute("aria-valuetext")
                parts_time = aria_value_text.split(' of ')
                video_time_1 = parts_time[1].split()[0]
                return video_time_1
            except NoSuchElementException:
                print('视频实时时常获取错误')
            except TimeoutException:
                print('请检查您的网络')

        # 通过网页元素获取时常
        def get_video_time_ing():
            try:
                target_element = WebDriverWait(wb, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "vjs-progress-holder"))
                )
                aria_value_text = target_element.get_attribute("aria-valuetext")
                parts_time = aria_value_text.split(' of ')
                video_time_ing1 = parts_time[0].split()[0]
                return video_time_ing1
            except NoSuchElementException:
                print('视频实时时常获取错误')
            except TimeoutException:
                print('请检查您的网络')

        # 以下为获取时常模块的子模块，用于过滤未加载的时常信息，以及转换时常格式，从分钟制转换为秒制
        def Time_converter(time_str):
            if time_str == '-:-':
                print('视频时长获取失败')

            minutes, second = map(int, time_str.split(':'))
            total_seconds = minutes * 60 + second

            return total_seconds

        # 将返回的时常传递给进度条模块

        # 以下为视频进度条模块

        def video_jingdutiao():
            # 以下为进度条模块
            try:
                # 等待一段时间确保页面加载稳定
                time.sleep(2)
                total_duration_1 = get_video_time()
                timeout = 10  # 设置超时时间为 10 秒
                start_time = time.time()
                while total_duration_1 == '-:-':
                    if time.time() - start_time > timeout:
                        raise TimeoutError("无法获取视频总时长。")
                    total_duration_1 = get_video_time()
                total_duration = Time_converter(total_duration_1)
                print('总时常获取成功')
                with tqdm(total=total_duration, ncols=100) as pbar:
                    while True:
                        try:
                            current_time_1 = get_video_time_ing()
                            current_time = Time_converter(current_time_1)
                            pbar.set_description(f'视频播放时长：{current_time_1}/{total_duration_1}')
                            pbar.update(current_time - pbar.n)
                            time.sleep(1)
                            if current_time == total_duration:
                                break
                        except Exception as e:
                            print(f"获取当前播放时间出现错误：{e}")
                            break
                print('视频完成')
                wb.switch_to.parent_frame()
            except Exception as e:
                print(f"视频进度条出现错误：{e}")

        '''以下有报错'''

        def main_operation():
            try:
                # wb.find_element(By.XPATH, '//*[@id="dct3"]').click()
                '''
                判断页面是否有按钮
                '''

                shipin_button = WebDriverWait(wb, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="dct3"]')))
                if shipin_button:
                    print('找到视频按钮')
                    shipin_button.click()
                    frame_1 = wb.find_element(By.XPATH, '//*[@id="iframe"]')
                    wb.switch_to.frame(frame_1)
                    print('\033[1;34m——\033[0m' * 80)
                    print('已经切换至第2层')
                else:
                    print('视频按钮不存在')
                    all_handles = wb.window_handles
                    wb.switch_to.window(all_handles[1])
                    frame1_V = WebDriverWait(wb, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="iframe"]')))
                    wb.switch_to.frame(frame1_V)
                    print('switch_frame_complete')






            except Exception as e:
                print(f'出现错误，错误为{e}')
                print('程序正在尝试修复错误')
                print('可能当前页面并未找到视频按钮')
                all_handles = wb.window_handles
                wb.switch_to.window(all_handles[1])
                WebDriverWait(wb, 10)
                frame_1 = wb.find_element(By.XPATH, '//*[@id="iframe"]')
                wb.switch_to.frame(frame_1)
                print('\033[1;34m——\033[0m' * 80)
                print('已经切换至第2层')

            '''
            检测当前有多少个视频框架
            '''
            print('检测当前有多少个视频框架')
            # number_of_frame = wb.find_elements(By.TAG_NAME, 'iframe')
            video_element_in_frame = []
            print('\033[1;34m——\033[0m' * 80)

            number_of_frame = WebDriverWait(wb, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
            print('切换完成')
            print(number_of_frame)

            for f_n in number_of_frame:
                print(f_n)

                wb.switch_to.frame(f_n)
                print(wb.page_source)

                try:
                    webtest = WebDriverWait(wb, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))

                    print(f'框架{f_n}查找到视频')

                    video_element_in_frame.append(webtest)
                    time.sleep(2)
                    print('开始刷课')

                    click_video_numb()
                    video_jingdutiao()
                except Exception as e:

                    print('\033[1;34m——\033[0m' * 80)

                    print(f'\033[1;34m框架{f_n}未找到视频\033[0m')
                    wb.switch_to.parent_frame()

            print(video_element_in_frame)
            print(video_element_in_frame.__len__())

            print(f'播放完成到当前页面有{video_element_in_frame.__len__()}个视频')

            wb.switch_to.default_content()
            print('正在返回最上层框架')
            return_button = WebDriverWait(wb, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="contentFocus"]')))
            return_button.click()
            all_handles = wb.window_handles
            try:
                wb.switch_to.window(all_handles[1])
                wb.switch_to.frame(0)
                print(wb.page_source)

                print('框架切换完成')
            except NoSuchFrameException:
                print('框架丢失')

            time.sleep(2)

        def main():
            for n_class in range(len(kc_list)):
                print(len(kc_list))
                print(n_class)
                print(kc_list[n_class])

                # 以下为执行区
                print({n_class})
                kc_list[n_class].click()
                print('成功点击')

                all_handles = wb.window_handles
                print(f"检测到{all_handles.__len__() + 1}个窗口句柄")
                # time.sleep(1)
                # time.sleep(1)
                wb.switch_to.window(all_handles[1])
                print('切换至第二个窗口')
                print(wb.page_source)

                time.sleep(2)

                main_operation()

                print(f"{class_name_1}的第{n_class + 1}节课视频已完成")

        main()

        # 以下为获取视频实时时常模块，为进度条时常服务





    except NoSuchElementException:
        print('没找到元素')
    except TimeoutException:
        print('查找超时')
    except NoSuchFrameException:
        print('框架丢失')
    except NoSuchWindowException:
        print('\033[31;34m网页已经退出\033[0m')


Universal_Course_Cramming_Program('（专科）大学生安全教育与应急处理训练')