import praw
import os
from pprint import pprint

print("Logging into Reddit")
#Get into Reddit
reddit = praw.Reddit(client_id=' ',
                     client_secret=' ',
                     user_agent='< ')
print("Logged in to Reddit")

def newLookUp():
    # Get the subreddit
    desiredSubreddit = input("What is the name of the subreddit, excluding the /r: ")
    desiredSubreddit = desiredSubreddit.strip()
    # desiredSubreddit = "excel"
    desiredSubreddit = reddit.subreddit(str(desiredSubreddit))
    print("Got to the subReddit")
    print("Getting the submission")

    titleOfPost = input ("What is the title of the post? ")
    titleOfPost = titleOfPost.strip()
    origionalAuthor = input("Just to be sure please enter the name of the author here: ")
    origionalAuthor = origionalAuthor.strip()

    # titleOfPost = "Autofilling a referenced text"
    # origionalAuthor = "EdlsslyFscntngGurl"

    counter = 1
    for submission in desiredSubreddit.top("year", limit=None):
        print(f"I'm looking for the post {counter}")
        counter = counter + 1
        if titleOfPost == submission.title:
            print("I've found the title of the post'")
            if origionalAuthor == submission.author:
                print("I've found the author's submission of this")
                print("Getting comments")
                submission.comments.replace_more(limit=100) # flatten tree
                comments = submission.comments.list() # all comments
                titleOfPost = titleOfPost.title()
                fileName = titleOfPost + " Author: " + origionalAuthor + " Subreddit: " + str(desiredSubreddit) + ".txt"
                os.chdir(" INITIAL FILE PLACE ")
                with open (fileName, "w") as f:
                    print("Made the file")
                    f.write(f'{titleOfPost} written by {origionalAuthor} \n \n')
                    f.write(f"What they said origionally: {submission.selftext}")
                    counter = 1
                    for comment in comments:
                        if comment.author != "AutoModerator":
                            f.write(f' \n\n\n What people commented: {counter}) \n {comment.body}')
                            counter = counter + 1
                    break

def reLookUp():
    #set the counter to show on the file how many comments
    counter = 1

    #list all files that you are watching
    listOfFiles = []
    os.chdir(" INITIAL FILE PLACE ")
    
    #allow the user to see the posts that are to be chccked up on
    fileCounter = 1
    for everyfile in os.listdir():
        listOfFiles.append(everyfile)
        print(f'{fileCounter}) {everyfile}') 
        fileCounter = fileCounter + 1
    
    #get the post to check from the user's choice by number
    pickedOption = input("Which post would you like to check up on? ") 
    pickedOption = int(pickedOption) - 1
    pickedOption = listOfFiles[pickedOption]
    print(pickedOption)

    #break up the file name ot reextract the subreddit, author name and post title
    breakFileName = pickedOption.split("Author:")
    titleOfPost = breakFileName[0]
    titleOfPost = titleOfPost.strip()

    #get the origional author's name
    origionalAuthor = breakFileName [1]
    origionalAuthor = origionalAuthor.split("Subreddit:")
    origionalAuthor = origionalAuthor[0]
    origionalAuthor = origionalAuthor.strip()

    #get the subreddit name
    breakFileName = pickedOption.split("Subreddit:")
    desiredSubreddit = breakFileName [1]
    noExtention = desiredSubreddit.split(".txt")
    desiredSubreddit = noExtention[0]
    desiredSubreddit = desiredSubreddit.strip()
    
    # confirm the post to check, and the subreddit
    print(f"Your post title was: {titleOfPost}")
    print(f"This was posted by: {origionalAuthor}")
    print(f"On the subreddit: {desiredSubreddit}")
    
    for submission in reddit.redditor(origionalAuthor).stream.submissions():
        print(submission.title)
        if submission.title == titleOfPost:
            submission.comments.replace_more(limit=100) # flatten tree
            comments = submission.comments.list() # all comments
            checkFileName = "Check: " + titleOfPost + ".txt"
            os.chdir(" COMPARE FILE PLACE")
            with open (checkFileName, "w") as f:
                print("Made the file")
                f.write(f'{titleOfPost} written by {origionalAuthor} \n \n')
                f.write(f"What they said origionally: {submission.selftext}")
                for comment in comments:
                    if comment.author != "AutoModerator":
                        f.write(f' \n\n\n What people commented: {counter}) \n {comment.body}')
                        counter = counter + 1
                break
    compareFiles(pickedOption, checkFileName)
    

