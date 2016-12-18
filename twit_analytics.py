#!/usr/bin/python
# -*- coding: utf-8 -*-

#TWIT_V119.py        for FATCOW implementation
#Webtunnel_vNNN.py

#Program to test TWITTER API functionality

#Program objectives
# - to get the data of the user
# - first get the first personal data
# - then get the friends and follower list
# - then get the last 200 tweets and analyze them
# - tweets are saved in the simple SQLITE3 database


#add the path of the twitter egg
import sys
egg_path = '/home/users/web/b603/moo.nikb999com/cgi-bin/PyPkg/twitter-1.14.3-py2.7.egg'
sys.path.append(egg_path)


# Import the CGI, string, sys, and md5crypt modules
import json, urllib2, re, time, datetime, sys, cgi, os
import sqlite3
import MySQLdb as mdb
#import pymysql as mdb
import string, random
from urlparse import urlparse
from twitter import *
from tempfile import TemporaryFile
from collections import *
from py_site_header import *



def thisPYfile():
    return 'twit_analytics.py'

def define_keys():
    CONSUMER_KEY="......................"       
    CONSUMER_SECRET="...................."  
    ACCESS_TOKEN="..........................."
    ACCESS_TOKEN_SECRET="...................................."
    return CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def start_database_to_store_tweets():
    dbhost="......................"     # Host name 
    dbuser="......."                      # Mysql username 
    dbpswd="......."                   # Mysql password 
    dbname = '........'                    # MySql db  
    try:
        conn = mdb.connect(host=dbhost,user=dbuser,passwd=dbpswd,db=dbname)
        c = conn.cursor()
        return c, True, conn
    except mdb.Error, e:
        return e, False


def site_header(st=''):
    site_start()
    print '</div>'
    site_title(st)


def site_start():
    print '''
            Content-type:text/html\r\n\r\n
            <html>
            <div class="wrap" id="wrap_id"> 
            <head>
            <meta http-equiv="content-type" content="text/html;charset=utf-8" />  
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Financial Models</title>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
            <script type="text/javascript" src="../js/js_functions.js"></script>
            <link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">
            <link rel="stylesheet" href="http://www.w3schools.com/lib/w3-theme-indigo.css">
            <link href='http://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css' rel='stylesheet' type='text/css'>
            <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css">

            <style>
                a:link      { text-decoration: none; }
                a:visited   { text-decoration: none;  }
                a:hover     { text-decoration: none;  }
                a:active    { text-decoration: none;  }
            </style>

            </head> 
            <body> 
    '''

def site_title(s_title):
    print '''
            <div id="site_title" class="w3-container w3-theme-d4 w3-center w3-padding-jumbo">
                <p>&nbsp;</p>
                <div class="w3-row w3-jumbo">
                
        '''
    print s_title
    print '''
                <br>
                </div>
            </div>
        '''

def site_footer():
    import datetime
    
    curr_year = datetime.datetime.now().strftime("%Y")
    print '<div class="w3-container w3-border-top" style="text-align:center">'
    print '<p>   &copy; 2013-'+curr_year+' | '
    print '<a>Contact Us</a> </p>'
    print '<p><a  href="./termsofuse.py">Terms of Use</a> |',
    print '<a  href="./home.py#aboutus">About Us</a> </p>'
    print '</div>'
    print '</form>'
    print ' </body>'        
    print ' </div>'        #for the div id = wrap
    print ' </html>'

	
    
def html_start():
    # Start the HLML Block
    site_header('Twitter Analytics')


def html_end():
    site_footer()


def top_list(in_l,topx):
    #function to get the top xx items in a list
    # Need this because v2.6 of python does not have Counter in collections
    counter = {}
    for i in in_l: 
        counter[i] = counter.get(i, 0) + 1
    
    final_dict = sorted([ (freq,word) for word, freq in counter.items() ], reverse=True)[:topx]
    
    return final_dict

def text_sanitize(in_text):
    out_text = in_text.replace("'","")
    out_text = out_text.replace("\""," ").replace("\\"," ").replace("="," ").replace("''",'\"').replace("' '",'\"')
    return out_text
    
    
