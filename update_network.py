# issues: google books query returns recent print publications? instead of the original work
# add a column for format for both source and reference? (to include non-book media?)
# add a logical column for the reference read or not read
# add an option to make an .env file if there is no API key found (first use)
# add requirements.txt
# comment on code
# add ability to hover over the points to see info, and makybe click to see quotes/notes?
# add a way to get the next set of results
#

import pandas as pd
import requests
import os
import webbrowser
import subprocess
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("GOOGLE_BOOKS_API_KEY")

if not API_key:
    print("Error: No API key found. Create an .env file.")
    exit()

def get_book_api(query):

    # turn the search term into a URL friendly format for the api and get the results
    encoded_query = quote_plus(query)
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={encoded_query}&key={API_key}"
        data = requests.get(url, timeout=5).json()

        # check if there are results
        if 'items' in data:
            all_items = data['items'][1:15] # get max 15 results
            start = 0
            max_batches = 3
            batch_number = 1

            while True:
                batch = all_items[start:start+5] # display the first 5 books

                if not batch: # if there are no items after 5 books
                    break

                batch_number += 1
                results = []
                
                print("\nGoogle Books search results:")
                for i, item in enumerate(batch): # go through each item in the current batch
                    info = item.get('volumeInfo', {})
                    title = info.get('title', 'Unknown')
                    author_list = info.get('authors', [])
                    if isinstance(author_list, list) and len(author_list) >0:
                        author = ", ".join(author_list)
                    else:
                        author = "Unknown"
                    year = info.get('publishedDate', 'N/A')[:4] # only get the year
                    results.append({'title': title, 'author': author, 'year':year})
                    print(f"[{i+1}] {title} by {author} ({year})")

                is_last_batch = batch_number >= max_batches # check if there are more items for another batch
                has_more = not is_last_batch and len(all_items) > start + 5

                if has_more:
                    print("[m] View more results")

                if not has_more:
                    print("[x] None of these")
                
                choice = input("Selection: ").strip()

                if choice.isdigit() and 1 <= int(choice) <= len(batch): # and 1 because of a 0 is inputted it will take a -1 index, which will take the last item 
                    selected = results[int(choice) -1]
                    print(f"You selected: {selected['title']} by {selected['author']} ({selected['year']})")

                    if input("Do you want to edit these details? (y/n): ").lower() == "y":
                        t = input(f"Title [{selected['title']}]: ") or selected['title']
                        a = input(f"Author [{selected['author']}]: ") or selected['author']
                        y = input(f"Year [{selected['year']}]: ") or selected['year']

                        return t, a, y
                    
                elif choice == "m" and has_more:
                    start +=5
                    continue

                elif choice == "x":
                    break

                else:
                    print("Invalid choice, please try again.")

      
    except Exception as e:
        print(f"Error: {e}")

    print("\nWhoops no results. You gotta enter it manually.")
    return input("Title: "), input("Author: "), input("Year: ")


def get_book_info(df, prompt_title):
    # get a list of books already in the dataframe
    shelved = pd.concat([
        df[["source_title", "source_author", "source_year"]].rename(columns={"source_title":"title", "source_author":"author", "source_year":"year"}),
        df[["ref_title", "ref_author", "ref_year"]].rename(columns={"ref_title":"title", "ref_author":"author", "ref_year":"year"})
        ]).drop_duplicates(subset="title")
    #case insensitive, return false if any missing titles just in case
    matches = shelved[shelved["title"].str.contains(prompt_title, case=False, na=False)]
    
    if not matches.empty:
        print("\nFound matching book(s) already in the network:")
        for i, row in enumerate(matches.itertuples(), start = 1):
            print(f"[{i}] {row.title} by {row.author} ({row.year})")
            print(f"[{len(matches) + 1}] None of these, search the API instead")
            choice = input(f" Select a number (1-{len(matches)+1}): ").strip()

            if 1 <= int(choice) <= len(matches):
                selected = matches.iloc[int(choice) -1] #get the correct selection in the matches df
                print(f"You selected: {selected['title']} by {selected['author']} ({selected['year']})")
                return selected['title'], selected['author'], selected['year']
            else:
                return get_book_api(query = prompt_title)
    else:
        return get_book_api(query = prompt_title)

if os.path.exists("library.csv"):
    df = pd.read_csv("library.csv")
else:
    df = pd.DataFrame(columns = ["source_title", "source_author", "source_year", "ref_title", "ref_author", "ref_year", "notes"])



# start of prompts
if input("Would you like to add a book to the network? (y/n): ") == "y":       

    s_query = input("\nEnter book title to search: ")
    s_title, s_author, s_year = get_book_info(df = df, prompt_title = s_query)

    while True:
        r_query = input(f"\nEnter book referenced in {s_title}: ")
        r_title, r_author, r_year = get_book_info(df = df, prompt_title = r_query)
        note = input("Enter a sentence to provide some context for this reference: ")

        new_row = pd.DataFrame([{
            "source_title":s_title, "source_author":s_author, "source_year":s_year, "ref_title":r_title, "ref_author":r_author, "ref_year":r_year, "notes":note
        }])
        
        df = pd.concat([df, new_row], ignore_index = True)
        
        if input(f"Add another reference from {s_title}? (y/n)").lower() != "y":
            break

else:
    if input("Would you like to regenerate the network widget? (y/n)") != "y":
        print("Okay, have a nice day!")

# save the updated dataframe and store it temporarily
df.to_csv("temp.csv", index=False)

# make the updated visual and store it temporarily by calling the R script
try:
    subprocess.run(["Rscript", "network.R"], check = True)


    if input("View the updated diagram? (y/n)").lower() == "y":
        webbrowser.open(f"file://{os.path.realpath("temp.html")}")
except subprocess.CalledProcessError:
    print("Error")

if input("Save the updated visual and dataframe? (y/n)") == "y":
    df.to_csv("library.csv", index = False)
    os.rename("temp.html", "viz.html")
    os.rename("temp_sc.png", "screenshot.png")


try:
    os.remove("temp.html")
except FileNotFoundError:
    pass

try:
    os.remove("temp.csv")
except FileNotFoundError:
    pass

try:
    os.remove("temp_sc.csv")
except FileNotFoundError:
    pass

print("Done!")