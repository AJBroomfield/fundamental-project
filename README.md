# DnD Dice Storage
## Introduction
The overall objective of this project is to create a CRUD application with utilisation of supporting tools, methodologies and technologies that encapsulate all core modules covered during training.  
The application must meet the following requirements:
* Trello Board
* Relational Database with ERD
* Functioning CRUD application created in Python
* Functioning front-end website using Flask
* Detailed Risk Assessment
* Autmated Tests
* Version Control System
## My Application
I decided to make and application for DnD players to store simple character stats and log their dice rolls. For the application to have complete CRUD functionality it needed to include the following features: 
* Create
  * Character
    * Name
    * Level
    * Race
  * Roll
    * Dice value
    * Dice result
* Read
  * View all characters on the index page
  * viewindividual player stats on their summary page
* Update
  * Change a character's level
* Delete
  * Remove rolls
  * Remove characters
   
## Database Structure

![ERD_V1](https://i.imgur.com/xhW3PyL.jpg)

The image above shows the entity relationship diagram (ERD) of the initial database structure which included three tables and allowed users to login to the application and view their own data. However, a user table was not required for the MVP (Minimal Viable Product) so was not included in the first scrum. 

![ERD_V2](https://i.imgur.com/8llbl6z.jpg)

The database structure implemented in the first scrum is shown by the ERD directly above, it follows a similar structure to my initial design but removes user table. This one-to-many relationship allows users to input their own simple character sheet and then assign dice rolls to that character.  

## Continous Integration

![CI_PIPELINE](https://i.imgur.com/ydgQk7W.jpg)

The diagram above shows the details of the continuous integration pipeline that I implemented, this helped speed up the development-to-deployment process. In my case as code is modified and added to the git repository, Jenkins will pull from here and run unit and integration tests and output their results. These results can then be implemented into the next iteration of code. Once the conditions for the MVP is met, the application is then ran on a VM (Virtual Machine) using Gunicorn which acts as a Web Server Gateway Interface (WSGI) allowing the user to access the application.  

## Risk Assessment
Before starting this project, I completed a risk assessment covering the risks which could occur when completing this project. 

![RISK](https://i.imgur.com/Cq6O8Mp.jpg)
Full risk assessment can be found [here](https://qalearning-my.sharepoint.com/:x:/r/personal/abroomfield_qa_com/Documents/Fundament%20Project%20Documents/Fundamental%20Project%20Risk%20Assessment%20Altered.xlsx?d=we1b2325c19ee4470854f543061f6309c&csf=1&web=1&e=0pRMUb)

As project was in development additional risks were discovered and were added to the bottom of the list. These are highlighted in grey. Each risk required a description, evaluation, likelihood, impact level, responsibility, response, and control measures. As the project went through its development cycle each risk was considered and their control measures were followed.

## Planning
A Trello board helped me visualise user stories, and from which allowed me to generate tasks. With each task, MoSCoW prioritisation was applied with the ‘Must Have’ tasks being required for the MVP. Each of these tasks included a checklist which covered that each feature was coded, implemented in html, and tested. Once all of these were completed it became the definition of done and was moved into the completed board.  

![TRELLO_P1](https://i.imgur.com/y2BJXQk.jpg)
![TRELLO_P2](https://i.imgur.com/UvoGRdZ.jpg)

The two images above show the status of the Trello board from before and after the first scrum was completed. For further details, here is a link to the [Trello Board](https://trello.com/b/yKIxy4Zh/agile-sprint-board)

## Testing

Throughout the development of this application a mixture of unit and integration testing these are both done using pytest. Both tests are run automatically using Jenkins whenever it detects an update to the git repository via a webhook.  

The following code is ran in Jenkins which runs both tests and output the results in its console.  

> #!/bin/bash 
>
> sudo apt-get update 
> sudo apt-get install python3 python3-venv python3-pip chromium-browser wget unzip -y 
> 
> version=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(chromium-browser --version | grep -oP 'Chromium \K\d+')) 
> wget https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip 
> sudo unzip chromedriver_linux64.zip -d /usr/bin 
> rm chromedriver_linux64.zip 
> 
> python3 -m venv venv 
> source venv/bin/activate 
> pip3 install -r requirements.txt 
> 
> export DATABASE_URI 
> export SECRET_KEY 
> 
> python3 -m pytest --cov=application 

Unit tests are used to analyse the effectiveness of the back-end code and allows me to see how much of the code has been covered successfully. Below shows two examples of a coverage report produced by pytest. One taken in the middle of development and one at the end showing 100% coverage.  

![PYTEST_1](https://i.imgur.com/ARzgEmy.jpg)![PYTEST_2](https://i.imgur.com/G5Haly5.jpg)

These unit tests covered that the application met the MVP and had basic CRUD functionality. An example of one of these tests is below: 

> <pre><code>class TestAdd(TestBase):  
>     def test_add_character(self):  
>         response = self.client.post(  
>         url_for('addchar'),  
>         data = dict(name='Luke Warm',level = 5,race = 'Mountain Dwarf'),  
>         follow_redirects=True  
>     )  
>     self.assertIn(b'Luke Warm',response.data)  
>     self.assertIn(b'5' ,response.data)  
>     self.assertIn(b'Mountain Dwarf',response.data) </code></pre>

Once a 100% coverage was achieved with the unit tests, I began integration testing which uses pytest-selenium. Selenium allows testing from the front-end of the application by running it and simulating the user interacting with the application. This helps to ensure it is working correctly and the user can clearly see any error messages that occur.  

An example of the test code is below 

> <pre><code> class SeleniAddChar(SeleniBase):  
> 
>    players = [('Luke Warm','2', 'Human'),('Chang Edlater', 3, 'Elf')]  
>    
>    def add_player(self, player): 
>    
>        self.driver.find_element_by_xpath('/html/body/h2[1]/a[2]').click()  
>        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys(player[0])  
>        self.driver.find_element_by_xpath('//*[@id="level"]').send_keys(player[1])  
>        self.driver.find_element_by_xpath('//*[@id="race"]').send_keys(player[2])  
>        self.driver.find_element_by_xpath('//*[@id="submit"]').click()  
>        
>    def test_create_success(self):  
>        for player in self.players:  
>            self.add_player(player)  
>            
>            self.assertIn(url_for('home'), self.driver.current_url)               
>            player_details = self.driver.find_element_by_xpath('/html/body/p[1]').text  
>            
>            self.assertIn(player[0],player_details)  
>            self.assertIn(str(player[1]),player_details)  
>            self.assertIn(str(player[2]),player_details)  </code></pre>

## Front End Design
### Home page

![HOME](https://i.imgur.com/8Ac1nhi.jpg)

The home page of the application can be reached using an empty directory or using “/home”. From this page the user can see any characters in the database and their rolls. Also contained on this page is options to add a character, add a dice roll, update the character, or view the summary page for any character.  

### Add a character

![Add a character](https://i.imgur.com/1AJeQrJ.jpg)

On this page a user can enter their basics character stats, including name, level, and race. Once clicking the add character button the user is then redirected to the homepage.  

### Add a dice roll

![Add a dice roll](https://i.imgur.com/y6WKV41.jpg)

This page a user can enter the dice roll for a character. They can choose which character, what dice and their result. Once added they remain on this page, to easily allow the user to add another result.  

### Summary Page

![Summary Page](https://i.imgur.com/oB11e5y.jpg)

The summary page allows user to view all dicer rolls, delete rolls or the entire character.

## Review

### Future Work
* Allow the user to add a random roll to their database rather than doing it themselves
* Modify the homepage to only show the past five rolls instead of them all
* Relocate the update button on the homepage to reduce clutter
* Provide a statistical review of a character's dice roll on the summary page

### Sprint Review
* Increase the number of events in a scrum to ensure a smooth workflow
* Include a design step for the front end portion of the application
* Link the Trello board with Github to allow for automation with this step of the CI pipeline
* Output Jenkin's test results automatically to an email to help speed up the CI pipeline


## Author

Andrew Broomfield