def generate_form():
    html_start()

    print '<div id="body_sty">'
    print '<p>Explore the world of Twitter and discover information about twitter users, their friends and followers as well as lexical analysis of the tweets.</p>'
    
    print '<TABLE style="display: block;" BORDER = 0>'
    print "<FORM METHOD = post ACTION=\'"+thisPYfile()+"\'>"
    print "<TR><TH align=\"left\">Screen Name:</TH><TD><INPUT type = text name=\"scn_name\"></TD><TR>"
    print "</TABLE>"
    print "<INPUT TYPE = hidden NAME = \"action\" VALUE = \"display\">"
    print "<INPUT TYPE = submit VALUE = \"Enter\">"
    print "</FORM>"
    print '</div>'
    html_end()

    

    
def user_public_info(find_id_for):
    #html_start()
    #this line gets the public info for the user
    print '<h2>'+'\nUsers Public Info'+'</h2>'
    do_rest_of_module = 0
    try:
        t = Twitter(auth=OAuth(define_keys()[2],define_keys()[3],define_keys()[0],define_keys()[1]))
        response = t.users.lookup(screen_name=find_id_for)
        #print '<p>', '\tResponses left:', response.headers['x-rate-limit-remaining'] ,'</p>' 
        do_rest_of_module = 1
    except:
       print '<p>', 'Error getting public data' ,'</p>' 


    if do_rest_of_module == 1:
        print '<h3>'+'\nBasic Info for: ', find_id_for+'</h3>'
        print '<p>', '\tKey Data' ,'</p>' 
        print '<ul>'
        print '<li>ID:',response[0]['id'],'</li>'
        print '<li>Screen Name:',response[0]['screen_name'],'</li>'
        print '<li>Name:',response[0]['name'] ,'</li>' 
        print '<li>Location:',response[0]['location'] ,'</li>'
        print '<li>Friends:',response[0]['friends_count'] ,'</li>'
        print '<li>Followers:',response[0]['followers_count'] ,'</li>'
        print '<li>Messages posted:',response[0]['statuses_count'] ,'</li>' 
        print '</ul>'
        #print >> f1, json.dumps(response[0],indent=2)
        
    #html_end()        


    
       
