#### Installing packages

```python
pip3 install -r requirements.txt
```

#### Run the code

Download all files to your computer.

Three are three .py files for task1, task2 and task3 respectively. Task1 and task2 are integrated into task3.py

run task3.py from terminal

```python
python3 task3.py
```

The app address is 127.0.0.1:5000, access it in the browser and you will recieve a hello message.

#### Task 1

Access 127.0.0.1:5000/fetch_profile for task1. It will open a web driver and start crawling some people's profile related to the keyword 'people' automatically. 

It will login with my own LinkedIn account and password. You can change the account, password and the search keyword in task1.py. The crawling will take around 10 mins. 

The information will be saved in 'test_data.json' and there is a more visible file named 'test_data_visual.json'. 

These profiles will be ranked by their personal home page in alphabet order. The ranked profiles are saved in '100_info.json'.

You can find certain person's profile via '127.0.0.1:5000/show_profile/<id>' where id is from 0 to 99

#### Task 2

Access 127.0.0.1:5000/cluster for task2. And it will show a simple graph clustered by 'education' and 'skill' section in their profiles.

