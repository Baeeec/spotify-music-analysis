# Spotify Analysis – Charlie Puth’s Music Trends 🎵

## Overview  
This project analyzes Charlie Puth's music trends using Spotify API data, AWS (Lambda, S3, RDS), Python (Pandas), MySQL (RDS), and Tableau.

## Technologies Used  
- **AWS Lambda (Python)**: Handling API calls, fetching and processing Spotify data
- **S3 & RDS**: Storing structured data  
- **MySQL**: Cleaning, transforming, and analyzing data  
- **Tableau**: Creating visualizations and dashboards for insights

## Process  
1. **Data Extraction & Storage (AWS Lambda & S3):**  
   - Installed required dependencies (`requests`, `sqlalchemy`, `pymysql`) locally and uploaded them as Lambda layers.
   - Authenticated with the Spotify API and used the artist name "Charlie Puth" to fetch artist, album, and track details from multiple API endpoints.
   - Processed and structured the data into CSV format.
   - Uploaded the CSV files to an Amazon S3 bucket for storage.

2. **Data Loading & Database Integration (AWS Lambda & RDS MySQL):**
   - Connected to Amazon S3 to access the stored CSV data.
   - Established a connection with Amazon RDS (MySQL database) using `sqlalchemy` and `pymysql`.
   - Created a MySQL table in RDS and loaded the CSV data into it.
     
3. **Database (MySQL on RDS)**
   - Connected MySQL Workbench to RDS for validation and queries.
   - Cleaned data (handled nulls, converted formats, removed duplicates).
   - Performed SQL queries for data analysis.

5. **Visualization with Tableau:**  
   - Connected Tableau to the RDS MySQL database.
   - Created 6 charts & a dashboard to visualize key insights.
   
## Results  
🚀 Uncovered key trends in Charlie Puth's music releases, track popularity, and collaboration impact!
   - Found that hit singles drive temporary popularity spikes, while albums generally perform better overall.
   - Identified an inverse relationship between track length and popularity—shorter songs tend to be more successful.
   - Analyzed how collaborations influence popularity, with solo tracks often outperforming them.

📊 Check out the visualizations, AWS Lambda functions, and SQL queries in this repo!

## 📌 How to Run  
1. Clone the repo: `git clone https://github.com/your-username/spotify-music-analysis.git`  
2. Set up AWS credentials and MySQL connection.  
3. Run the provided Python scripts and SQL queries.  

## 🔗 Links  
- [LinkedIn Post](#)  
- [Tableau Public Dashboard](https://public.tableau.com/views/SpotifyAnalysisCharliePuthsMusicTrends1/SpotifyAnalysisCharliePuthsMusicTrends?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)  

---
