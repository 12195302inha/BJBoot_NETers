import datetime

from selenium import webdriver
from pathlib import Path

import yaml
import os

if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    YAML_PATH = os.path.join(BASE_DIR, 'accounts.yaml')
    RESULT_PATH = os.path.join(BASE_DIR, '네터스 백준 인증 {0}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")))
    DRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver.exe')

    URL = 'https://www.acmicpc.net/group/member/10895'

    with open(YAML_PATH, encoding='UTF8') as y:
        accounts = yaml.load(y, Loader=yaml.FullLoader)

    member_list = []

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_start = yesterday.replace(hour=0, minute=0, second=0)
    yesterday_end = yesterday.replace(hour=23, minute=59, second=59)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    driver.implicitly_wait(30)

    driver.get(url=URL)

    for account in accounts:
        f = open(RESULT_PATH, 'a')
        f.write("이름: {0}, 아이디: {1}\n".format(accounts[account], account))
        solve_count = 0
        problem_number = []

        # member click
        member_tag = driver.find_element_by_xpath("//a[contains(@href,'/user/{0}')]".format(account))
        member_tag.click()

        # 맞았습니다 click
        solve_problem = driver.find_element_by_id("u-result-4")
        solve_problem.click()

        # 각 문제 가져오기
        problems = driver.find_elements_by_xpath(".//tr[contains(@id, 'solution')]")
        for problem in problems:
            # 문제의 solve time 가져오기
            problem_solve_time_tag = problem.find_element_by_xpath(
                ".//a[contains(@class, 'real-time-update show-date')]")
            problem_solve_time = problem_solve_time_tag.get_attribute("data-original-title")

            # solve time 계산하기
            solve_time = datetime.datetime.strptime(problem_solve_time, "%Y년 %m월 %d일 %H:%M:%S")
            if yesterday_start < solve_time < yesterday_end:
                # 해당 문제 정보 가져오기
                problem_info = list(map(str, problem.text.split()))

                # 제출 번호와 문제만 가져오기
                problem_info = [problem_info[0], problem_info[2]]

                # 겹치는 문제 제거
                if problem_info[1] not in problem_number:
                    problem_number.append(problem_info[1])
                    solve_count += 1
                    f.write('제출 번호: {0}, 문제: {1}\n'.format(problem_info[0], problem_info[1]))

        f.write("총 개수: " + str(solve_count) + "\n\n")
        f.close()
        driver.get(url=URL)

    driver.quit()
