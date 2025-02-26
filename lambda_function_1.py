import json
import base64
import requests
import boto3
import csv
import io
import os
import datetime
import pytz

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
auth_url = 'https://accounts.spotify.com/api/token'
base_url = "https://api.spotify.com/v1"

def get_token():
  client_creds = f"{client_id}:{client_secret}"
  client_bytes = client_creds.encode()
  client_creds_b64 = base64.b64encode(client_bytes).decode()

  auth_headers = {
      'Authorization': f'Basic {client_creds_b64}',
      'Content-Type': 'application/x-www-form-urlencoded'
  }
  auth_data = {'grant_type': 'client_credentials'}

  response = requests.post(auth_url, headers=auth_headers, data=auth_data)

  if response.status_code != 200:
      print(f"Error fetching token: {response.status_code}")
      print(response.json())  #Debugging
      return None

  return response.json().get("access_token")

token = get_token()
headers = {"Authorization": f"Bearer {token}"}

#Get Charlie Puth's artist ID and info
def get_artist_info(artist_name):
  url = f"{base_url}/search" #Use search end point
  params = {"q": artist_name, "type": "artist", "limit": 1}
  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  artist = data["artists"]["items"][0]
  artist_info = {
  "artist_name": artist["name"],
  "artist_id": artist["id"],
  "popularity": artist["popularity"],
  "followers": artist["followers"]["total"],
  "genres": artist["genres"]
  }
  return artist_info

#Get all albums of the artist by their Spotify ID.
def get_artist_albums(artist_id):
  albums = []
  url = f"{base_url}/artists/{artist_id}/albums" #Use artists end point to fetch album data using artist id
  params = {"include_groups": "album,single,compilation", "limit": 50}

  while url:
      response = requests.get(url, headers=headers, params=params)

      data = response.json()

      if "items" in data:
          for album in data["items"]:
              album_info = {
                  "album_name": album["name"],
                  "album_id": album["id"],
                  "release_date": album["release_date"],
                  "total_tracks": album["total_tracks"],
                  "available_markets_count": len(album.get("available_markets", [])),  #Count of available markets
                  "album_type": album["album_type"],
                  "album_group": album.get("album_group", "N/A"),
              }  
              #Additional details from get_album_details()
              album_details = get_album_details(album["id"])
              album_info.update(album_details)
            
              albums.append(album_info)
          url = data.get("next")  #Pagination
        
  return albums

#Get additional details of each album and each track of each album
def get_album_details(album_id):
  url = f"{base_url}/albums/{album_id}"
  response = requests.get(url, headers=headers)
  data = response.json()

  album_details = {
      "popularity": data.get("popularity", "N/A"),
      "genres":data.get("genres", []),
      "label": data.get("label", "N/A"),
      "tracks": [] #Initialize an empty list to hold track details
  }

  #Extract track info from the 'tracks' field
  for track in data.get("tracks", {}).get("items", []):
      track_info = {
          "track_name": track.get("name", "N/A"),
          "track_id": track.get("id", "N/A"),
          "duration_ms": track.get("duration_ms", "N/A"),
          "explicit": track.get("explicit", "N/A"),
          "track_number": track.get("track_number", "N/A"),
          "available_markets_count": len(track.get("available_markets", [])),  #Count of available markets
      }
      #Additional track details from get_track_details ()
      track_details = get_track_details(track_info["track_id"])
    
      #Combine track_info and track_details
      track_info.update(track_details)

      album_details["tracks"].append(track_info)

  return album_details

#Get additional details for a track.
def get_track_details(track_id):
  url = f"{base_url}/tracks/{track_id}"
  response = requests.get(url, headers=headers)
  data = response.json()

  #Extract popularity and artist name
  track_details = {
      "popularity": data.get("popularity", "N/A"),
      "artists": [artist["name"] for artist in data.get("artists", [])]  #Get all artist names
  }
  return track_details

#Upload CSV data to an S3 bucket
def upload_to_s3(csv_data, bucket_name, object_name):
  #Create an S3 client
  s3_client = boto3.client('s3')
  try:
      #Convert CSV data into bytes and upload to S3
      s3_client.put_object(
          Bucket=bucket_name,
          Key=object_name,
          Body=csv_data,
          ContentType='text/csv'
      )
      print(f"Successfully uploaded CSV to s3://{bucket_name}/{object_name}")
  except Exception as e:
      print(f"Error uploading CSV to S3: {e}")

#Convert artist info and albums to CSV format
def convert_to_csv(artist_info, artist_albums):
  output = io.StringIO()
  csv_writer = csv.DictWriter(output, fieldnames=[
      "artist_name", "popularity", "followers", "genres", "album_name", "album_id",
      "release_date", "total_tracks", "available_markets_count", "album_type", "album_group",
      "album_popularity", "album_genres", "album_label",
      "track_number", "track_name", "track_id", "duration_ms", "explicit", "track_popularity", "artists"
  ])
  csv_writer.writeheader()

  #Write artist info and album data
  for album in artist_albums:
      for track in album["tracks"]:
          #Flatten data and write to CSV
          row = {
              "artist_name": artist_info["artist_name"],
              "popularity": artist_info["popularity"],
              "followers": artist_info["followers"],
              "genres": ", ".join(artist_info["genres"]),
              "album_name": album["album_name"],
              "album_id": album["album_id"],
              "release_date": album["release_date"],
              "total_tracks": album["total_tracks"],
              "available_markets_count": album["available_markets_count"],
              "album_type": album["album_type"],
              "album_group": album["album_group"],
              "album_popularity": album["popularity"],
              "album_genres": ", ".join(album["genres"]),
              "album_label": album["label"],
              "track_number": track["track_number"],
              "track_name": track["track_name"],
              "track_id": track["track_id"],
              "duration_ms": track["duration_ms"],
              "explicit": track["explicit"],
              "track_popularity": track["popularity"],
              "artists": ", ".join(track["artists"])
          }
          csv_writer.writerow(row)

  #Return the CSV data as a string
  return output.getvalue()

def lambda_handler(event, context):
  artist_name = event.get("artist_name", "Charlie Puth") #Change the name here, case insensitive
  artist_info = get_artist_info(artist_name) #Fetch artist info and albums
  artist_albums = get_artist_albums(artist_info["artist_id"]) #Fetch albums and tracks of the artist
  csv_data = convert_to_csv(artist_info, artist_albums) #Convert the data to CSV

  local_tz = pytz.timezone("America/New_York") #Set the timezone to est since lambda runs on utc time by default
  today_date = datetime.datetime.now(local_tz).strftime("%Y-%m-%d")  

  bucket_name = "spotify-fetch-data"
  object_name = f"{today_date}_{artist_info['artist_name']}_data.csv"

  upload_to_s3(csv_data, bucket_name, object_name)

  return {
      "status": "Success",
      "message": f"Data successfully uploaded to s3://{bucket_name}/{object_name}"
  }