def get_last200_tweets(in_user):
    #this method will get the last 200 tweets of the user
    #rate limit is 180 requests per 15 min window
    #print '<h2>'+'\nAnalysis of Past Tweets for',in_user,'</h2>'
    do_rest_of_module = 0
    try:
        t = Twitter(auth=OAuth(define_keys()[2],define_keys()[3],define_keys()[0],define_keys()[1]))
        response=t.statuses.user_timeline(screen_name=in_user,count=200)
        #print '<p>', '\tResponses left:', response.headers['x-rate-limit-remaining'] ,'</p>' 
        #print '<p>Line 201. Response length: ',len(response),'</p>'
        if len(response) > 0:
            do_rest_of_module = 1
        else:
            print '<p>', 'No info found for: ',in_user ,'</p>' 
    except:
        print '<p>', 'Error getting tweets info for: ',in_user ,'</p>' 


    if do_rest_of_module == 1:
        base_twit_list = []
        data_for_plots = []

        x = response
        #x = [element.lower() for element in response]      #x is list - LOWER CASE
        hashtag_list = []            #start an empty list of hashtags
        at_list = []                #start an empty list of twitter IDs
        re_twt_list = []            #start a list of retweets
        #get the start and end dates
        sdf = x[0]['created_at']        #get the full date of last tweet
        start_date = datetime.date(int(sdf[26:30]), int(time.strptime(sdf[4:7],'%b').tm_mon), int(sdf[8:10]))
        edf = x[len(x)-1]['created_at']        #get the full date of first tweet
        end_date = datetime.date(int(edf[26:30]), int(time.strptime(edf[4:7],'%b').tm_mon), int(edf[8:10]))
        #end_date = str(edf[8:10])+'-'+str(edf[4:7])+'-'+str(edf[26:30])
        twit_day_range = (start_date-end_date).days
        avg_twit_day = (1.0*len(x)/max(1,twit_day_range))
        
        print >> t2, '<h4>'+'Tweet Stats for ', in_user+'</h4>'
        #print x[0]
        #print '\tStats for last',len(x), 'tweets by',in_user
        fix_nm = x[0]['user']['screen_name']
        try:
            if str(x[0]['user']['name']).decode('ascii'): fix_nm = str(x[0]['user']['name'])
        except:
            #print 'something wrong with the name for ', x[0]['user']['name']
            fix_nm = x[0]['user']['screen_name']
        
        print >> t2, '<ul>'
        print >> t2,  '<li>Key Personal Data</li>'
        print >> t2, '<ul>'
        print >> t2, '<li>ID:',x[0]['user']['id'],'</li>'
        print >> t2, '<li>Screen Name:',x[0]['user']['screen_name'],'</li>'
        print >> t2, '<li>Name:',fix_nm,'</li>'        
        #print '<li>Location:',x[0]['user']['location'],'</li>'
        print >> t2, '<li>Friends:',x[0]['user']['friends_count'] ,'</li>'
        print >> t2, '<li>Followers:',x[0]['user']['followers_count'] ,'</li>'
        print >> t2, '<li>Messages posted:',x[0]['user']['statuses_count'] ,'</li>' 
        foll_frnd_rat = 1.0*x[0]['user']['followers_count'] / max(1,x[0]['user']['friends_count'])
        print >> t2, '<li>Follower to Friend Ratio:', '%.1f' %(foll_frnd_rat),'</li>'
        print >> t2, '</ul>'
        print >> t2, '</ul>'
        print >> t2, '<ul>'
        print >> t2, '<li>',len(x),'tweets in past',twit_day_range,'days',
        print >> t2, '(',end_date,'to',start_date,')' ,'</li>' 
        print >> t2, '<li>', 'Avg of ','%.1f' %(avg_twit_day),'tweets per day' ,'</li>' 

        #add info to the data for charts list
        data_for_plots.extend([x[0]['user']['screen_name']])
        data_for_plots.extend([x[0]['user']['friends_count']])
        data_for_plots.extend([x[0]['user']['followers_count']])
        data_for_plots.extend([x[0]['user']['statuses_count']])
        data_for_plots.extend([twit_day_range])
        data_for_plots.extend([len(x)])

        for item in x:
            #the encode(ascii,ignore) will convert text to ascii and ignore other
            td = item['created_at']
            twt_date = datetime.date(int(td[26:30]), int(time.strptime(td[4:7],'%b').tm_mon), int(td[8:10]))
            fix_nm = item['user']['screen_name']
            try:
                if str(item['user']['name']).encode('utf8','ignore'): fix_nm = str(item['user']['name'])
            except:
                fix_nm = item['user']['screen_name']

            try:
                fix_text = text_sanitize(item['text'].encode('utf8','ignore'))
            except:
                #print 'something wrong with the text in tweet for: ',in_user
                fix_text = 'Did not process'
                #print fix_text,'\t',type(item['text']),'\t',len(item['text']),'\t',item['text'],
               
            twt_list_data = [twt_date] + [fix_nm.lower()] + [fix_text]
            try:
                base_twit_list.append(twt_list_data)
            except:
                print '<p>Unknown Error:', type(twt_list_data), twt_list_data, '</p>'
            textitem = fix_text
            newhastags = re.findall('[#]\w+',textitem)
            newatitems = re.findall('[@]\w+',textitem)
            re_tweets = re.findall('RT',textitem)
            #before adding to the final lists, convert the hashtags and atitems
            #to lower case.  This will avoid issues of double counting same names
            newhastags = [hti.lower() for hti in newhastags]
            newatitems = [ati.lower() for ati in newatitems]
            #Now add to the list.  
            #Use EXTEND function that adds elements to the list rahter than another list.
            hashtag_list.extend(newhastags)       
            at_list.extend(newatitems)            
            re_twt_list.extend(re_tweets)
            
        #now try to find some patterns in the last 200 tweets
        #print 'use the collections library to find out the top 5'
        #Version 2.6 of python does not support Counters within collections
        #py2.6    hashcollect = collections.Counter(hashtag_list)
        #py2.6    atcollect = collections.Counter(at_list)
        totalretweets = len(re_twt_list)
        retwpercent = (1.0 * totalretweets / max(1,len(x)) ) * 100
        top10users = []
        #print '\n.............................' ,'</p>' 
        print >> t2, '<li>', '\t',"%.2f%%" % retwpercent, 'are retweets (',totalretweets,'of a total of',len(x),'tweets)' ,'</li>' 
        print >> t2, '<ul>'
        print >> t2, '<li>',(len(x)-totalretweets), 'tweets in ',twit_day_range,' days (without retweets)</li>'
        print >> t2, '<li>','Avg of ','%.1f' %( 1.0*(len(x)-totalretweets)/max(twit_day_range,1) ),'tweets per day (without retweets)</li>' 
        print >> t2, '</ul></ul>' 
        data_for_plots.extend([totalretweets])

        print >> t2, '<ul>'
        print >> t2, '<li>', '\tHastags referenced over past',len(x),'tweets = ',len(hashtag_list) ,'</li>' 
        print >> t2, '<li>', '\t10 Most referenced hashtags' ,'</li>' 
        print >> t2, '<ul>'
        #py2.6    for h_item in hashcollect.most_common(10):    #can't use in python 2.6
        for h_item in top_list(hashtag_list,10):
            print >> t2, '<li>',text_sanitize(h_item[1]),'|',h_item[0] ,'</li>' 
        
        print >> t2, '</ul></ul>'
        print >> t2, '<ul>'
        print >> t2, '<li>', '\tTwitter IDs referenced over past',len(x),'tweets = ',len(at_list) ,'</li>' 
        print >> t2, '<li>', '\t10 Most referenced Tweeter IDs' ,'</li>'
        print >> t2, '<ul>' 
        #py2.6    for at_item in atcollect.most_common(10):
        for at_item in top_list(at_list,10):
            print >> t2, '<li>', '\t\t',text_sanitize(at_item[1]),'|',at_item[0],'</li>'
            #add the list of users to the top10user list
            top10users.append(at_item[1].replace('@',''))
        
        print >> t2, '</ul></ul>'
        #print '<p>Twit list:',type(base_twit_list),'\t',len(base_twit_list),'</p>'    
        return top10users, base_twit_list, data_for_plots



        
