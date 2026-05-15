import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Web Scraper App",
    page_icon="🌐",
    layout="centered"
)

# Title
st.title("🌐 Simple Web Scraper")
st.write("Enter a website URL and scrape headings, paragraphs, and links.")

# User Input
url = st.text_input("Enter Website URL", "https://example.com")

# Scraping Button
if st.button("Scrape Website"):

    try:
        # Request Website
        response = requests.get(url)

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Headings
        headings = []
        for tag in soup.find_all(["h1", "h2", "h3"]):
            headings.append(tag.text.strip())

        # Extract Paragraphs
        paragraphs = []
        for p in soup.find_all("p"):
            paragraphs.append(p.text.strip())

        # Extract Links
        links = []
        for a in soup.find_all("a"):
            href = a.get("href")
            if href:
                links.append(href)

        st.success("Website Scraped Successfully!")

        # Display Headings
        st.subheader("📌 Headings")
        if headings:
            for h in headings:
                st.write("-", h)
        else:
            st.write("No headings found.")

        # Display Paragraphs
        st.subheader("📝 Paragraphs")
        if paragraphs:
            for p in paragraphs[:5]:
                st.write(p)
        else:
            st.write("No paragraphs found.")

        # Display Links
        st.subheader("🔗 Links")

        if links:
            df = pd.DataFrame(links, columns=["Links"])
            st.dataframe(df)

            # Download CSV
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇ Download Links CSV",
                data=csv,
                file_name="scraped_links.csv",
                mime="text/csv"
            )

        else:
            st.write("No links found.")

    except Exception as e:
        st.error(f"Error: {e}")
