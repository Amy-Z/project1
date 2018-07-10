import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

with open('zips.csv', newline='') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        db.execute("INSERT INTO locations (zipcode, city, state, lat, long, population) VALUES (:zipcode, :city, :state, :lat, :long, :population)",
            {"zipcode": row[0], "city": row[1], "state": row[2], "lat": row[3], "long": row[4], "population": row[5]})
        db.commit()





#     # Open a file using Python's CSV reader.
#     f = open("zips.csv")
#     reader = csv.reader(f)

#     # Iterate over the rows of the opened CSV file.
#     for row in reader:

#         # Execute database queries, one per row; then print out confirmation.
#         db.execute("INSERT INTO locations (location, shortcode, zipcode, latitude, longitude, population) VALUES (:location, :shortcode, :zipcode, :latitude, :longitude, :population)",
#                     {"location": row[0], "shortcode": row[1], "zipcode": row[2], "latitude":row[3], "longitude":row[4], "population":row[5]})
#         print(f"{row[0]} {row[1]} has a zip code of {row[2]}. {row[0]} is Added flight from {row[0]} to {row[1]} lasting {row[2]} minutes.")

#     # Technically this is when all of the queries we've made happen!
#     db.commit()