def display_data(scn_name):
    html_start()
    print '<div id="body_sty">'
    
    print '<h4>Data shown for '+scn_name.upper()+' and 10 other users most referenced in '+scn_name.upper()+'\'s tweets.</h4><hr>'
    
    user_to_check = scn_name  
    
    if user_to_check[0] == '@':
        user_raw = user_to_check
        user_to_check = user_raw.replace('@','')
        
    # the following lines get the user info
    # -- this is response limited to 180
    #user_public_info(user_to_check)

    max_items_to_show = 200
    max_tweets_to_get = 200

    #if temp file exists, close it
    global t2
    try:
        t2.close()
    except:
        print ''

    #open the temp file
    t2=TemporaryFile()
    print >> t2, '''
        <a href="#" onclick="show_hideStuff('detailed_data'); return false;">
        <br><br><hr><br>
        <h3>Detailed Data (click to see or hide)</h3></a><br>
        <div id="detailed_data" style="display:none">
        ''' 
    
    # last xx tweets is response limited to 180
    res_last200_tweets = get_last200_tweets(user_to_check.lower())
    #print '<p>', type(res_last200_tweets), len(res_last200_tweets), '</p>'
    final_tweet_list = []
    final_data_for_plots = []
    do_rest_of_display_data = 0
    try:
        user_reference = res_last200_tweets[0]
        tweet_last200_tweets = res_last200_tweets[1]
        final_tweet_list.append(tweet_last200_tweets)
        final_data_for_plots.append(res_last200_tweets[2])
        do_rest_of_display_data = 1
    except:
        print '<p>Something wrong to get the list of twitter IDs</p>'

    if (do_rest_of_display_data == 1):
        print >> t2, '<br>'
        try:
            if len(user_reference) > 0:
                for newuser in user_reference:
                    if newuser != user_to_check:
                        res_last200_tweets = get_last200_tweets(newuser.lower())
                        tweets_from_res_last200 = res_last200_tweets[1]
                        final_tweet_list.append(tweets_from_res_last200)
                        final_data_for_plots.append(res_last200_tweets[2])
            else:
                print >>t2, '<p>', 'Did not find any instance of other users referenced in your tweets.' ,'</p>' 
        except:
            print >>t2, '<p>', 'No info found.' ,'</p>' 
            
        #Add the data to the temp file also
               
        print >> t2, '<br><br><hr><h4>List of Tweets Analyzed</h4>'
        print >> t2, '<table id="table1" class="pure-table" width=100% style="display: block;">'
        print >> t2, '<thead><tr bgcolor=#def><td>Date</td><td>Sender</td><td>Text</td></tr></thead>'
        row_even = True
        for i1 in final_tweet_list:
            for i2 in i1:
                #database fields: current date, username, screen name, twt_date, twt_writer, twt_text
                twts = [datetime.date.today(),scn_name,user_to_check,i2[0],text_sanitize(i2[1]),text_sanitize(i2[2])]
                try:
                    if row_even == True:
                        print >> t2, '<tr><td><sm>', twts[3] ,'</sm></td><td><sm>', str(twts[4]),'</sm></td><td><sm>', str(twts[5]),'</sm></td></tr>'
                        row_even = False
                    else:
                        print >> t2, '<tr class="pure-table-odd"><td><sm>', twts[3] ,'</sm></td><td><sm>', str(twts[4]),'</sm></td><td><sm>', str(twts[5]),'</sm></td></tr>'                        
                        row_even = True
                except:
                    print '',

        print >> t2, '</table>'


        
        #print out the chart data
        #data fields: screen_name, friends, followers, msgs, daterange, tweets, retweets
        #print json.dumps(final_data_for_plots,indent=2)

        #try doing a chart

        #draw a chart showing friends and followers
        
        print '<h3>Friends and Followers</h3>'
        x_fdfp = []
        y1_fdfp = []
        y2_fdfp = []
        #print '<p>Before adding data:',x_fdfp, y_fdfp, '</p>'
        x_fdfp.append( 'Screen Name'   )
        y1_fdfp.append(  'Friends'  )
        y2_fdfp.append(  'Followers'  )
        for xy1 in range(len(final_data_for_plots)):
            x_fdfp.append(  final_data_for_plots[xy1][0]   )
            y1_fdfp.append(  final_data_for_plots[xy1][1]  )
            y2_fdfp.append(  final_data_for_plots[xy1][2]  )
           
        two_bar_chart_data("Friends and Followers", x_fdfp, y1_fdfp, y2_fdfp)


        print '<h3>Followers to Friends Ratio</h3>'
        #Draw a bar chart to show followers to friends ratio
        x_fdfp = []
        y_fdfp = []
        #print '<p>Before adding data:',x_fdfp, y_fdfp, '</p>'
        for xy1 in range(len(final_data_for_plots)):
            x_fdfp.append(  final_data_for_plots[xy1][0]   )
            y_fdfp.append(  round( 1.0 * final_data_for_plots[xy1][2] / max(final_data_for_plots[xy1][1],1),1)   )
            #print '<p>',x_fdfp, y_fdfp, '</p>'
           
        bar_chart_data("Followers to Friends Ratio", x_fdfp, y_fdfp)

        print '<h3>Tweets sent per day</h3>'
        x_fdfp = []
        y1_fdfp = []
        y2_fdfp = []
        #print '<p>Before adding data:',x_fdfp, y_fdfp, '</p>'
        x_fdfp.append( 'Screen Name'   )
        y1_fdfp.append(  'Tweets per day - with retweets'  )
        y2_fdfp.append(  'Tweets per day - without retweets'  )
        for xy1 in range(len(final_data_for_plots)):
            x_fdfp.append(  final_data_for_plots[xy1][0]   )
            y1_fdfp.append( final_data_for_plots[xy1][5] / max(final_data_for_plots[xy1][4],1)  )
            y2_fdfp.append( (final_data_for_plots[xy1][5]-final_data_for_plots[xy1][6]) / max(final_data_for_plots[xy1][4],1)  )
           
        two_bar_chart_data("Tweets sent per day", x_fdfp, y1_fdfp, y2_fdfp)


        print '<h3>Tweet range (tweets seen per day)</h3>'
        x_fdfp = []
        y_fdfp = []
        #print '<p>Before adding data:',x_fdfp, y_fdfp, '</p>'
        for xy1 in range(len(final_data_for_plots)):
            x_fdfp.append(  final_data_for_plots[xy1][0]   )
            y_fdfp.append(  round( 1.0 * final_data_for_plots[xy1][2] * final_data_for_plots[xy1][5] / max(final_data_for_plots[xy1][4],1) ) )
            #print '<p>',x_fdfp, y_fdfp, '</p>'
           
        bar_chart_data("Tweet Range", x_fdfp, y_fdfp)

        lex_anal(final_tweet_list)
        
        #print out the detailed data
        # go to the first record of the temp file first
        print >> t2, '    </div>        '

        t2.seek(0)
        print t2.read()
        t2.close()
        
        #if this works - can delete below this.
        
    else:
        print '<p>Not able to process this user.  Please try another.</p>'
    
    print '</div>'        #close the body_sty div
    html_end()


