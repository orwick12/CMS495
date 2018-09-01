##
## This program uses the several libraries to interact with RSS (really simple syndication)
## newspaper feeds. RSS feeds provide an easy way to identify and download relevant articles
## from web sources, extract relevant metadata, and perform additional process on the
## resulting articles.
##
from newspaper import Article
import feedparser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from bs4 import BeautifulSoup
import nltk

## We will use the NLTK sentiment analyzer in order to generate very
## basic positive/negative scores off the text of each article
##
sid = SentimentIntensityAnalyzer()

## listing of several RSS feeds from newspapers across the US
##
## we'll use the CNN US top news story feed for this program
##
## currentStories = feedparser.parse('http://chicagotribune.feedsportal.com/c/34253/f/622872/index.rss')
## currentStories = feedparser.parse('http://rss.cnn.com/rss/cnn_topstories.rss')
## currentStories = feedparser.parse('http://rss.cnn.com/rss/cnn_world.rss')

## connect our program up to the RSS feed and pull down
## the feed contents
##
currentStories = feedparser.parse('http://rss.cnn.com/rss/cnn_us.rss')

## now iterate through the list of stories on from the RSS feed and
## print all posts including the title, authors, publication date,
## and overall positive/negative sentiment rankings
##
for currentStory in currentStories.entries:
	currArticle = Article(currentStory.link) ## the link holds the URL to the actual news story
	currArticle.download() ## download the text of the news story
	currArticle.parse()
	print ("-----------------------------------------")
	print (currArticle.title)
	print (currArticle.authors)
	print (currArticle.publish_date)
	print (currArticle.text[:50])
##	print (currArticle.text)

	## reset our positive/negative counters to 0
	totPos = 0.0
	totNeg = 0.0

	## extract a list of sentences that make up the article
	articleSentences = nltk.sent_tokenize(currArticle.text)

	## for each sentence in the list
	## calculate a sentiment score for the sentence and
	## update the counters with the positive and negative
	## scores
	##
	for sentence in articleSentences:
		sentRating = sid.polarity_scores(sentence)
		totPos += sentRating['pos']
		totNeg += sentRating['neg']

	## print out the scores for each article
	##
	print ('Positive Score: ' + str(totPos))
	print ('Negative Score: ' + str(totNeg))

	print ("===========================================\n")
