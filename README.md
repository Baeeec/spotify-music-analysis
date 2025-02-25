# Spotify Analysis – Charlie Puth’s Music Trends 🎵

## Overview  
This project analyzes Charlie Puth's music trends using Spotify API data, AWS (Lambda, S3, RDS), Python, MySQL (RDS), and Tableau.

## Technologies Used  
- **AWS Lambda (Python)**: Handling API calls, fetching and processing Spotify data
- **S3 & RDS**: Storing structured data  
- **MySQL**: Cleaning, transforming, and analyzing data  
- **Tableau**: Creating visualizations and dashboards for insights

## Process  
1. **AWS Lambda:**  
   - Installed dependencies (`requests`) locally and uploaded as Lambda layers.  
   - Authenticated with Spotify API to fetch artist albums & track details.  
   - Converted data to CSV and uploaded to S3.  

2. **Database (MySQL on RDS):**  
   - Connected MySQL Workbench to RDS.  
   - Created tables and loaded data from S3.  
   - Cleaned data (handled nulls, converted formats, removed duplicates).  

3. **Analysis & Insights:**  
   - Identified the most active artists in 2024.  
   - Analyzed seasonal trends in music releases.  

4. **Visualization with Tableau:**  
   - Connected RDS to Tableau.  
   - Created charts & dashboards (e.g., genre distribution across albums).  

## Results  
🚀 Key trends in artist activity and song popularity uncovered!  
📊 Check out the visualizations and SQL queries in this repo.  

## 📌 How to Run  
1. Clone the repo: `git clone https://github.com/your-username/spotify-music-analysis.git`  
2. Set up AWS credentials and MySQL connection.  
3. Run the provided Python scripts and SQL queries.  

## 🔗 Links  
- [LinkedIn Post](#)  
- [Tableau Public Dashboard](#)  

---