def lex_anal(incomingTweetList):
    '''
    routine to do lexical analysis
    '''
    #final_tweet_list --- date / sender full name / tweet
    #read the tweets and create a list of sender-htag and sender-@
    #incoming TweetList has two layer lists
    sender_htag = []
    sender_at = []
    h_tags_all = []
    at_items_all = []
    ts_all = []
    
    for lex2 in incomingTweetList:
        for lex22 in lex2:
            td = lex22[0]            #this is the tweet date
            try:
                ts = text_sanitize(lex22[1])            #this is the tweet sender
            except:
                print 'something wrong with ',lex22[1]
                ts = '---'
            ts_all.append(ts)
            h_tags = re.findall('[#]\w+',lex22[2])        #these are the h-tags
            at_items = re.findall('[@]\w+',lex22[2])    #these are the other users
            h_tags = [hti.lower() for hti in h_tags]
            at_items = [ati.lower() for ati in at_items]

            for h2 in h_tags:
                sender_htag.append([td,ts.lower()+'-'+h2])
                h_tags_all.append(h2)
                   
            for at2 in at_items:
                sender_at.append([td,ts.lower()+'-'+at2])
                at_items_all.append(at2)
                    
    
    #summarize the two new lists
    #print type(sender_htag), len(sender_htag)
    #print sender_htag[:10]
    #print type(sender_at), len(sender_at)
    #print sender_at[:10]
    
    #following lists don't have dates
    sender_htag2 = [xx[1] for xx in sender_htag]
    sender_at2 = [yy[1] for yy in sender_at]
    
    #make a list of the tweet senders only
    ts_all = list(set(ts_all))
    #print ts_all

    #get the top 10 htags
    #py2.6    ht_col = collections.Counter(h_tags_all)
    htag_data4heatmap = []
    at_data4heatmap = []
    #print '<ul>Top 10 Hashtags'
    #py2.6    for h_item in ht_col.most_common(10):
    for h_item in top_list(h_tags_all,10):
        #print '<li>', h_item, '</li>'
        #count the number of times each of the hastag was referenced by each tweet sender
        try:
            for tsitem in ts_all:
                try:
                    itemtocount = str(tsitem+'-'+h_item[1])
                    htag_data4heatmap.append([tsitem,h_item[1], sender_htag2.count(itemtocount)])
                except:
                    print 'Problem here: ',h_item,tsitem
        except:
            print 'Problem here',h_item

    print '</ul>'
     
    #get the top 10 user references
    #py2.6   at_col = collections.Counter(at_items_all)
    #print '<ul>Top 10 Users'
    #py2.6   for a_item in at_col.most_common(10):
    for a_item in top_list(at_items_all,10):
        #print '<li>', a_item, '</li>' 
        #count the number of times each of the hastag was referenced by each tweet sender
        try:
            for tsitem in ts_all:
                itemtocount = str(tsitem+'-'+a_item[1])
                at_data4heatmap.append([tsitem,a_item[1], sender_at2.count(itemtocount)])
        except:
            print 'Problem here 2',a_item

    print '</ul>'

    #draw the table with the heatmap
    tcols = len(ts_all)                        #number of tweet senders - rows
    trows = len(htag_data4heatmap) / tcols     #number of hastags - cols
    #print trows, tcols
    if trows>0: 
        print '<br><br>'
        print '<h3>Most Popular Hashtags</h3>'
        heatmap_table(trows,tcols,htag_data4heatmap)

    tcols = len(ts_all)                        #number of tweet senders - rows
    trows = len(at_data4heatmap) / tcols     #number of hastags - cols
    #print trows, tcols
    if trows>0: 
        print '<br><br>'
        print '<h3>Most Referenced Users</h3>'
        heatmap_table(trows,tcols,at_data4heatmap)
    
    
    
    
