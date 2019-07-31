#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import json
import os

def clear_html_re(src_html):
    content = re.sub(r"</?(.+?)>", "", src_html)
    # content = re.sub(r"&nbsp;", "", content)
    dst_html = re.sub(r"\s+", "", content) 
    return dst_html

def find_information(content,information):
	# find name
	basic_profile = content.find_all('section',{'class':'pv-top-card-v3 artdeco-card ember-view'})
	name_section = basic_profile[0].find_all('li',{'class':'inline t-24 t-black t-normal break-words'})
	string = str(name_section[0])
	name = clear_html_re(string)
	information['name']=name
	# career
	try:
		career_section = basic_profile[0].find_all('h2',{'class':'mt1 t-18 t-black t-normal'})
		career = str(career_section[0])
		career = clear_html_re(career)
		information['career'] = career
	except:
		pass
	# find location
	location_section = basic_profile[0].find_all('li',{'class':'t-16 t-black t-normal inline-block'})
	i = location_section[0]
	string = str(i)
	location = clear_html_re(string)
	information['location']=location
	# find profile detail
	# experience section
	try:
		experience_section = content.find_all('div',{'class':'pv-entity__position-group-pager pv-profile-section__list-item ember-view'})
		work = []
		for i in experience_section:
			exp = i.find_all('h3',{'class':'t-16 t-black t-bold'})
			work_type = clear_html_re(str(exp[0]))
			work.append(work_type)
		information['exprience'] = work
	except:
		pass
	# education section
	try:
		education_section = content.find_all('li',{'class':'pv-profile-section__sortable-item pv-profile-section__section-info-item relative pv-profile-section__sortable-item--v2 pv-profile-section__list-item sortable-item ember-view'})
		edu = []
		for i in education_section:
			educat = i.find_all('h3',{'class':'pv-entity__school-name t-16 t-black t-bold'})
			education = clear_html_re(str(educat[0]))
			edu.append(education)
		information['education'] = edu
	except:
		pass
	# skill
	try:
		skill_section = content.find_all('li',{'class':'pv-skill-category-entity__top-skill pv-skill-category-entity pb3 pt4 pv-skill-endorsedSkill-entity relative ember-view'})
		skills = []
		for i in skill_section:
			skill = i.find_all('span',{'class':'pv-skill-category-entity__name-text t-16 t-black t-bold'})
			skill = clear_html_re(str(skill[0]))
			skills.append(skill)
		information['skill'] = skills
	except:
		pass
	print(information)
	return information

def main():
	os.chmod('./chromedriver',0o755)
	diver=webdriver.Chrome('./chromedriver')
	diver.get('https://www.linkedin.com/login')
	# waiting for loading the website
	time.sleep(1)
	# login
	diver.find_element_by_id('username').send_keys('m773817988@gmail.com') # linkedin account
	diver.find_element_by_id('password').send_keys('mch6682777mch') # linkedin password
	diver.find_element_by_id('password').send_keys(Keys.ENTER)
	time.sleep(1)
	# send the query
	diver.find_element_by_tag_name('input').send_keys('people') # change the search query here
	diver.find_element_by_tag_name('input').send_keys(Keys.ENTER)
	time.sleep(1)
	diver.execute_script("window.scrollBy(0,3000)")
	time.sleep(1)
	# get all profiles in current page
	soup=BeautifulSoup(diver.page_source,'lxml')
	items=soup.findAll('li',{'class':'search-result search-result__occluded-item ember-view'})
	main_url = diver.current_url #https://www.linkedin.com/search/results/all/?keywords=people&origin=GLOBAL_SEARCH_HEADER
	n=0
	page = 1
	collection = {}
	while n<100:
		for i in items:
			info = {}
			try:
				title=i.find('div',{'class':'search-result__image-wrapper'}).find('a')['href']
				diver.get('https://www.linkedin.com'+title)
				time.sleep(1)
				info['id'] = title
				print(title)
				diver.execute_script("window.scrollBy(0,3000)")
				time.sleep(1)
				source = BeautifulSoup(diver.page_source,'lxml')
				infos = find_information(source,info)
				collection[str(n)] = infos
				n+=1
				if n>=100:
					break
			except:
				continue
		page += 1
		diver.get(str(main_url) + '&page=' + str(page))
		diver.execute_script("window.scrollBy(0,3000)")
		time.sleep(1)
		soup=BeautifulSoup(diver.page_source,'lxml')
		items=soup.findAll('li',{'class':'search-result search-result__occluded-item ember-view'})
	# save the raw data to json file
	json_str_visual = json.dumps(collection, indent=4)
	json_str = json.dumps(collection)
	with open('test_data_visual.json', 'w') as json_file:
	    json_file.write(json_str_visual)
	with open('test_data.json', 'w') as json_file:
		json_file.write(json_str)
	# rank by their ID (personal home page) in alphabet order
	arr = list(collection.values())
	arr = sorted(arr, key=lambda e: e.__getitem__('id'))
	new_dict = { i : arr[i] for i in range(0, len(arr) ) }
	new_file = json.dumps(new_dict, indent = 4)
	# save the ranked file
	with open('100_info.json', 'w') as json_file:
		json_file.write(new_file)
	diver.close()