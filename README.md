# My_Doctor(tabibi)
"A  simple web app to make booking appointment easy for patients "

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Authors](#authors)

## Installation

1. Clone the repo:
    `git clone https://github.com/abdelkaderbelkacemi13/my_doctor.git`
    then
    `cd my_doctor`
2. Since the project requires a databse you must have MySQl installed in you system,
   if not follow this [guide](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/)
   then run:
     `cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p`
   put your mysql password at the prompt.
3. Start a virtual env. Download it using:
     `python3 -m venv venv`
4. Activate the virtual env:
   `source venv/bin/activate`
   Once you have activated it, your bash prompt should have a preceeding (venv) at the beginning.
5. Install the requirements:
    `pip install -r requirements.txt`
after the installation is successful:
6.  run `cd app`
7.  run `flask run` to start the application.

## usage
after the app run successfully, copy the url you have something like this `http://127.0.0.1:5000`
and open it in your browser and will get to the web app home page.

## contributing:
1. Fork the project. 
2. Creat a new branch with the name of the feature.
3. Submit a Pull request.

## Authors:
Reach out to [@Abdelkader Belkacemi](https://www.linkedin.com/in/abdelkaderbelkacemi/)
Reach out to[@Austin Muthoni](https://www.linkedin.com/in/austin-nganga/)
