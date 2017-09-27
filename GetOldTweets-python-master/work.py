# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:26:25 2017

@author: sentifi
"""

# -*- coding: utf-8 -*-
import sys, codecs

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def getTweet(query, since, until, filename):

    try:
        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = filename

        tweetCriteria.since = since
        tweetCriteria.until = until
        tweetCriteria.querySearch = query

        outputFile = codecs.open(outputFileName, "w+", "utf-8")

        outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

        print('Searching...\n')
        print('KW: ' + query + ' since: ' + since + ' until: ' + until)
        def receiveBuffer(tweets):
            for t in tweets:
                outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
            outputFile.flush();
            print('More %d saved on file...\n' % len(tweets))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except:
        raise
    finally:
        outputFile.close()
        print('Done. Output file generated "%s".' % outputFileName)


keyword = ['bundestagswahl%20OR%20bundestagswahlen', 'german%20election%20OR%20elections', '%23merkel%20OR%20%23gehwaehlen%20OR%20%23gehwählen%20OR%20%23btw13%20OR%20%23fragmanuela%20OR%20%23vorwärtsSPD%20OR%20%2372hSPD%20OR%20%23CDU%20OR%20%23fragPeer%20OR%20%23wiebitte']
since = ['2013-01-01','2013-02-01','2013-03-01','2013-04-01','2013-05-01', \
         '2013-06-01','2013-07-01','2013-08-01','2013-09-01','2013-09-15', \
         '2013-09-20','2013-09-23','2013-10-01','2013-11-01','2013-12-01']
until = ['2013-02-01','2013-03-01','2013-04-01','2013-05-01','2013-06-01', \
         '2013-07-01','2013-08-01','2013-09-01','2013-09-15','2013-09-20', \
         '2013-09-23','2013-10-01','2013-11-01','2013-12-01','2014-01-01']
workList = []
for kw in keyword:
    for i in range(len(since)):
        filename = kw + since[i] + until[i] + '.csv'
        workList.append([kw, since[i], until[i], filename])
        
count = -1
count += -1
for j in workList[42:]:
    count+=1
    print(count)
    getTweet(*j)

    