def compareFiles(pickedOption, checkFileName):
    print("Comparing files")
    f1 = " INITAL FILE PLACE " + pickedOption
    f2 = " COMAPRE FILE PLACE " + checkFileName

    f1 = open(f1, "r")  
    f2 = open(f2, "r")  

    i = 0
    
    for line1 in f1:
        i += 1
        for line2 in f2:
            # matching line1 from both files
            if line1 != line2:
                print("Line ", i, ":")
                # else print that line from both files
                print("\tFile 1:", line1, end='')
                print("\tFile 2:", line2, end='')
            else: 
                print(f"This line hasn't changed: {i}")    
            break
    
    # closing files
    f1.close()                                       
    f2.close()   

def closePost():
    listOfFiles = []
    firstDir = " INITAL FILE PLACE"
    os.chdir(firstDir)
    
    #allow the user to see the posts that are to be chccked up on
    fileCounter = 1
    for everyfile in os.listdir(firstDir):
        listOfFiles.append(everyfile)
        # print(f'{fileCounter}) {everyfile}') 
        fileCounter = fileCounter + 1
    
    #how to get both files with different names and remove both/delete
    completedFiles = []
    secondDir = " COMPARE PLACE "
    os.chdir(secondDir)
    completedFileCounter = 1
    for eachFile in os.listdir(secondDir):
        completedFiles.append(eachFile)
        # print(f"{completedFileCounter}) {eachFile}")
        completedFileCounter = completedFileCounter + 1

    # print (type(listOfFiles))
    # print (type(completedFiles))
    # print(f"{listOfFiles} \n")
    # print(f"{completedFiles} \n")

    postToLookForSubmissionTitles = []
    postCompleteFileList = []
    
    i = 0
    watchedPostSubmissionNames = []
    while i < len(listOfFiles):
        splitTheNameUp = listOfFiles[i]
        splitTheNameUp = splitTheNameUp.split("Author: ")
        splitTheNameUp = splitTheNameUp[0]
        watchedPostSubmissionNames.append(splitTheNameUp)
        i = i + 1

    c = 0
    comparedFilesPostNames = []
    while c < len(completedFiles): 
        splitCheckOff = completedFiles[c]
        splitCheckOff = splitCheckOff.split("Check: ")
        splitCheckOff = splitCheckOff[1]
        comparedFilesPostNames.append(splitCheckOff)
        c = c + 1

    # print(f"List of files in Posts to look: {watchedPostSubmissionNames}\n")
    # print(f"List of files in to compare: {comparedFilesPostNames}\n")

    a = 0
    while a < len(watchedPostSubmissionNames):
        removeExtention = watchedPostSubmissionNames[a]
        removeExtention = removeExtention.split(".txt")
        removeExtention = removeExtention[0]
        # print(removeExtention)
        postToLookForSubmissionTitles.append(removeExtention)
        a = a + 1

    b = 0
    # print(f"{comparedFilesPostNames[b]}\n")
    while b < len(comparedFilesPostNames):
        removeExtentions = comparedFilesPostNames[b]
        removeExtentions = removeExtentions.split(".txt")
        removeExtentions = removeExtentions[0]
        postCompleteFileList.append(removeExtentions)
        b = b + 1

    # print(f"Proper names in watch submission: {postToLookForSubmissionTitles}\n")
    # print(f"{len(comparedFilesPostNames)}\n")
    # print(f"Proper names in files to compare: {postCompleteFileList}\n")
    p = 0
    q = 0 
    while p < len(watchedPostSubmissionNames):
        while q < len(comparedFilesPostNames):
            if watchedPostSubmissionNames[p] == comparedFilesPostNames[q]:
                print(f"{watchedPostSubmissionNames[p]}\n")
                print(f"{comparedFilesPostNames[q]}\n")
                p = p + 1
                q = q + 1
                 
            break
        break

useroption = input("What would you like to do? (1) Store a new post? (2) Check if there are any updates? (3) Stop following a post? ")
# useroption = "3"

if useroption == "1":
    newLookUp()
if useroption == "2":
    reLookUp()
if useroption == "3":        
    closePost()
    
