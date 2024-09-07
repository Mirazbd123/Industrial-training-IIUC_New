
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from database_connection import create_db_connection
from requests_html import HTMLSession
import pandas as pd 
import numpy as np

from database.news_insert import (execute_query,
                        insert_reporter, 
                        insert_category, 
                        insert_news,
                        insert_publisher,
                        insert_image,
                        insert_summary
                        )

dictionary = {}
dictionary['category'] = []
dictionary['title'] = []
dictionary['time & author'] = []
dictionary['body'] = []
dictionary['image_link'] = []
dictionary['page_link'] = []

def process_and_insert_news_data(connection,category, title, body, image_link, page_link, author,
       time_date, category_description, reporter_mail, publisher_name,
       publisher_email, publisher_phone, head_office_address, website ):
    
    try:
        # Insert category if not exists
        category_id = insert_category(connection, category, category_description)
        
        # Insert reporter if not exists
        reporter_id = insert_reporter(connection, author, reporter_mail)
        
        # Insert publisher as a placeholder (assuming publisher is not provided)
        publisher_id = insert_publisher(connection, publisher_name, publisher_email,publisher_phone,head_office_address,website,
                                        "facebook.com/dailynayadigonto" , "twitter.com/dailynayadigonto" , 
                                        "linkedin.com/dailynayadigonto" , "instagram.com/dailynayadigonto")
        
        # Insert news article
        news_id = insert_news(connection, category_id, reporter_id, publisher_id, time_date, title, body, page_link)
        
        # Insert images
        image_id = insert_image(connection, news_id, image_link)
    
    except Error as e:
        print(f"Error while processing news data - {e}")


def render_javascript(url):
    
    session = HTMLSession()
    try:
        response = session.get(url)
        # response.html.render()  # This will download Chromium if not found
        print("Rendered web page:", response.html.html)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def extract_title_link(url): #use only once
    session = HTMLSession()
    try:
        link_lists = []
        response = session.get(url)
        title_link_lead = response.html.find("div.news-caption-lead > h2 > a")
        link_lists.append(title_link_lead[0].attrs['href'])

        title_links = response.html.find("div.news-caption > h2 > a")
        for link in title_links:
            link_lists.append(link.attrs['href'])

        news_title_links = response.html.find("div.news-title > h3 > a")
        for link in news_title_links:
            link_lists.append(link.attrs['href'])
        
        return link_lists


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def extract_information(url):
    
    session = HTMLSession()
    try:
        response = session.get(url)
        dictionary['page_link'].append(url)

        # Example: Extracting category
        category = response.html.find("ol.breadcrumb > li > a")
        # for link in category:
        #     print(f"Category : {link.text} ")
        # print(f"Category : {category[2].text}\n")
        dictionary['category'].append(category[2].text)

        #Extracting Title
        title = response.html.find("h1.headline")
        # print(f"Title : {title[0].text}\n")
        dictionary['title'].append(title[0].text)

        #Extracting Time and author
        times = response.html.find("div.col-md-6 > ul.list-inline")
        # for i in times:
        #     # new_time = i.html.find('li')
        #     print(i.text)
        # print(f"Time and author : {times[2].text}\n")
        # print(len(times))
        dictionary['time & author'].append(times[2].text)

        #Extracting body
        body = response.html.find("div.news-content > p")
        # print("Body : ")
        bodyy = ''
        for i in body:
            # print(i.text)
            bodyy += i.text
        # print("\n")
        dictionary['body'].append(bodyy)

        #extracting Image source
        img = response.html.find("div.image-holder > figure.figure > img.img-responsive")
        # print(f"Image Link : {img[0].attrs['src']}\n")
        dictionary['image_link'].append(img[0].attrs['src'])
        

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def AuthorSplit(text):
    author = text.split("\n")
    return author[0].strip()

def TimeSplit(text):
    author = text.split("\n")
    return author[1].strip()

def update_trim(text):
    if text.find("আপডেট:")!=-1:
        return text.split("আপডেট: ")[1].strip()
    else:
        return text
    

