# linkedinurl_extractor
Code to extract linkedin profile url's for leads
Linkedin_url_extractor.py - Python code to scrape linkedin URL for profile from google search 

To run the script : 
1) Save a csv file of leads data into the same root folder. The search is performed on the  'First Name'+'Last Name'+'EMAIL'+'LinkedIn'.If any value is null it will be ignored. 
   ***MAKE SURE the column names in csv match to the ones used in codes : ('First Name' , 'Last Name' , 'EMAIL') ****
2) Update the 'csv_file_path' variable to the path of where the csv file is.
3) Update the 'output_csv_file' variable to the file name and path where you want to save a new updated CSV file with 'LinkedinURL' column added.
