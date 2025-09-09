import sqlite3

# Make connection to file based database
con = sqlite3.connect('youtube_manager.db')
cursor = con.cursor()

# Create tables
cursor.execute('''
               CREATE TABLE IF NOT EXISTS videos(
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   time TEXT NOT NULL
                   )
                 ''' ) 
def list_videos():
    cursor.execute("SELECT * FROM videos")   # tells SQLite what to query and fills the cursor with results.
    rows = cursor.fetchall()                     # Get all rows as tuples, fetchall helps get the
                                            # result that the cursor already holds in above query
    if not rows:
        print("No videos have been added yet")
        return  # exits function here
    for row in rows:         
        print(row)

def add_video(name,time):
    # The Python sqlite3 library sends the SQL plus the separate params to the SQLite engine
    #sqlite3 binds the params safely into the placeholders (so you avoid SQL injection and quoting issues)
    #The execute call performs the insertion on the database connection’s cursor
    cursor.execute("INSERT INTO videos(name, time) VALUES (?, ?)",(name, time)) 
    
    # Now we have to separately commit using con as cursor only used to execute queries
    con.commit()   

def update_video(video_id, new_name, new_time):
    cursor.execute("UPDATE videos SET name = ?, time = ? WHERE id = ?",(new_name, new_time, video_id))
    con.commit()

def delete_video(video_id):
    cursor.execute("DELETE FROM videos WHERE id = ?",(video_id,))
    con.commit()
    

def main():
    
    while True:     # So the app keeps on running until 5th choice then break
        print("\n Youtube Manager App with in-built Database")
        print("1.** List Videos **")
        print("2.** Add Videos **")
        print("3.** Update Videos **")
        print("4.** Delete Videos **")
        print("5.** Exit App **")
        
        # Now take input from user
        choice = input("Enter your choice: ")
        
        if choice == "1":
            list_videos()
        elif choice == "2":
            # Ask user for input of video name and time
            name = input("Enter the video name: ")
            time = input("Enter the video length: ")
            add_video(name,time)
        elif choice == "3":
            # Update the video based on input of videoid given by user
            video_id =input("Enter video id which is to be updated: ")
            name = input("Enter the new video name: ")
            time = input("Enter the new video length: ")
            update_video(video_id,name,time)
        elif choice == "4":
            video_id =input("Enter video id which is to be deleted: ")
            delete_video(video_id)
        elif choice == "5":
            break #exiting loop means exiting the app
        else:
            print("Invalid Choice")
              
    con.close()     # When the user exits, then disconnect the connection of python to database too
                    # preventing database corruption
            
            


if __name__ == "__main__":
    main()