def heatmap_table(trows,tcols,hm):
    #calculate the max and min of the references
    #and create a normalized color scale
    mx = max(i[2] for i in hm)
    mn = min(i[2] for i in hm)
    itv = mx - mn
    #COLOR pallete from http://colorbrewer2.org/
    for arow in hm:
        rval = 1.0*arow[2]/itv
        if rval<0.1:
            arow[2]='#FFF5F0'
        elif rval>=0.1 and rval<0.25:
            arow[2]='#FEE0D2'
        elif rval>=0.25 and rval<0.4:
            arow[2]='#FCBBA1'
        elif rval>=0.4 and rval<0.5:
            arow[2]='#FC9272'
        elif rval>=0.5 and rval<0.6:
            arow[2]='#FB6A4A'
        elif rval>=0.6 and rval<0.7:
            arow[2]='#EF3B2C'
        elif rval>=0.7 and rval<0.8:
            arow[2]='#CB181D'
        elif rval>=0.8 and rval<0.9:
            arow[2]='#A50F15'
        elif rval>=0.9:
            arow[2]='#67000D'

    
    print '<table width=100% style="display: block;">       '
    for i in range(trows+1):
        print '<tr>',
        for j in range(tcols+1):
            if (i==0 and j==0):
                print '<td width="15%">','','</td>',
            elif i==0 and j>0 and j<(tcols):
                print '<td width="8.5%"><sm>',hm[j-1][0][:10],'</sm></td>',
            elif i==0 and j==(tcols):
                print '<td width="8.5%"><sm>',hm[j-1][0][:10],'</sm></td></tr>'
            elif i>0 and j==0:
                print '<td><sm>',hm[(i-1)*tcols+j+1-1][1],'</sm></td>',
            elif i>0 and j>0 and j<tcols:
                print '<td bgcolor=',hm[(i-1)*tcols+j-1][2],'></td>',
            elif i>0 and j==tcols:
                print '<td bgcolor=',hm[(i-1)*tcols+j-1][2],'></td></tr>'
  
    print '</table>      '
   

  
