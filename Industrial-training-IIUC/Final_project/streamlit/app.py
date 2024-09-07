import streamlit as st
import requests

# Set the base URL for your FastAPI backend
BASE_URL = "http://localhost:8001"

st.set_page_config(page_title="News Summarizer App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Welcome", "Categories", "All News", "Add News", "Summaries"])

# Welcome Page
if options == "Welcome":
    st.title("Welcome to the News Summarizer App")
    st.write("Use the navigation menu to explore different functionalities.")
    st.write("Visit [FastAPI Swagger UI](http://localhost:8001/docs) for more API details.")

# Categories Page
elif options == "Categories":
    st.title("Categories")
    categories_response = requests.get(f"{BASE_URL}/categories/")
    if categories_response.status_code == 200:
        categories = categories_response.json()
        for category in categories:
            st.write(f"Category ID: {category['id']}, Name: {category['name']}")
    else:
        st.error("Failed to fetch categories")

# All News Page
elif options == "All News":
    st.title("All News Articles")
    news_response = requests.get(f"{BASE_URL}/news/")
    if news_response.status_code == 200:
        news_articles = news_response.json()
        for news in news_articles:
            st.write(f"News ID: {news['id']}, Title: {news['title']}")
            st.write(news['content'])
            # Provide a link to fetch summary
            if st.button(f"Get Summary for News ID {news['id']}"):
                summary_response = requests.get(f"{BASE_URL}/news/{news['id']}/summary")
                if summary_response.status_code == 200:
                    summary = summary_response.json()
                    st.write(f"Summary: {summary['summary']}")
                else:
                    st.error(f"Failed to fetch summary for News ID {news['id']}")
    else:
        st.error("Failed to fetch news articles")

# Add News Page
elif options == "Add News":
    st.title("Add a New News Article")
    url_input = st.text_input("Enter the URL of the news article")
    if st.button("Add News"):
        if url_input:
            post_response = requests.post(f"{BASE_URL}/news/", json={"url": url_input})
            if post_response.status_code == 200:
                st.success("News article successfully posted!")
            else:
                st.error("Failed to post the news article")
        else:
            st.error("Please enter a URL")

# Summaries Page
elif options == "Summaries":
    st.title("All Summaries")
    summaries_response = requests.get(f"{BASE_URL}/summaries/")
    if summaries_response.status_code == 200:
        summaries = summaries_response.json()
        for summary in summaries:
            st.write(f"Summary ID: {summary['id']}, Text: {summary['text']}")
    else:
        st.error("Failed to fetch summaries")