def main():
    """
    Main function to execute the web scraping examples.
    """
    # print("Rendering JavaScript on a web page...")
    # render_javascript('https://www.dailynayadiganta.com/politics/857443/%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%A7%E0%A6%BE%E0%A6%A8%E0%A7%80%E0%A6%A4%E0%A7%87-%E0%A6%B6%E0%A7%87%E0%A6%96-%E0%A6%B9%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%A8%E0%A6%BE%E0%A6%B0-%E0%A6%AC%E0%A6%BF%E0%A6%B0%E0%A7%81%E0%A6%A6%E0%A7%8D%E0%A6%A7%E0%A7%87-%E0%A6%86%E0%A6%B0%E0%A7%8B-%E0%A7%AC-%E0%A6%B9%E0%A6%A4%E0%A7%8D%E0%A6%AF%E0%A6%BE-%E0%A6%AE%E0%A6%BE%E0%A6%AE%E0%A6%B2%E0%A6%BE')

    # print("\nExtracting information from a web page...")
    extract_information('https://www.dailynayadiganta.com/chattagram/858102/%E0%A6%AC%E0%A6%BE%E0%A6%9A%E0%A7%8D%E0%A6%9A%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B0-%E0%A6%A8%E0%A6%BF%E0%A7%9F%E0%A7%87-%E0%A6%95%E0%A7%8B%E0%A6%A8%E0%A7%8B%E0%A6%B0%E0%A6%95%E0%A6%AE-%E0%A6%9C%E0%A6%BE%E0%A6%A8%E0%A7%87-%E0%A6%AC%E0%A7%87%E0%A6%81%E0%A6%9A%E0%A7%87-%E0%A6%8F%E0%A6%B8%E0%A7%87%E0%A6%9B%E0%A6%BF')

if __name__ == "__main__":
    conn = create_db_connection()
    link_lists = extract_title_link("https://www.dailynayadiganta.com/")
    for i in link_lists:
        extract_information(i)
    df = pd.DataFrame.from_dict(dictionary)
    # Data preprocessing
    df['author'] = df['time & author'].apply(AuthorSplit)
    df['time_date'] = df['time & author'].apply(TimeSplit)
    df.drop(columns='time & author' , inplace=True)
    df['time_date'] = df['time_date'].apply(update_trim)
    df['category_description'] = "All news regarding " + df['category']
    df['reporter_mail'] = df['author']+"@gmail.com"
    df['publisher_name'] = "নয়া দিগন্ত"
    df['publisher_email'] = "info@nayadigonto.com"
    df['publisher_phone'] = "৫৭১৬৫২৬১-৯"
    df['head_office_address'] = "১ আর. কে মিশন রোড, (মানিক মিয়া ফাউন্ডেশন ভবন) , ঢাকা-১২০৩"
    df['website'] = "https://www.dailynayadiganta.com"

    #insert into database
    lenth = df.shape[0]
    for i in range (lenth):
        process_and_insert_news_data(conn,df['category'][i], df['title'][i],
                                  df['body'][i], df['image_link'][i], df['page_link'][i],df['author'][i],df['time_date'][i], 
                                  df['category_description'][i], df['reporter_mail'][i], df['publisher_name'][i],df['publisher_email'][i], 
                                  df['publisher_phone'][i], df['head_office_address'][i], df['website'][i])
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from database.database_connection import create_db_connection
from requests_html import HTMLSession
import pandas as pd 
import numpy as np

from database.news_insert import (execute_query,
                        insert_reporter, 
                        insert_category, 
                        insert_news,
                        insert_publisher,
                        insert_image,
                        insert_summary
                        )

dictionary = {}
dictionary['category'] = []
dictionary['title'] = []
dictionary['time & author'] = []
dictionary['body'] = []
dictionary['image_link'] = []
dictionary['page_link'] = []

def process_and_insert_news_data(connection,category, title, body, image_link, page_link, author,
       time_date, category_description, reporter_mail, publisher_name,
       publisher_email, publisher_phone, head_office_address, website ):
    
    try:
        # Insert category if not exists
        category_id = insert_category(connection, category, category_description)
        
        # Insert reporter if not exists
        reporter_id = insert_reporter(connection, author, reporter_mail)
        
        # Insert publisher as a placeholder (assuming publisher is not provided)
        publisher_id = insert_publisher(connection, publisher_name, publisher_email,publisher_phone,head_office_address,website,
                                        "facebook.com/dailynayadigonto" , "twitter.com/dailynayadigonto" , 
                                        "linkedin.com/dailynayadigonto" , "instagram.com/dailynayadigonto")
        
        # Insert news article
        news_id = insert_news(connection, category_id, reporter_id, publisher_id, time_date, title, body, page_link)
        
        # Insert images
        image_id = insert_image(connection, news_id, image_link)
    
    except Error as e:
        print(f"Error while processing news data - {e}")