def print_detailed_tweets(in_usertocheck):
    html_start()
    check_another_user_button()
    #print '<h3>Listing of tweets analyzed:</h3>'
    sd2st = start_database_to_store_tweets()
    if sd2st[1] == True:
        c2 = sd2st[0]
        conn2 = sd2st[2]
        #read all the tweets for the username and screen name
        read_text = "SELECT * FROM tweetlist WHERE (username =\'"+in_usertocheck+"\')"
        #print '<p>Select tweet command:',read_text,'</p>'
        try:
            c2.execute(read_text)
            for crow in c2:
                print crow[1]
            conn2.close()
            #print '<h2>Finished with the tweet list</h2>'
        except conn2.Error, e:
            print "E Error %d: %s" % (e.args[0], e.args[1])
    else:
        print "F Error %d: %s" % (sd2st[0].args[0],sd2st[0].args[1])
            
    html_end()


def bar_chart_data(cht_title,xdata,ydata):
    #this routine will draw a bar chart
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    print '<!--Load the AJAX API-->'
    print '<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>'
    print '<script type=\"text/javascript\">'

    # Load the Visualization API and the piechart package. 
    print '  google.load(\'visualization\', \'1.0\', {\'packages\':[\'corechart\']}); '

    # Set a callback to run when the Google Visualization API is loaded.
    print '  google.setOnLoadCallback(drawChart);'

    # Callback that creates and populates a data table, 
    # instantiates the pie chart, passes in the data and
    # draws it.
    print '  function drawChart() {  '


    #print '<p>Inside chart middle</p>'
    # Create the data table.
    print '    var data = new google.visualization.arrayToDataTable([  '
    print '    [   \'Screen Name\', \' ' , cht_title, ' \', {role:\'style\'} ],        '
    for cdi in range(len(xdata)):
        if cdi == 0:
            print "  [ \'", xdata[cdi], "\',",  ydata[cdi], ", \'orange\' ], "
        else:
            print "  [ \'", xdata[cdi], "\',",  ydata[cdi], ", \'blue\' ], "

    #print '      [\'\', 0]  '
    print '    ]);  '

    #Set chart options
    print "    var options = {\'title\':\'",cht_title,"\',  "
    print '                   \'width\':600,  '
    print '                   \'height\':400, '
    print '                   \'hAxis\' : {\'logScale\' : true}  ,      '
    print '                   legend :\'none\' , \'backgroundColor\': { fill: \"none\" }  '
    print '                               };  '

    # chart_bottom():
    # Instantiate and draw our chart, passing in some options.
    print '    var chart = new google.visualization.BarChart(document.getElementById(\"',cht_title+'DIV','\"));  '
    print '    function selectHandler() {  '
    print '      var selectedItem = chart.getSelection()[0];  '
    print '      if (selectedItem) {  '
    print '        var topping = data.getValue(selectedItem.row, 0);  '
    print '        alert(\'The user selected \' + topping);  '
    print '      }  '
    print '    }  '

    print '    google.visualization.events.addListener(chart, \'select\', selectHandler);      '
    print '    chart.draw(data, options);  '
    print '  }  '

    print '</script>  '
    print '<!--Div that will hold the pie chart-->  '
    print '<div id=\"',cht_title+'DIV','\" style=\"width:600; height:400\"></div>  '


