import praw

CLIENT_ID = 'v04Fr2CmByn_zQ'
CLIENT_SECRET = "Zc6Dv8P9nEAUSU-hwWjoiLWEOd8"
REDIRECT_URI = "https://github.com/ghanashyamvtatti/autotagging"

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri= REDIRECT_URI,
                     user_agent="Scraper-Big-Data Project")

#print(reddit.auth.url(["identity"], "...", "permanent"))

def getByPopularity(reddit):
    sub = praw.models.Subreddits(reddit,_data=None)
    response = sub.popular()
    return [reddit.display_name for reddit in response]

def getByName(reddit,keyword):
    sub = praw.models.Subreddits(reddit,_data=None)
    response = sub.search_by_name(query=keyword)
    return [reddit.display_name for reddit in response]

def getByQuery(reddit,keyword):
    sub = praw.models.Subreddits(reddit,_data=None)
    response = sub.search(query=keyword)
    return [reddit.display_name for reddit in response]

def getWikiHandles(subreddit):
    handles =[]
    for wikipage in reddit.subreddit(subreddit).wiki:
        handles.append(wikipage.name)
    return handles

def getWikiContent(subreddit, wikiHandle):
    #print(subreddit, wikiHandle)
    wikipage = reddit.subreddit(subreddit).wiki[wikiHandle]
    try:
        return wikipage.content_md
    except Exception:
        return None

def getTopComments(subreddit,n=25):
    data =[]
    for submission in reddit.subreddit("subreddit").hot(limit=n):
        item = {}
        item["title"] = submission.title
        item["comments"] =[]
        for top_level_comment in submission.comments:
            print("Submission Title: ", submission.title)
            print("Top level: ",top_level_comment.body)
            item["comments"].append(top_level_comment.body)
        data.append(item)
    return data
    
handles = getWikiHandles(subreddit="iama")
allContent = []
for handle in handles:
    content = {}
    print("---------")
    content['content'] = getWikiContent(subreddit="iama",wikiHandle=handle)
    content['handle'] = handle
    allContent.append(content)
    print(content['content'])

print(allContent)

# data = getTopComments(subreddit="iama",n=25)
# print(data)