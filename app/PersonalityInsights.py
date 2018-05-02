from __future__ import print_function
from watson_developer_cloud import PersonalityInsightsV3
import json
import sys
import requests
import tweepy
import io
from pathlib import Path
#######Clearly you will never use this in production but it serves to show the methods

##Tweepy and Twitter setup
access_key = "800656444328546304-sVhWw2d93iOEpK33TT4hL8DTNmWWxOv"
access_secret = "PETOnHEqXwZKagf11d4LXE1CoNuj63rOgmkDuPMQU8exJ"
consumer_key = "R8wXApxv1HyOZzVxqpZrK4FzU"
consumer_secret = "vdqUjF6ly6Jp3oWygpfIE0Px9fJvrontoqzALALguNILOkaX79"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

twitter_api = tweepy.API(auth)


### Personality insights setup
personality_insights = PersonalityInsightsV3(
  version='2017-10-13',
  username='597f97f4-6f57-49d3-9bb4-1f8b64785d2c',
  password='KIwpVrB6Vf3f'
)


##This takes the information from twitter and makes it readable by Personality Insights
def convert_status_to_pi_content_item(s):
    
    return {
        'userid': str(s.user.id),
        'id': str(s.id),
        'sourceid': 'python-twitter',
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        #'created': s.created_at_in_seconds,
        'reply': (s.in_reply_to_status_id is None),
        'forward': False
    }

#Twitter handle is used for a lot in this code so we make it a variable now
handle = sys.argv[1]

#using tweepy read the twitter feed of the perosn we want to analyse
def get_feed(handle): 
    max_id = None
    statuses = []

    for x in range(0, 16):  # Pulls max number of tweets from an account
        if x == 0:
            statuses_portion = twitter_api.user_timeline(screen_name=handle,
                                                         count=200,
                                                         include_rts=False)
            status_count = len(statuses_portion)
            # get id of last tweet and bump below for next tweet set
            max_id = statuses_portion[status_count - 1].id - 1
        else:
            statuses_portion = twitter_api.user_timeline(screen_name=handle,
                                                         count=200,
                                                         max_id=max_id,
                                                         include_rts=False)
            status_count = len(statuses_portion)
            try:
                # get id of last tweet and bump below for next tweet set
                max_id = statuses_portion[status_count - 1].id - 1
            except Exception:
                pass
        for status in statuses_portion:
            statuses.append(status)

    #print ('Number of Tweets has: %s' % str(len(statuses)))

    pi_content_items_array = map(convert_status_to_pi_content_item, statuses)
    pi_content_items = {'contentItems': pi_content_items_array}
    return (pi_content_items)

# A workaround due to time constraints, one possible fix to allow multiple users is to store each handle to a DB ( mongo/cloudant )
# and call that json as needed. The easiest is prob to work out how to stream the results directly 
def write_to_file(handle):
    data=get_feed(handle)
    filename=handle+".json"
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))

    #print ("details saved to showme.json")   
    return() 

#checks if feed already exists if not creates it
def checkcache(handle):
    filename="./"+handle+".json"
    file=Path(filename)
    print (filename)
    if file.exists():
        return filename
    else:
        write_to_file(handle)
        return filename

#the meat of the issue. This returns a list of all consumption preferences as anylsed by PI as per their algorithm.
#returns array of preferences
def get_personality_insights(handle):
   
    filename = checkcache(handle)

    
    #deliver a personaility profile from the feed that we have
    with open(filename) as profile_json:
        profile = personality_insights.profile(
            profile_json.read(), content_type='application/json', 
            raw_scores=False, consumption_preferences=True)

        #get music preferences from the proflle
        preferences=profile["consumption_preferences"]
        return preferences

#simple function to get rid of the stuff we dont need and make some slight changes
def cleanUp(data):
    if 'playing' in data:
        data.remove('playing')
    if 'musical' in data:   
        data.remove('musical')
    if 'hop' in data:
        data.append('hip-hop')
        data.remove('hop')
    return data

#from the consumption preferences narrows down music and then creates arrays of what we will and might listen to 
def get_music_preferences(handle):
    preferences=get_personality_insights(handle)
    music=preferences[5]

    likely=[]
    might=[]

    for genre in music['consumption_preferences']:
        liking= genre['score']
        name = genre['name'].split(' ')[-2]
        if liking>0.5:
            likely.append(name)
        elif liking > 0:
            might.append(name)   

    likely=cleanUp(likely)
    might=cleanUp(might)        
    #return the information that is required    
    return( likely, might)

def get_movie_preferences(handle):
    preferences=get_personality_insights(handle)
    music=preferences[4]

    likely=[]
    might=[]

    for genre in music['consumption_preferences']:
        liking= genre['score']
        name = genre['name'].split(' ')[-2]
        if liking>0.5:
            likely.append(name)
        elif liking > 0:
            might.append(name)   

    #likely=cleanUp(likely)
    #might=cleanUp(might)        
    #return the information that is required    
    return( likely, might)    