def two_bar_chart_data(cht_title,xdata,ydata1,ydata2):
    #this routine will draw a bar chart with two bara
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    print '<!--Load the AJAX API-->'
    print '<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>'
    print '<script type=\"text/javascript\">'

    # Load the Visualization API and the piechart package. 
    print '  google.load(\'visualization\', \'1.0\', {\'packages\':[\'corechart\']}); '

    # Set a callback to run when the Google Visualization API is loaded.
    print '  google.setOnLoadCallback(drawChart);'
    print '  function drawChart() {  '
    print '    var data = new google.visualization.arrayToDataTable([  '
    print "    [   \'Screen Name\', \' ",ydata1[0], "\' ,{role:\'style\'},    \'" ,ydata2[0], "\' , {role:\'style\'} ],        "
    for cdi in range(len(xdata)):
        if cdi>0:
            print "  [ \'", xdata[cdi], "\',",  ydata1[cdi],",\'blue\',", ydata2[cdi], ", \'red\' ], "

    #print '      [\'\', 0]  '
    print '    ]);  '

    #Set chart options
    print "    var options = {\'title\':\'",cht_title,"\',  "
    print '                   \'width\':600,  '
    print '                   \'height\':400, '
    print '                   \'hAxis\' : {\'logScale\' : false}  ,      '
    print '                   legend :\'top\' , \'backgroundColor\': { fill: \"none\" }   '
    print '                               };  '

    # chart_bottom():
    # Instantiate and draw our chart, passing in some options.
    print '    var chart = new google.visualization.BarChart(document.getElementById(\"',cht_title+'DIV','\"));  '
    print '    function selectHandler() {  '
    print '      var selectedItem = chart.getSelection()[0];  '
    print '      if (selectedItem) {  '
    print '        var topping = data.getValue(selectedItem.row, 0);  '
    print '        alert(\'The user selected \' + topping);  '
    print '      }  '
    print '    }  '

    print '    google.visualization.events.addListener(chart, \'select\', selectHandler);      '
    print '    chart.draw(data, options);  '
    print '  }  '

    print '</script>  '
    print '<!--Div that will hold the pie chart-->  '
    print '<div id=\"',cht_title+'DIV','\" style=\"width:600; height:400\"></div>  '


def test3():
    #Test some random twitter functions on stream data
    html_start()
    testname = "concession,privatization,public private"
    #testname = "mining,mines,metal,oil,gas,petroleum"
   
    try:
        ts = TwitterStream(auth=OAuth(define_keys()[2],define_keys()[3],define_keys()[0],define_keys()[1]))
 
        #response = ts.statuses.sample()
        response = ts.statuses.filter(track=testname)
        
        showcount = 0
        maxshow = 50
        for tweet in response:
            showcount += 1
            if showcount>= maxshow: break

            # You must test that your tweet has text. It might be a delete
            # or data message.
            if tweet is None:
                print_para("-- None --")
            elif tweet.get('text'):
                print_para(tweet['user']['name']+'.....'+str(twit_date(tweet['created_at']))+'---'+tweet['text'])
            else:
                print_para(str(showcount)+'...')
                #print_para(json.dumps(tweet,indent=2))
        
    except TwitterHTTPError, e:
        print '<p>Error getting tweets info for:',e['details'],'</p>' 

        
    html_end()
    
    
def print_para(instr):
    print '<p>',instr,'</p>'

    
def twit_date(in_created_at):
    out_date = datetime.date(int(in_created_at[26:30]), int(time.strptime(in_created_at[4:7],'%b').tm_mon), int(in_created_at[8:10]))
    return out_date

    
def test2(inin,inin2):
    html_start()
    print '<p>Something wrong - cannot print tweet list for',inin,inin2,'</p>'
    html_end()


# Define main function.
def main():
    form = cgi.FieldStorage()
    if (form.has_key("action") and form.has_key("scn_name")):
        if (form["action"].value == "display"):
            display_data(text_sanitize(form["scn_name"].value))
    else:
        generate_form()



main()
