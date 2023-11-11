# A web-based fitness tracker
#### Video Demo:  https://www.youtube.com/watch?v=df0q8MSS_Oo
#### Description:
This is a web-based fitness tracker where users can register, record their gym exercises and then access the information. Users can add the exercise name, weight used, and the number of sets and repititions. This information is displayed back to the user and can be searched.

The web page has been developed using Flask on python. Data is stored in Sqlite3. There are three sql tables - one tracking users, one tracking each exercise session and one tracking each individual exercise. I felt this was a suitable way to seperate the training given their different frequencies (register once, exercise session once per day, multiple exercises per day).

HTML and bootstrap have been used to display data and gather user input. Javascript was used to implement the search function in the dashboard page. One of the interesting challenges in this project was development on my desktop which meant I did not rely on any cs50 assistance. 

In future I would like to develop the dashboard to track whether the user is achieving progressive overload (i.e. increasing the weight or repititions whenever they do the same exercise).