def render_javascript(url):
    
    session = HTMLSession()
    try:
        response = session.get(url)
        # response.html.render()  # This will download Chromium if not found
        print("Rendered web page:", response.html.html)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def extract_title_link(url): #use only once
    session = HTMLSession()
    try:
        link_lists = []
        response = session.get(url)
        title_link_lead = response.html.find("div.news-caption-lead > h2 > a")
        link_lists.append(title_link_lead[0].attrs['href'])

        title_links = response.html.find("div.news-caption > h2 > a")
        for link in title_links:
            link_lists.append(link.attrs['href'])

        news_title_links = response.html.find("div.news-title > h3 > a")
        for link in news_title_links:
            link_lists.append(link.attrs['href'])
        
        return link_lists


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def extract_information(url):
    
    session = HTMLSession()
    try:
        response = session.get(url)
        dictionary['page_link'].append(url)

        # Example: Extracting category
        category = response.html.find("ol.breadcrumb > li > a")
        # for link in category:
        #     print(f"Category : {link.text} ")
        # print(f"Category : {category[2].text}\n")
        dictionary['category'].append(category[2].text)

        #Extracting Title
        title = response.html.find("h1.headline")
        # print(f"Title : {title[0].text}\n")
        dictionary['title'].append(title[0].text)

        #Extracting Time and author
        times = response.html.find("div.col-md-6 > ul.list-inline")
        # for i in times:
        #     # new_time = i.html.find('li')
        #     print(i.text)
        # print(f"Time and author : {times[2].text}\n")
        # print(len(times))
        dictionary['time & author'].append(times[2].text)

        #Extracting body
        body = response.html.find("div.news-content > p")
        # print("Body : ")
        bodyy = ''
        for i in body:
            # print(i.text)
            bodyy += i.text
        # print("\n")
        dictionary['body'].append(bodyy)

        #extracting Image source
        img = response.html.find("div.image-holder > figure.figure > img.img-responsive")
        # print(f"Image Link : {img[0].attrs['src']}\n")
        dictionary['image_link'].append(img[0].attrs['src'])
        

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def AuthorSplit(text):
    author = text.split("\n")
    return author[0].strip()

def TimeSplit(text):
    author = text.split("\n")
    return author[1].strip()

def update_trim(text):
    if text.find("আপডেট:")!=-1:
        return text.split("আপডেট: ")[1].strip()
    else:
        return text
    

def main():
    """
    Main function to execute the web scraping examples.
    """
    # print("Rendering JavaScript on a web page...")
    # render_javascript('https://www.dailynayadiganta.com/politics/857443/%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%A7%E0%A6%BE%E0%A6%A8%E0%A7%80%E0%A6%A4%E0%A7%87-%E0%A6%B6%E0%A7%87%E0%A6%96-%E0%A6%B9%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%A8%E0%A6%BE%E0%A6%B0-%E0%A6%AC%E0%A6%BF%E0%A6%B0%E0%A7%81%E0%A6%A6%E0%A7%8D%E0%A6%A7%E0%A7%87-%E0%A6%86%E0%A6%B0%E0%A7%8B-%E0%A7%AC-%E0%A6%B9%E0%A6%A4%E0%A7%8D%E0%A6%AF%E0%A6%BE-%E0%A6%AE%E0%A6%BE%E0%A6%AE%E0%A6%B2%E0%A6%BE')

    # print("\nExtracting information from a web page...")
    extract_information('https://www.dailynayadiganta.com/chattagram/858102/%E0%A6%AC%E0%A6%BE%E0%A6%9A%E0%A7%8D%E0%A6%9A%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B0-%E0%A6%A8%E0%A6%BF%E0%A7%9F%E0%A7%87-%E0%A6%95%E0%A7%8B%E0%A6%A8%E0%A7%8B%E0%A6%B0%E0%A6%95%E0%A6%AE-%E0%A6%9C%E0%A6%BE%E0%A6%A8%E0%A7%87-%E0%A6%AC%E0%A7%87%E0%A6%81%E0%A6%9A%E0%A7%87-%E0%A6%8F%E0%A6%B8%E0%A7%87%E0%A6%9B%E0%A6%BF')

if __name__ == "__main__":
    conn = create_db_connection()
    link_lists = extract_title_link("https://www.dailynayadiganta.com/")
    for i in link_lists:
        extract_information(i)
    df = pd.DataFrame.from_dict(dictionary)
    # Data preprocessing
    df['author'] = df['time & author'].apply(AuthorSplit)
    df['time_date'] = df['time & author'].apply(TimeSplit)
    df.drop(columns='time & author' , inplace=True)
    df['time_date'] = df['time_date'].apply(update_trim)
    df['category_description'] = "All news regarding " + df['category']
    df['reporter_mail'] = df['author']+"@gmail.com"
    df['publisher_name'] = "নয়া দিগন্ত"
    df['publisher_email'] = "info@nayadigonto.com"
    df['publisher_phone'] = "৫৭১৬৫২৬১-৯"
    df['head_office_address'] = "১ আর. কে মিশন রোড, (মানিক মিয়া ফাউন্ডেশন ভবন) , ঢাকা-১২০৩"
    df['website'] = "https://www.dailynayadiganta.com"

    #insert into database
    lenth = df.shape[0]
    for i in range (lenth):
        process_and_insert_news_data(conn,df['category'][i], df['title'][i],
                                  df['body'][i], df['image_link'][i], df['page_link'][i],df['author'][i],df['time_date'][i], 
                                  df['category_description'][i], df['reporter_mail'][i], df['publisher_name'][i],df['publisher_email'][i], 
                                  df['publisher_phone'][i], df['head_office_address'][i], df['website'][i])