
# add a column for notes/quotes
# add a column for format for both source and reference?
# add a logical column for the reference read or not read
# fix oliver twist year to 1838

import pandas as pd
import requests
import os
import webbrowser
import subprocess
from urllib.parse import quote_plus
from dotenv import load_dotenv


def get_book_api(query):
    encoded_query = quote_plus(query)
    try:
        url = f"https://openlibrary.org/search.json?q={encoded_query}"
        data = requests.get(url, timeout=5).json() #put data into a dictionry

        if 'docs' in data and len(data['docs']) > 0:
            results = [] #store the first 3 results

            for i, item in enumerate(data['docs'][:3]):
                title = item.get('title', 'Unknown')
                author_list = item.get('author_name', [])
                author = ", ".join(author_list) if author_list else "Unknown"
                year = str(item.get('first_publish_year', 'N/A'))
                results.append({'title': title, 'author': author, 'year':year})
                print(f"[{i+1}] {title} by {author} ({year})")

            print("[4] Whoops, none of these (enter manually)")

            choice = input("Select a number (1-4): ")

            if choice in ['1','2','3'] and int(choice) <= len(results):
                selected = results[int(choice) -1]
                print(f"You selected: {selected['title']} by {selected['author']} ({selected['year']})")

                if input("Do you want to edit these details? (y/n): ").lower() == "y":
                    t = input(f"Title [{selected['title']}]: ") or selected['title']
                    a = input(f"Author [{selected['author']}]: ") or selected['author']
                    y = input(f"Year [{selected['year']}]: ") or selected['year']

                    return t, a, y
            return selected['title'], selected['author'], selected['year']
      
    except Exception as e:
        print(f"Error: {e}")
    print("\nWhoops. You gotta enter it manually.")
    return input("Title: "), input("Author: "), input("Year: ")

if os.path.exists("library.csv"):
    df = pd.read_csv("library.csv")
else:
    df = pd.DataFrame(columns = ["source_title", "source_author", "source_year", "ref_title", "ref_author", "ref_year"])

s_query = input("\nEnter book title to search: ")
s_title, s_author, s_year = get_book_api(s_query)

while True:
    r_query = input(f"\nEnter book referenced in {s_title}: ")
    r_title, r_author, r_year = get_book_api(r_query)

    new_row = pd.DataFrame([{
        "source_title":s_title, "source_author":s_author, "source_year":s_year, "ref_title":r_title, "ref_author":r_author, "ref_year":r_year
    }])
    
    df = pd.concat([df, new_row], ignore_index = True)
    
    if input(f"Add another reference from {s_title}? (y/n)").lower() != "y":
        break

# save the updated dataframe and store it temporarily
df.to_csv("temp.csv", index=False)

# make the updated visual and store it temporarily by calling the R script
try:
    subprocess.run(["Rscript", "network.R"], check = True)


    if input("View the updated diagram? (y/n)").lower() == "y":
        webbrowser.open(f"file://{os.path.realpath("temp.html")}")
except subprocess.CalledProcessError:
    print("Error")

if input("Save the updated visual and dataframe?") == "y":
    df.to_csv("library.csv", index = False)
    os.rename("temp.html", "viz.html")


try:
    os.remove("temp.html")
except FileNotFoundError:
    pass

try:
    os.remove("temp.csv")
except FileNotFoundError:
    pass

print("Done!")