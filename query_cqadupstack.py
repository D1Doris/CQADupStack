#!/usr/bin/env python

# Copyright 2015 Doris Hoogeveen (doris dot hoogeveen at gmail)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, re, sys
import nltk, json, codecs
import pydoc, math
import zipfile, random, datetime
import itertools
from operator import truediv
from scipy.misc import comb
from random import randrange
from HTMLParser import HTMLParser

# Written by Doris Hoogeveen Nov 2015. For a usage please call the script without arguments.

def load_subforum(subforumzipped):
    ''' Takes a subforum.zip file as input and returns a StackExchange Subforum class object.'''
    return Subforum(subforumzipped)

class Subforum():
    def __init__(self, zipped_catfile):
	''' This class takes a StackExchange subforum.zip file as input and makes it queryable via the methods below. '''
	# Check to see if supplied file exists and is a valid zip file.
	if not os.path.exists(zipped_catfile):
	    sys.exit('The supplied zipfile does not exist. Please supply a valid StackExchange subforum.zip file.')
 	if not zipfile.is_zipfile(zipped_catfile):
	    sys.exit('Please supply a valid StackExchange subforum.zip file.')

	self.cat = os.path.basename(zipped_catfile).split('.')[0]
	self._unzip_and_load(zipped_catfile)	

	# Stopwords for cleaning. They need to be initialised here in case someone accesses self.stopwords.

	self.__indri_stopwords = ['a', 'about', 'above', 'according', 'across', 'after', 'afterwards', 'again', 'against', 'albeit', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'apart', 'are', 'around', 'as', 'at', 'av', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'but', 'by', 'can', 'cannot', 'canst', 'certain', 'cf', 'choose', 'contrariwise', 'cos', 'could', 'cu', 'day', 'do', 'does', "doesn't", 'doing', 'dost', 'doth', 'double', 'down', 'dual', 'during', 'each', 'either', 'else', 'elsewhere', 'enough', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'except', 'excepted', 'excepting', 'exception', 'exclude', 'excluding', 'exclusive', 'far', 'farther', 'farthest', 'few', 'ff', 'first', 'for', 'formerly', 'forth', 'forward', 'from', 'front', 'further', 'furthermore', 'furthest', 'get', 'go', 'had', 'halves', 'hardly', 'has', 'hast', 'hath', 'have', 'he', 'hence', 'henceforth', 'her', 'here', 'hereabouts', 'hereafter', 'hereby', 'herein', 'hereto', 'hereupon', 'hers', 'herself', 'him', 'himself', 'hindmost', 'his', 'hither', 'hitherto', 'how', 'however', 'howsoever', 'i', 'ie', 'if', 'in', 'inasmuch', 'inc', 'include', 'included', 'including', 'indeed', 'indoors', 'inside', 'insomuch', 'instead', 'into', 'inward', 'inwards', 'is', 'it', 'its', 'itself', 'just', 'kind', 'kg', 'km', 'last', 'latter', 'latterly', 'less', 'lest', 'let', 'like', 'little', 'ltd', 'many', 'may', 'maybe', 'me', 'meantime', 'meanwhile', 'might', 'moreover', 'most', 'mostly', 'more', 'mr', 'mrs', 'ms', 'much', 'must', 'my', 'myself', 'namely', 'need', 'neither', 'never', 'nevertheless', 'next', 'no', 'nobody', 'none', 'nonetheless', 'noone', 'nope', 'nor', 'not', 'nothing', 'notwithstanding', 'now', 'nowadays', 'nowhere', 'of', 'off', 'often', 'ok', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'own', 'per', 'perhaps', 'plenty', 'provide', 'quite', 'rather', 'really', 'round', 'said', 'sake', 'same', 'sang', 'save', 'saw', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'seldom', 'selves', 'sent', 'several', 'shalt', 'she', 'should', 'shown', 'sideways', 'since', 'slept', 'slew', 'slung', 'slunk', 'smote', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'spake', 'spat', 'spoke', 'spoken', 'sprang', 'sprung', 'stave', 'staves', 'still', 'such', 'supposing', 'than', 'that', 'the', 'thee', 'their', 'them', 'themselves', 'then', 'thence', 'thenceforth', 'there', 'thereabout', 'thereabouts', 'thereafter', 'thereby', 'therefore', 'therein', 'thereof', 'thereon', 'thereto', 'thereupon', 'these', 'they', 'this', 'those', 'thou', 'though', 'thrice', 'through', 'throughout', 'thru', 'thus', 'thy', 'thyself', 'till', 'to', 'together', 'too', 'toward', 'towards', 'ugh', 'unable', 'under', 'underneath', 'unless', 'unlike', 'until', 'up', 'upon', 'upward', 'upwards', 'us', 'use', 'used', 'using', 'very', 'via', 'vs', 'want', 'was', 'we', 'week', 'well', 'were', 'what', 'whatever', 'whatsoever', 'when', 'whence', 'whenever', 'whensoever', 'where', 'whereabouts', 'whereafter', 'whereas', 'whereat', 'whereby', 'wherefore', 'wherefrom', 'wherein', 'whereinto', 'whereof', 'whereon', 'wheresoever', 'whereto', 'whereunto', 'whereupon', 'wherever', 'wherewith', 'whether', 'whew', 'which', 'whichever', 'whichsoever', 'while', 'whilst', 'whither', 'who', 'whoa', 'whoever', 'whole', 'whom', 'whomever', 'whomsoever', 'whose', 'whosoever', 'why', 'will', 'wilt', 'with', 'within', 'without', 'worse', 'worst', 'would', 'wow', 'ye', 'yet', 'year', 'yippee', 'you', 'your', 'yours', 'yourself', 'yourselves']
	self.__short_stopwords = ['a', 'an', 'the', 'yes', 'no', 'thanks']
        self.__middle_stopwords = ['in', 'on', 'at', 'a', 'an', 'is', 'be', 'was', 'I', 'you', 'the', 'do', 'did', 'of', 'so', 'for', 'with', 'yes', 'thanks']

	# The NLTK stopwords cause a problem if they have not been downloaded, so we need a check for that.
	try:	
	    self.__nltk_stopwords = nltk.corpus.stopwords.words('english')
	except:
	    self.__nltk_stopwords = []

	self.__stopwords = self.__middle_stopwords # Default.
	self.cutoffdate = False # Needed for classification splits.


    def _unzip_and_load(self, zipped_catfile):
	ziplocation = os.path.dirname(zipped_catfile)
	cat = os.path.basename(zipped_catfile).split('.')[0]
	questionfile = ziplocation + '/' + cat + '/' + cat + '_questions.json'
	answerfile = ziplocation + '/' + cat + '/' + cat + '_answers.json'
	commentfile = ziplocation + '/' + cat + '/' + cat + '_comments.json'
	userfile = ziplocation + '/' + cat + '/' + cat + '_users.json'
	if os.path.exists(questionfile) and os.path.exists(answerfile) and os.path.exists(userfile) and os.path.exists(commentfile):
	    pass # All good, we don't need to unzip anything
	else:
	    zip_ref = zipfile.ZipFile(zipped_catfile, 'r')
	    zip_ref.extractall(ziplocation)

	qf = codecs.open(questionfile, 'r', encoding='utf-8')
        self.postdict = json.load(qf)

	af = codecs.open(answerfile, 'r', encoding='utf-8')
        self.answerdict = json.load(af)

        cf = codecs.open(commentfile, 'r', encoding='utf-8')
        self.commentdict = json.load(cf)

	uf = codecs.open(userfile, 'r', encoding='utf-8')
        self.userdict = json.load(uf)

        print "Loaded all data from", zipped_catfile

    def tokenize(self, s):
        ''' Takes a string as input, tokenizes it using NLTK (http://www.nltk.org) and returns a list of the tokens. '''
        return nltk.word_tokenize(s) # The NLTK tokenizer cuts things like 'cannot' into 'can' and 'not'.


    ########################
    # GENERAL POST METHODS #
    ########################

    def get_posts_with_duplicates(self):
        ''' Takes no input and returns a list of all posts that have at least one duplicate. '''
        dups = []
        for p in self.postdict:
            if len(self.postdict[p]['dups']) > 0:
                dups.append(p)
        return dups

    def get_posts_without_duplicates(self):
        ''' Takes no input and returns a list of all posts that don't have any duplicates. '''
        nodups = []
        for p in self.postdict:
            if len(self.postdict[p]['dups']) == 0:
                nodups.append(p)
        return nodups

    def get_posts_with_and_without_duplicates(self):
        ''' Takes no input and returns two lists: one with all posts that have at least one duplicate, and one with all posts that don't have any duplicates. In that order.
            Calling this method is quicker than calling get_posts_with_duplicates() followed by get_posts_without_duplicates() is you want both dups and non-dups. '''
        nodups = []
        dups = []
        for p in self.postdict:
            if len(self.postdict[p]['dups']) == 0:
                nodups.append(p)
            else:
                dups.append(p)
        return dups, nodups

    def get_ordered_list_of_posts(self):
        ''' Takes no input and returns a list of tuples (postid, datetime object), ordered chronologically from newest to oldest post. '''
        return sorted([(i, datetime.datetime.strptime(self.get_postdate(i), '%Y-%m-%d')) for i in self.postdict], key=lambda x: x[1], reverse=True)

    def get_random_postid(self):
        ''' Takes no input and returns a random post id. '''
        allids = self.postdict.keys()
        return random.choice(allids)

    def get_random_pair_of_posts(self):
        ''' Takes no input and returns a tuple with two random post ids and a duplicate verdict. The second is always lower than the first. 
            Example: (4865, 553, 'dup')
            Other values for the verdict are: 'related' and 'nondup'. '''
        allids = self.postdict.keys()
        id1 = random.choice(allids)
        id2 = random.choice(allids)
        while id2 >= id1:
            id2 = random.choice(allids)
        if id2 in self.postdict[id1]['dups']:
            return (id1, id2, 'dup')
        elif id2 in self.postdict[id1]['related']:
            return (id1, id2, 'related')
        else:
            return (id1, id2, 'nondup')

    def get_all_postids(self):
        ''' Takes no input and returns a list of ALL post ids. '''
        return self.postdict.keys()

    def get_true_label(self, postid1, postid2):
	''' Takes two postids as input and returns the true label, which is one of "dup", "nodup" or "related". '''
	if postid1 in self.postdict[postid2]['dups']:
	    return "dup"
	elif postid1 in self.postdict[postid2]['related']:
	    return "related"
	elif postid2 in self.postdict[postid1]['dups']:
	    return "dups"
	elif postid2 in self.postdict[postid1]['related']:
            return "related"
	else:
	    return "nodup"

    ###########################
    # PARTICULAR POST METHODS #
    ###########################

    def get_posttitle(self, postid):
	''' Takes a post id as input and returns the title of the post. '''
	return self.postdict[postid]["title"]

    def get_postbody(self, postid):
	''' Takes a post id as input and returns the body of the post. '''
	return self.postdict[postid]["body"]

    def get_post_title_and_body(self, postid):
	''' Takes a post id as input and returns the title and the body of the post together as one string, so in other words, the full initial post. '''
	t = self.postdict[postid]["title"]
	b = self.postdict[postid]["body"]
	return t + ' ' + b

    def get_postdate(self, postid):
	''' Takes a post id as input and returns the date the post was posted in YYYY-MM-DD format. '''
	cdate = datetime.datetime.strptime(self.postdict[postid]['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
	return str(cdate.year) + '-' + cdate.strftime('%m') + '-' + cdate.strftime('%d')

    def get_posttime(self, postid):
	''' Takes a post id as input and returns the time the post was posted in HH:MM:SS format. '''
	cdate = datetime.datetime.strptime(self.postdict[postid]['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return cdate.strftime('%H') + ':' + cdate.strftime('%M') + ':' + cdate.strftime('%S')

    def get_postviewcount(self, postid):
	''' Takes a post id as input and returns the number of times the post has been looked at by users. '''
	return self.postdict[postid]["viewcount"]

    def get_postfavoritecount(self, postid):
	''' Takes a post id as input and returns an integer representing the nr of times this post has been favoured by a user.
	    More information on what that means can be found here: http://meta.stackexchange.com/questions/53585/how-do-favorite-questions-work '''
	return self.postdict[postid]['favoritecount']

    def get_postscore(self, postid):
	''' Takes a post id as input and returns the score of the post. This is the number of upvotes minus the number of downvotes is has received. '''
	return self.postdict[postid]['score']

    def get_postuserid(self, postid):
	''' Takes a post id as input and returns the userid of the person that posted it. Returns False if the user is not known. '''
	return self.postdict[postid]['userid']

    def get_duplicates(self, postid):
	''' Takes a post id as input and returns a list of ids of posts that have been labeled as a duplicate of it. '''
	return self.postdict[postid]['dups']

    def get_related(self, postid):
	''' Takes a post id as input and returns a list of ids of posts that have been labeled as related to it. '''
	return self.postdict[postid]['related']

    def get_posttags(self, postid):
        ''' Takes a post id as input and returns a list of tags. '''
        return self.postdict[postid]['tags']


    ##################
    # ANSWER METHODS #
    ##################

    def get_answers(self, postid):
        ''' Takes a post id as input and returns a list of answer ids. '''
        return self.postdict[postid]["answers"]

    def get_answercount(self, postid):
        ''' Takes a post id as input and returns an integer representing the number of answers it has received. '''
        return len(self.postdict[postid]['answers'])

    def get_answer_parentid(self, answerid):
	''' Takes an answer id as input and returns its parent id: the id of the post it is an answer of. '''
	return self.answerdict[answerid]['parentid']

    def get_acceptedanswer(self, postid):
        ''' Takes a post id as input and returns the answer id of the accepted answer if it exists, else it returns False. '''
        if 'acceptedanswer' in self.postdict[postid]:
            return self.postdict[postid]['acceptedanswer']
        else:
            return False

    def get_answerbody(self, answerid):
	''' Takes an answer id as input and returns the body of the answer. That is the text of the answer. '''
        return self.answerdict[answerid]['body']

    def get_answerdate(self, answerid):
        ''' Takes an answer id as input and returns the date the answer was posted in YYYY-MM-DD format. '''
        cdate = datetime.datetime.strptime(self.answerdict[answerid]['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return str(cdate.year) + '-' + cdate.strftime('%m') + '-' + cdate.strftime('%d')

    def get_answertime(self, answerid):
        ''' Takes an answer id as input and returns the time the answer was posted in HH:MM:SS format. '''
        cdate = datetime.datetime.strptime(self.answerdict[answerid]['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return cdate.strftime('%H') + ':' + cdate.strftime('%M') + ':' + cdate.strftime('%S')

    def get_answerscore(self, answerid):
	''' Takes an answer id as input and returns an integer representing the score of the answer. This is the number of upvotes minus the number of downvotes is has received. ''' 
        return self.answerdict[answerid]["score"]

    def get_answeruserid(self, answerid):
	''' Takes an answer id as input and returns the userid of the person that posted it. Returns False if the user is not known. '''
        return self.answerdict[answerid]['userid']

    ###################
    # COMMENT METHODS #
    ###################

    def get_post_comments(self, postid):
	''' Takes a post id as input and returns a list of comment ids. '''
	return self.postdict[postid]['comments']

    def get_answer_comments(self, answerid):
	''' Takes an answer id as in put and returns a list of comment ids. '''
	return self.answerdict[answerid]['comments']

    def get_post_commentcount(self, postid):
	''' Takes a post id as input and returns and integer representing the number of comments this post has received. '''
	return len(self.postdict[postid]['comments'])

    def get_answer_commentcount(self, answerid):
	''' Takes an answer id as input and returns and integer representing the number of comments this answer has received. '''
        return len(self.answerdict[answerid]['comments'])

    def get_comment_parentid(self, commentid):
	''' Takes a comment id as input and returns its parent id: the id of the post or answer it is a comment to. '''
        return self.commentdict[commentid]['parentid']

    def get_comment_parenttype(self, commentid):
	''' Takes a comment id as input and returns either 'question' or 'answer', depending on the type of its parent id. '''
        return self.commentdict[commentid]['parenttype']

    def get_commentbody(self, commentid):
	''' Takes a comment id as input and returns the body of the comment. '''
	return self.commentdict[commentid]['body']

    def get_commentdate(self, commentid):
	''' Takes a comment id as input and returns the date the comment was posted, in YYYY-MM-DD format. '''
	cdate = datetime.datetime.strptime(self.commentdict[commentid]['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return str(cdate.year) + '-' + cdate.strftime('%m') + '-' + cdate.strftime('%d')

    def get_commenttime(self, commentid):
 	''' Takes a comment id as input and returns the time the comment was posted, in HH:MM:SS format. '''
        cdate = datetime.datetime.strptime(self.commentdict[commentid]['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return cdate.strftime('%H') + ':' + cdate.strftime('%M') + ':' + cdate.strftime('%S')

    def get_commentscore(self, commentid):
	''' Takes a comment id as input and returns an integer representing the score of the comment. This is the number of upvotes minus the number of downvotes is has received. '''
	return self.commentdict[commentid]['score']

    def get_commentuserid(self, commentid):
	''' Takes a comment id as input and returns the id of the user that posted the comment. '''
	return self.commentdict[commentid]['userid']

    ################
    # USER METHODS #
    ################

    def get_user_reputation(self, userid):
	''' Takes a user id as input and outputs an integer representing the reputation of the user.
	    Information on what this means and how it is calculated can be found here http://stackoverflow.com/help/whats-reputation '''
	return self.userdict[userid]['rep']

    def get_user_views(self, userid):
	''' Takes a user id as input and outputs an integer representing how often people have viewed a post by this user. '''
	return self.userdict[userid]['views']

    def get_user_upvotes(self, userid):
	''' Takes a user id as input and outputs an integer representing how many upvotes on posts or answers this user has received. '''
	return self.userdict[userid]['upvotes']

    def get_user_downvotes(self, userid):
        ''' Takes a user id as input and outputs an integer representing how many downvotes on posts or answers this user has received. '''
        return self.userdict[userid]['downvotes']

    def get_user_joindate(self, userid):
	''' Takes a user id as input and outputs the date this user joined this subforum, in YYYY-MM-DD format. '''
	cdate = datetime.datetime.strptime(self.userdict[userid]['date_joined'], "%Y-%m-%dT%H:%M:%S.%f")
        return str(cdate.year) + '-' + cdate.strftime('%m') + '-' + cdate.strftime('%d')
	
    def get_user_lastaccess(self, userid):
	''' Takes a user id as input and outputs the last time this user has logged into this subforum, in YYYY-MM-DD format. '''
	cdate = datetime.datetime.strptime(self.userdict[userid]['lastaccessdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return str(cdate.year) + '-' + cdate.strftime('%m') + '-' + cdate.strftime('%d')

    def get_user_age(self, userid):
	''' Takes a user id as input and outputs the user's age as an integer, if known. Else it returns 'unknown'. '''
	if 'age' in self.userdict[userid]:
	    return self.userdict[userid]['age']
	else:
	    return 'unknown'

    def get_user_posts(self, userid):
	''' Takes a user id as input and returns a list of the question posts he/she has made. '''
	return self.userdict[userid]['questions']

    def get_user_answers(self, userid):
	''' Takes a user id as input and returns a list of the answers he/she has written. '''
        return self.userdict[userid]['answers']

    def get_user_badges(self, userid):
	''' Takes a user id as input and returns a list of the badges this user has earned. 
	    Information on what badges are and which ones can be earned can be found here: http://stackoverflow.com/help/badges '''
	return self.userdict[userid]['badges']


    ####################
    # Cleaning methods #
    ####################

    @property
    def stopwords(self):
        ''' Returns the current list of words that is used as the stop word list. It can be accessed via self.stopwords'''
        return self.__stopwords

    def supply_stopwords(self, filename):
	''' Takes as input a plain text file encoded in UTF-8 with one stop word per line and saves these internally in a stop word list.
	    This list will be used in cleaning if perform_cleaning() is called with remove_stopwords=True. '''
	self.__stopwords = []
	inputf_open = codecs.open(filename, 'r', encoding='utf-8')
	inputf = inputf_open.readlines()
	inputf_open.close()
	for line in inputf:
	    line = line.rstrip()
	    self.__stopwords.append(line)

    def change_to_default_stopwords(self, stopwordset='middle'):
	''' Changes the stopword list to one of the supplied ones: 'nltk', 'indri', 'short' or 'middle'. 'Middle' is the default.
	    The NLTK stopword list contains 127 stopwords. (http://www.nltk.org/book/ch02.html#code-unusual)
	    The Indri stopword list contains 418 stopwords. (http://www.lemurproject.org/stopwords/stoplist.dft)
	    Short = ["a", "an", "the", "yes", "no", "thanks"]
            Middle = ["in", "on", "at", "a", "an", "is", "be", "was", "I", "you", "the", "do", "did", "of", "so", "for", "with", "yes", "thanks"]
	    To be able to use the NLTK stopwords, they need to be downloaded first. See: http://www.nltk.org/data.html for more info.
	    If the data is not downloaded first, the script will default to the NLTK stopword list of November 2015.
	'''
	if stopwordset == 'nltk':
	    if self.__nltk_stopwords != []:
                self.__stopwords = self.__nltk_stopwords
	    else: # This can happen if the NLTK stopwords have not been downloaded yet. Defaulting to the NLTK stopword list of November 2015.
		self.__stopwords = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']
	elif stopwordset == 'indri':
            self.__stopwords = self.__indri_stopwords
	elif stopwordset == 'short':
	    self.__stopwords = self.__short_stopwords
	else:
	    self.__stopwords = self.__middle_stopwords # DEFAULT

    def perform_cleaning(self, s, maxcodelength=150, remove_stopwords=False, remove_punct=False, stem=False):
	''' Takes a string as input and returns a cleaned version.
	    - The string will be lowercased and newlines removed.
	    - HTML tags will be removed.
	    - Mentions of possible duplicates will be removed.
	    - URLs pointing to other StackExchange threads are turned into 'stackexchange-url'.
	    - Blocks of code will be removed.
	    - Contracted forms will be expanded. E.g. "didn't" --> "did not".
	    - '&amp;' will be turned into 'and'.
	    - Other HTML entities will be removed, and string matching the following pattern too: '&#?[a-z]+;'.
	    - Whitespace is added around punctuation
	    OPTIONAL ARGUMENTS:
	    maxcodelength: the maximum length of code blocks that will not be removed. Default: 150.
	    remove_stopwords: removed stop words. (Values: True or False)
	    remove_punct: punctuation is removed, except for punctuation in URLs and numbers. (Values: True or False)
	    stem: stemming is performed via the Porter stemmer as implemented in the NLTK (http://www.nltk.org/). (Values: True or False)
	'''
	s, codes = self._deal_with_code(s,maxcodelength)
        s = s.lower()
        s = re.sub('\n', ' ', s)
        s = self._remove_tags(s)
        s = self._expand_contractions(s)
        s = self._general_cleaning(s,codes,remove_punct)
        if remove_stopwords:
            s = self._remove_stopwords(s)
        if stem:
            s = self._stem(s)
	s = self._fix_exceptions(s)

	# TODO: consider removing dashes between hyphenated words (far-off -> faroff), and removing full stops in acronyms/initials (U.N. -> UN). It helps for METEOR apparently (http://www.cs.cmu.edu/~alavie/METEOR/pdf/meteor-wmt11.pdf). U.S.-based will become US based.

	return s


    def _fix_exceptions(self, s):
	''' Takes a string as input, applies a bunch of regexes to it to fix exceptions that have accidentally been changed, and returns the new string. '''
	s = re.sub(' \. net ', ' .net', s)
	s = re.sub(' i \. e ', ' i.e. ', s)
	# fix extensions
	s = re.sub(' \. jpeg ', '.jpeg ', s)
	s = re.sub(' \. jpg ', '.jpg ', s)
	return s

    def _deal_with_code(self, s, maxcodelength):
	''' Takes a string as input, finds all code blocks in it and replace them with HHHH to protect them from whitespace addition, lower casing etc. Then returns the new string and a list of the code blocks so we can replace them after more cleaning. '''
        codepat = re.compile(r'<code>[^<]+</code>')
        codes = re.findall(codepat, s) # re.M for multiline matching not necessary?
        n = 0
        newcodes = []
        for c in codes:
	    if len(c) < maxcodelength + 13: # two code tags are 13 characters
		s = re.sub(re.escape(c), 'HHHH' + str(n), s)
               
		# Remove brackets if other half is missing. Else we'll have problems when we try to put them back. 
		if re.search(r'\)', c) and not re.search(r'\(', c):
                    c = re.sub(r'\)', '', c)
                if re.search(r'\(', c) and not re.search(r'\)', c):
                    c = re.sub(r'\(', '', c)

		c = re.sub(r'\n', ' ', c, re.M) # remove real newlines
		c = re.sub(r'\\n', r'\\\\n', c) # keep and escape \n in things like latex's \newcommand{}.
		c = re.sub(r'\s+', ' ', c)
		c = re.sub(r'<code>', '', c)
		c = re.sub(r'</code>', '', c)
                newcodes.append(c)
                n += 1
	    else:
		s = re.sub(re.escape(c), '', s) # Remove large code blocks

	return s, newcodes


    def very_basic_cleaning(self, s):
        s = self.url_cleaning(s)
        s = self.strip_tags(s)
        s = re.sub('\n+', ' ', s)
        return s

    def url_cleaning(self, s):
        ''' Takes a string as input and removes references to possible duplicate posts, and other stackexchange urls. '''

        posduppat = re.compile(r'<blockquote>(.|\n)+?Possible Duplicate(.|\n)+?</blockquote>', re.MULTILINE)
        s = re.sub(posduppat, '', s)

        s = re.sub(r'<a[^>]+stackexchange[^>]+>([^<]+)</a>', 'stackexchange-url ("\1")', s)
        s = re.sub(r'<a[^>]+stackoverflow[^>]+>([^<]+)</a>', 'stackexchange-url ("\1")', s)

        return s

    def strip_tags(self, html): # Source: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def _remove_stopwords(self, s):
	''' Takes a string as input, removes the stop words in the current stop word list, and returns the result.
	    The current stop word list can be accessed via self.stopwords, or altered by calling supply_stopwords(). '''

	words = nltk.word_tokenize(s) # The NLTK tokenizer cuts things like 'cannot' into 'can' and 'not'.
	words_split = s.split()
	if 'cannot' in words_split: # which we'd like to keep.
	    location = words_split.index('cannot')
	    words_split[location] = 'can'
	    words_split.insert(location + 1, 'not')
	counter = 0

	filteredwords = []
	prevw_in_split = True
	for w in words:
	    # It used to be so beautifully simple, until I found out NLTK sometimes splits things wrongly.
	    #if w in self.__stopwords:
            #    pass # skip it, we don't want it.
            #else:
            #    filteredwords.append(w)

	    if words_split[counter] == w: # word was correctly split
		if w not in self.__stopwords:
		    filteredwords.append(w)
		counter += 1
		prevw_in_split = True
	    elif prevw_in_split: # previous word was fine, but this is the first part of a wrongly split word.
		filteredwords.append(w)
		prevw_in_split = False
	    else: # this is a subsequent part of a wrongly split word
		newword = filteredwords[-1] + w
		filteredwords[-1] = newword
		if words_split[counter] == newword:
		    counter += 1
		    prevw_in_split = True
		else:
		    prevw_in_split = False
	cleanstring = ' '.join(filteredwords)
	cleanstring = self._fix_abbreviations(cleanstring)
	return cleanstring


    def _stem(self, s):
	''' Takes a string as input and applies the Porter stemmer as implemented in the NLTK (http://www.nltk.org/). Returns the result. '''
	words = nltk.word_tokenize(s)

	words_split = s.split()
        if 'cannot' in words_split:
            location = words_split.index('cannot')
            words_split[location] = 'can'
            words_split.insert(location + 1, 'not')
        counter = 0

	newwords = []
	for w in words:
	    # It used to be so beautiful and simple, until I found out that NLTK splits some things wrongly...
	    #neww = nltk.PorterStemmer().stem_word(w)
	    #newwords.append(neww)

	    if words_split[counter] == w: # word was correctly split
		neww = nltk.PorterStemmer().stem_word(w)
                newwords.append(neww)
                counter += 1
                prevw_in_split = True
            elif prevw_in_split: # previous word was fine, but this is the first part of a wrongly split word.
                newwords.append(w)
                prevw_in_split = False
            else: # this is a subsequent part of a wrongly split word
                newword = newwords[-1] + w
                if words_split[counter] == newword:
		    newwords[-1] = nltk.PorterStemmer().stem_word(newword)
                    counter += 1
                    prevw_in_split = True
                else:
		    newwords[-1] = newword
                    prevw_in_split = False


	news = ' '.join(newwords)
	news = self._fix_abbreviations(news)
	return news

    def _fix_abbreviations(self, s):
	''' Takes as input a string tokenized by nltk and joined again, and outputs a version in which the abbreviations have been fixed.
	    That means the final dot has been glued to the abbreviation once more.'''
	if re.search(r' ([a-z]\.[a-z])+ \.', s):
            found = re.search(r'( ([a-z]\.[a-z])+ \.)', s)
            abbr = found.group(1)
            newabbr = re.sub(' ', '', abbr)
            s = re.sub(abbr, ' ' + newabbr, s)
	return s

    def _remove_tags(self, s):
	''' Takes a string as input and removes HTML tags, except for code tags, which are remove in general_cleaning.
	    Also removes mentions of possible duplicates and changes URLs that point to other StackExchange threads into 'stackexahcnge-url'. '''

	s = re.sub(r"<blockquote.+possible duplicate.+/blockquote>", " ", s)
	s = re.sub(r"<a href=\"https?://[a-z]+\.stackexchange\.com[^\"]+\">([^<]+)</a>", r"\1", s)
	s = re.sub(r"<a href=\"[^\"]+\">([^<]+)</a>", r"\1", s)

	# Put some space between tags and urls or other things. So we don't accidentally remove more than we should a few lines further below this line.
	s = re.sub(r"<", " <", s)
	s = re.sub(r">", "> ", s)

	s = re.sub(r"https?://([a-z]+\.)?stackexchange\.com[^ ]+", "stackexchange-url", s)
	s = re.sub(r"https?://stackoverflow\.com[^ ]+", "stackexchange-url", s)

	# Remove all tags except for code tags
	alltags = re.findall(r'(</?)([^>]+)(>)', s) # list of tuples
	for tag in alltags:
	    if tag[1] != u'code':
                codetag = tag[0] + tag[1] + tag[2]
		s = re.sub(re.escape(codetag), '', s)
	return s


    def _expand_contractions(self, s):
	''' Takes a string as input, expands the contracted forms in it and returns the result. '''

	# Source: http://www.englishcoursemalta.com/learn/list-of-contracted-forms-in-english/
	c = {'i\'m': 'i am', 
	    'you\'re': 'you are',
	    'he\'s': 'he is',
	    'she\'s': 'she is',
	    'we\'re': 'we are',
	    'it\'s': 'it is',
	    'isn\'t': 'is not',
	    'aren\'t': 'are not',
	    'they\'re': 'they are',
	    'there\'s': 'there is',
	    'wasn\'t': 'was not',
	    'weren\'t': ' were not',
	    'i\'ve': 'i have',
	    'you\'ve': 'you have',
	    'we\'ve': 'we have',
	    'they\'ve': 'they have',
	    'hasn\'t': 'has not',
	    'haven\'t': 'have not',
	    'you\'d': 'you had',
	    'he\'d': 'he had',
	    'she\'d': 'she had',
	    'we\'d': 'we had',
	    'they\'d': 'they had',
	    'doesn\'t': 'does not',
	    'don\'t': 'do not',
	    'didn\'t': 'did not',
	    'i\'ll': 'i will',
	    'you\'ll': 'you will',
	    'he\'ll': 'he will',
	    'she\'ll': 'she will',
	    'we\'ll': 'we will',
	    'they\'ll': 'they will',
	    'there\'ll': 'there will',
	    'i\'d': 'i would',
	    'it\'d': 'it would',
	    'there\'d': 'there had',
	    'there\'d': 'there would',
	    'can\'t': 'can not',
	    'couldn\'t': 'could not',
	    'daren\'t': 'dare not',
	    'hadn\'t': 'had not',
	    'mightn\'t': 'might not',
	    'mustn\'t': 'must not',
	    'needn\'t': 'need not',
	    'oughtn\'t': 'ought not',
	    'shan\'t': 'shall not',
	    'shouldn\'t': 'should not',
	    'usedn\'t': 'used not',
	    'won\'t': 'will not',
	    'wouldn\'t': 'would not',
	    'what\'s': 'what is',
	    'that\'s': 'that is',
	    'who\'s': 'who is',}
	# Some forms of 's could either mean 'is' or 'has' but we've made a choice here.
	# Some forms of 'd could either mean 'had' or 'would' but we've made a choice here.
	# Some forms of 'll could wither mean 'will' or 'shall' but we've made a choice here.
	for pat in c:
	    s = re.sub(pat, c[pat], s)
	return s


    def _general_cleaning(self, s, codes, remove_punct=False):
	''' Takes a string as input and False or True for the argument 'remove_punct'.
	    Depending on the value of 'remove_punct', all punctuation is either removed, or a space is added before and after.
	    In both cases the punctuation un URLs and numbers is retained. 
	    
	    Also transforms "&amp;" into "and", and removes all other HTML entities.
	    Removes excessive white space. '''

	# Find all URLs and replace them with GGGG to protect them from whitespace addition.
	urlpat = re.compile(r'https?://[^ ]+')
	wwwpat = re.compile(r'www\.[^ ]+')
	compat = re.compile(r'[^ ]+\.com[^ ]+')
	coms = re.findall(compat, s)
	wwws = re.findall(wwwpat, s)
	urls = re.findall(urlpat, s)
	urls += wwws + coms
	n = 0
	newurls = []
	for url in set(urls):
	    if re.search(r'\)', url) and not re.search('\(', url):
		url = re.sub(r'\).*$', '', url)
	    if re.search(r'\\', url): # Get rid of backslashes because else we get regex problems when trying to put the URLs back.
		url = re.sub(r'\\', '/', url)
	    s = re.sub(re.escape(url), 'GGGG' + str(n), s)
	    newurls.append(url)
	    n += 1

	# Protect points, commas and colon in numbers
	while re.search(r'([0-9])\.([0-9])', s):
	    s = re.sub(r'([0-9])\.([0-9])', r'\1BBB\2', s)
	while re.search(r'([0-9]),([0-9])', s):
            s = re.sub(r'([0-9]),([0-9])', r'\1CCC\2', s)
	while re.search(r'([0-9]):([0-9])', s):
            s = re.sub(r'([0-9]):([0-9])', r'\1DDD\2', s)

	s = re.sub(r'&amp;', ' and ', s)

	if remove_punct:
	    # Remove all sorts of punctuation
	    #s = re.sub('[^a-zA-Z0-9_-]', ' ', s) # Too agressive!
	    p = re.compile(r'( [a-z] \.)( [a-z] \.)+')
	    l = p.finditer(s)
	    if l:
                for m in l:
                    newbit = re.sub(r' ', '', m.group()) # Get rid of white space in abbreviations
		    newabbr = re.sub(r'\.', 'PPPP', newbit) # change dots in abbreviations into 'PPPP'
                    s = re.sub(m.group() + ' +', ' ' + newabbr + ' ', s) # protect abbreviations
		    s = re.sub(r'\.', '', s) # remove all points that are not in abbreviations
		    s = re.sub(newabbr, newbit, s) # place dots back in abbreviations
	    else:
		s = re.sub(r'\.', ' ', s)
            s = re.sub(r',', ' ', s)
            s = re.sub(r'\?', ' ', s)
            s = re.sub(r'!', ' ', s)
            s = re.sub(r' \'([a-z])', r'  \1', s)
            s = re.sub(r'([a-z])\' ', r'\1 ', s)
            s = re.sub(r' \"([a-z])', r' \1', s)
            s = re.sub(r'([a-z])\" ', r'\1 ', s)
            s = re.sub(r'\(', ' ', s)
            s = re.sub(r'\)', ' ', s)
            s = re.sub(r'\[', ' ', s)
            s = re.sub(r'\]', ' ', s)
            s = re.sub(r'([a-z]): ', r'\1 ', s)
            s = re.sub(r';', ' ', s)
	    s = re.sub(r" - ", " ", s)
            s = re.sub(r"- ", " ", s)
	else:
	    # Add space around all sorts of punctuation.
	    #s = re.sub('([^a-zA-Z0-9_-])', r' \1 ', s) # Too agressive!
	    s = re.sub(r'\.', ' . ', s)

	    # Remove space around abbreviations
	    p = re.compile(r'( [a-z] \.)( [a-z] \.)+')
	    for m in p.finditer(s):
    		#print m.start(), '###' + m.group() + '###'
		#print s[m.start() - 20: m.start() + 20]
		newbit = re.sub(' ', '', m.group())
		s = re.sub(m.group() + ' +', ' ' + newbit + ' ', s)
		#print s[m.start() - 20: m.start() + 20]

	    s = re.sub(r',', ' , ', s)
	    s = re.sub(r'\?', ' ? ', s)
	    s = re.sub(r'!', ' ! ', s)
	    s = re.sub(r' \'([a-z])', r" ' \1", s)
	    s = re.sub(r'([a-z])\' ', r"\1 ' ", s)
	    s = re.sub(r' \"([a-z])', r' " \1', s)
            s = re.sub(r'([a-z])\" ', r'\1 " ', s)
	    s = re.sub(r'\(', ' ( ', s)
	    s = re.sub(r'\)', ' ) ', s)
	    s = re.sub(r'\[', ' [ ', s)
            s = re.sub(r'\]', ' ] ', s)
	    s = re.sub(r'([a-z]): ', r'\1 : ', s)
	    s = re.sub(r';', ' ; ', s)
	    s = re.sub(r"'s", " 's", s)


	# Restore points, commas and colons in numbers
	while re.search(r'([0-9])BBB([0-9])', s):
	    s = re.sub(r'([0-9])BBB([0-9])', r'\1.\2', s)
        while re.search(r'([0-9])CCC([0-9])', s):
            s = re.sub(r'([0-9])CCC([0-9])', r'\1,\2', s)
        while re.search(r'([0-9])DDD([0-9])', s):
            s = re.sub(r'([0-9])DDD([0-9])', r'\1:\2', s)

	# restore URLs
	newurllist = itertools.izip(reversed(xrange(len(newurls))), reversed(newurls)) # reverse list to GGGG1 does not match GGG10. (Source: http://galvanist.com/post/53478841501/python-reverse-enumerate)
	for i, u in newurllist:
	    s = re.sub('GGGG' + str(i), u, s) # Escaping u here leads to backslashes in URLs.

	# Get rid of things we don't want, like HTML entities.
	s = re.sub(r"&[a-z]+;", "", s)
	s = re.sub(r"&#?[a-z]+;", "", s) # &#xA; == '\n'
	# Remove excessive whitespace
	s = re.sub(r"\s+", " ", s)
	s = re.sub(r"^\s", "", s)
	s = re.sub(r"\s$", "", s)

        # restore codeblocks
	newlist = itertools.izip(reversed(xrange(len(codes))), reversed(codes)) # reverse list to hhhh1 does not match hhhh10 (Source: http://galvanist.com/post/53478841501/python-reverse-enumerate)
	for i, c in newlist:
            s = re.sub('hhhh' + str(i), c.encode('unicode-escape'), s) # Escaping here leads to backslashes being added in the code blocks.
	return s


    #################
    # Split methods #
    #################

    def split_for_classification(self):
	''' Takes no input and makes twelve plain text files: a small test set, a large test set, and 10 files for the training set (trainpairs_[01-10].txt, testpairs_small.txt and testpairs_large.txt).
	    Each line in these sets contains two postids and a label (1 for duplicate, 0 for non-duplicate), separated by a space. Each of these pairs is a training or test instance.
	    The training pairs have been divided over ten different files. These can be used for ten-fold cross-validation.

	    To make the split all posts are ordered according to date. Next the set is cut into two at a certain date.
	    This date is chosen such that the test set will ideally contain at least 200 duplicate pairs, or if that iss not possible, as many as possible, with a minimum of 100, and the train set contains at least four times as many.
	    The test set contains pairs of posts with a date after the cutoff date. Posts are only combined with older posts, as would be the case in a real world setting. The training set contains pairs of posts with a date before the cutoff date. Again, posts are only combined with older posts. 
	    A consequence of this approach is that we lose a number of duplicate pairs, namely the ones that are posted after the cutoff date, but their duplicate was posted before. 
	    Both testpairs_large.txt and the trainpairs files will contain millions of pairs.
	    Testpairs_small.txt contains a subset of testpairs_large.txt. It is a smaller and more balanced set, which contains ten times more non-duplicate pairs than duplicate pairs.'''
	
	if not self.cutoffdate:
	    self._find_cutoff_date()
        if self.cutoffdate == 'nogood': # Should not happen with the supplied forums, only with the smaller ones I'm sometimes testing with.
	    #print "No candidate cutoff date could be found that satisfies our constraints."
	    #print "This means we cannot make splits for classification for this subforum."
	    return

	sorted_all = self.get_ordered_list_of_posts()
	# The above results in a list of tuples (postid, datetime object), ordered from newest to oldest post.

	# Split the set
	testposts = []
	trainposts = []
	
	for posttuple in sorted_all:
	    if posttuple[1] >= self.cutoffdate:
		testposts.append(posttuple[0])
	    else:
		trainposts.append(posttuple[0])


	# Generate pairs and write them to files.
	withdups = []
        withoutdups = []
	testfile = open(self.cat + '_testpairs_large.txt', 'w')
	for i,postid in enumerate(testposts):
	    dups = self.get_duplicates(postid)
	    combine_with = testposts[i+1:] # combine each post with older posts.
	    for otherpostid in combine_with:
		if otherpostid in dups:
		    withdups.append((postid, otherpostid, '1'))
		    testfile.write(postid + ' ' + otherpostid + ' 1\n')
		else:
		    withoutdups.append((postid, otherpostid, '0'))
		    testfile.write(postid + ' ' + otherpostid + ' 0\n')
	testfile.close()

	#print "Nr of duplicate pairs in the test sets:", len(withdups)

	# Now we need to randomly pick non-duplicate pairs for the small test set.
	# Here's an O(n) way to do it. This way, no searching and no trailing-element copying are made, but withoutdups is still getting smaller, to make sure we don't repeat picks.
	# Source: http://code.activestate.com/recipes/59883-random-selection-of-elements-in-a-list-with-no-rep/ .

	nrofnondups_forsmallset = len(withdups) * 10 # Take ten times the nr of duplicate pairs as non-duplicate pairs. The rest of the non-duplicate pairs will not be used in the small test set.
	withoutdups_for_smallset = []
	while nrofnondups_forsmallset > 0:
	    pos = randrange(len(withoutdups)) # randrange very conveniently excludes the last element of the list.
	    picked_nondup = withoutdups[pos]
	    withoutdups[pos] = withoutdups[-1] # Replace picked element with last one in the list
	    del withoutdups[-1] # Cheap removal of element
	    withoutdups_for_smallset.append(picked_nondup)
	    nrofnondups_forsmallset -= 1

        testfile = open(self.cat + '_testpairs_small.txt', 'w')
        for tup in withdups:
            testfile.write(tup[0] + ' ' + tup[1] + ' ' + tup[2] + '\n')
        for tup in withoutdups_for_smallset:
            testfile.write(tup[0] + ' ' + tup[1] + ' ' + tup[2] + '\n')
        testfile.close()


	totaltrainpairs = int(round(float(comb(len(trainposts), 2)),0))
	print "total train pairs:", totaltrainpairs

	trainfile1 = open(self.cat + '_trainpairs_01.txt', 'w')
        trainfile2 = open(self.cat + '_trainpairs_02.txt', 'w')
        trainfile3 = open(self.cat + '_trainpairs_03.txt', 'w')
        trainfile4 = open(self.cat + '_trainpairs_04.txt', 'w')
        trainfile5 = open(self.cat + '_trainpairs_05.txt', 'w')
        trainfile6 = open(self.cat + '_trainpairs_06.txt', 'w')
        trainfile7 = open(self.cat + '_trainpairs_07.txt', 'w')
        trainfile8 = open(self.cat + '_trainpairs_08.txt', 'w')
        trainfile9 = open(self.cat + '_trainpairs_09.txt', 'w')
        trainfile10 = open(self.cat + '_trainpairs_10.txt', 'w')

	filenrs = [trainfile1, trainfile2, trainfile3, trainfile4, trainfile5, trainfile6, trainfile7, trainfile8, trainfile9, trainfile10]
	dupindex = 0
	nondupindex = 0

	traindups = 0
        for i,postid in enumerate(trainposts):
            dups = self.get_duplicates(postid)
            combine_with = trainposts[i+1:] # combine each post with older posts.
            for otherpostid in combine_with:
                if otherpostid in dups:
		    filenrs[dupindex].write(postid + ' ' + otherpostid + ' 1\n') # 1 = duplicate pair
		    if dupindex == 9:
                        dupindex = 0
                    else:
                        dupindex += 1
		    traindups += 1
		else:
		    filenrs[nondupindex].write(postid + ' ' + otherpostid + ' 0\n') # 0 = non-duplicate pair
		    if nondupindex == 9:
			nondupindex = 0
		    else:
		        nondupindex += 1
        trainfile1.close()
        trainfile2.close()
        trainfile3.close()
        trainfile4.close()
        trainfile5.close()
        trainfile6.close()
        trainfile7.close()
        trainfile8.close()
        trainfile9.close()
        trainfile10.close()
	#print "Nr of duplicate pairs in the train set:", traindups


    def _find_cutoff_date(self):
	''' Takes no input and finds the best date to be used as a cutoff point to split the data into a training and test set.
	    See split_for_classification() for more details. '''
	duppairs = []
	dates = []

	postswithdups = self.get_posts_with_duplicates()

	# Generate duplicate pairs
	for postid in postswithdups:
	    y, m, d = self.get_postdate(postid).split('-')
	    d = datetime.date(int(y), int(m), int(d))
	    dups = self.get_duplicates(postid)
	    for dup in dups:
		y2, m2, d2 = self.get_postdate(dup).split('-')
		d2 = datetime.date(int(y2), int(m2), int(d2))
		duppairs.append((d, d2))

	duppairs = sorted(duppairs)
	t = {}
	datelist = []

	# Calculate the number of duplicate pairs in the test set, train set and the ones we lose, based on different cutoff dates
	for pair in duppairs:
	    thresdate = pair[0] # This is the cutoff date
	    datelist.append(thresdate)
	    t[thresdate] = {'test': 0, 'train': 0, 'lost': 0}
	    for combo in duppairs:
		if combo[0] >= thresdate:
		    if combo[1] >= thresdate:
			t[thresdate]['test'] += 1
		    else:
			t[thresdate]['lost'] += 1
		else:
		    t[thresdate]['train'] += 1

	datelist = sorted(list(set(datelist)))

	# Find date where train is 4 times bigger than test, and test has at least 200 duplicate pairs if possible, else as many as possible, with a minimum of 100.
	allcandidates = [] # candiDATES
	for thres in datelist:
	    if t[thres]['test'] >= 200:
		if t[thres]['train'] >= 4 * t[thres]['test']:
		    datum = str(thres.year) + '-' + str(thres.month) + '-' + str(thres.day)
		    allcandidates.append((datum, t[thres]['test'], t[thres]['train'], t[thres]['lost']))

	# If 200 is too many and we didn't find any candidates, than lower the minimum of duplicate pairs in the test set to 100.
	if allcandidates == []:
	    for thres in datelist:
		if t[thres]['test'] >= 100:
		    if t[thres]['train'] >= 4 * t[thres]['test']:
			datum = str(thres.year) + '-' + str(thres.month) + '-' + str(thres.day)
			allcandidates.append((datum, t[thres]['test'], t[thres]['train'], t[thres]['lost']))
			break # One candiDATE is enough: the one with the highest nr of duplicate pairs in the test set.

	position = len(allcandidates) / 2 # The best candiDATE is the one in the middle.
	if allcandidates != []:
	    bestdate = allcandidates[position][0]
	    self.cutoffdate = datetime.datetime.strptime(bestdate, '%Y-%m-%d')
	else:
	    self.cutoffdate = 'nogood' # No cutoff candiDATE could be found that satisfies our constraints. Won't happen in the chosen subforums.


    def split_for_retrieval(self):
	''' Takes no input and returns three lists: one with test ids, one with development ids and one with ids to be indexed.
	    The test and development sets contain the most recent posts in the subforum, such that each contains about 15% of all the posts that have duplicates.
	    They have been assigned alternately to the test and devel sets, so they are quite similar.
	    Both test and development sets also contain posts that do not have any duplicates, in the actual proportion of the particular subforum. '''

	sorted_all = self.get_ordered_list_of_posts()
	# The above results in a list of tuples (postid, datetime object), ordered from newest to oldest post.

	# Find out how many duplicate posts there are and how many correspond to fifteen percent of them.
	posts_with_dups = self.get_posts_with_duplicates()
	fifteen_percent = int(round(15 * len(posts_with_dups) / 100.0, 0))

	testids = [] # all test ids
	testdups = [] # only those test ids that have one or more duplicate posts
	develids = [] # all development ids
	develdups = [] # only those development ids that have one or more duplicate posts
	toindex = []

	# Alternatingly assign posts with duplicates to test and devel set (and posts without duplicates too).
	# When we reach the 15% limit, we assign everything else to the index set.
	flip = False
	for posttup in sorted_all:
	    postid = posttup[0]
	    if len(testdups) == fifteen_percent:
		toindex.append(postid)
	    elif flip:
		develids.append(postid)
		if postid in posts_with_dups:
		    develdups.append(postid)
		    flip = not flip
	    else:
		testids.append(postid)
		if postid in posts_with_dups:
		    testdups.append(postid)
		    flip = not flip
	
        # Next we check if all duplicate posts are in the toindex set. If not, we need to move them, because else they cannot be found.
	for post in testdups:
	    for dup in self.postdict[post]['dups']:
		if not dup in toindex:
		    toindex.append(dup)
		    if dup in testids:
			testids.remove(dup)
		    elif dup in develids:
			develids.remove(dup)

	for post in develdups:
	    for dup in self.postdict[post]['dups']:
		if not dup in toindex:
		    toindex.append(dup)
		    if dup in testids:
                        testids.remove(dup)
		    elif dup in develids:
			develids.remove(dup)

	#print "Nr of dups in testset:", len(testdups)
	#print "Nr of dups in develset:", len(develdups)
	return testids, develids, toindex

    ####################################
    # Evaluation metrics for retrieval #
    ####################################


    def _read_scorefile(self, scorefile):
	''' Takes a file with scores as input and returns three lists with one list per query in them. One list contains ranked lists of results, one contains lists of the duplicates that should be found, and one contains lists of the related posts that can optionally be counted as half relevant in the evaluation. 
	    The score file should contain a query id followed by a ranked list of returned results, all separated by white space. '''
	inputf_open = open(scorefile, 'r')
	inputf = inputf_open.readlines()
	inputf_open.close()
	rankings = [] # Will be a list of lists
	relevantdocs = [] # Will be a list of lists
	relateddocs = []
	for line in inputf:
            bits = line.split()
            queryid = bits[0]
            rankedresults = bits[1:]
	    # If ranked ids are followed by their scores, use the following two lines to select only the ids.
	    #rankedresults_evens = filter(lambda x: rankedresults.index(x) % 2 == 0, rankedresults)
	    #rankedresults = rankedresults_evens

	    dupstofind = self.get_duplicates(queryid)
	    relstofind = self.get_related(queryid)
	    rankings.append(rankedresults)
	    relevantdocs.append(dupstofind)
	    relateddocs.append(relstofind)
	return rankings, relevantdocs, relateddocs
	
    def average_ndcg_at(self, scorefile, cutoff=None, include_related_posts=False):
        ''' Takes a file with scores and a cutoff point as input and returns the Normalised Discounted Cumulative Gain at the cutoff point. The default is 10.
            If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant. 
            See "Cumulated Gain-based Evaluation of IR Techniques" by Jarvelin and Kekalainen 2002 for more information on this metric.
	    Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. 
	    Just for extra information: Taking related posts into account can lower the score if these documents are not returned, because they appear in the ideal ranking that is used in the calculation of the metric. This is not the case for the other retrieval evaluation metrics. '''

        all_rankings, all_relevantdocs, all_relateddocs = self._read_scorefile(scorefile)

        ndcgs_at_cutoff = []
        for i,ranking in enumerate(all_rankings):
	    relevantdocs = all_relevantdocs[i]
	    relateddocs = all_relateddocs[i]
            if relevantdocs != []:# or (relateddocs != [] and include_related_posts): # We only compute the score for queries that actually do have duplicates in the indexed set.
				  # With the above extra check included, it can happen that the scores decrease when including related posts.
                                  # This is because some queries only have related posts, leading to a higher number of scores in precision_at_list.

		if cutoff:
                    ranking = ranking[:cutoff]

                if include_related_posts:
                    relevance_judgements = map(lambda x: 1.0 if x in relevantdocs else (0.5 if x in relateddocs else 0.0), ranking)
                else:
                    relevance_judgements = map(lambda x: 1.0 if x in relevantdocs else 0.0, ranking)

		DCG = self._get_DCG(relevance_judgements)
		I = self._get_I(cutoff, include_related_posts, relevantdocs, relateddocs)
		DCG_I = self._get_DCG(I)

		try:
		    nDCG = map(truediv, DCG, DCG_I)
		except ZeroDivisionError: # Can lead to ZeroDivisionError if you use queries that don't have any duplicates. Although the metric does not make sense in that scenario.
		    nDCG = []
		    for i,v in enumerate(DCG):
			if DCG_I[i] == 0:
			    nDCG.append(0)
			else:
			    nDCG.append(v/DCG_I[i])
		
    		av_nDCG = round(sum(nDCG) / float(len(nDCG)), 4) # This is the same as round(sum(nDCG) * len(nDCG) ** -1, 4)
                ndcgs_at_cutoff.append(av_nDCG)

        return sum(ndcgs_at_cutoff) / len(ndcgs_at_cutoff)

    def _get_DCG(self, G):
	''' Returns the discounted cumulative gain vector of the input vector G, which is a list of ranking scores. 
	    E.g. [1, 1, 0, 0, 0,5, 1, 0.5, 0, 0] '''
	DCG = []
	for i,v in enumerate(G):
	    if i == 0:
		DCG.append(v)
	    elif v == 0:
		DCG.append(DCG[-1])
	    else:
		newv = round(DCG[-1] + v / math.log(i + 1,2), 2)
		DCG.append(newv)
	return DCG

    def _get_I(self, cutoff, include_related_posts, relevantdocs, relateddocs):
	''' Returns a list of ideal gains based on a cutoff point, a list of relevant documents, and optionally a list of related documents. '''
	ones = len(relevantdocs)
	halves = 0
        if include_related_posts:
            halves = len(relateddocs)
	I = [1.0 for i in range(ones)] + [0.5 for i in range(halves)]
	I += [0.0 for i in range(cutoff - len(I))]
	return I[:cutoff]
	    

    def average_recall_at(self, scorefile, cutoff=None, include_related_posts=False):
	''' Takes a file with scores and optionally a cutoff point as input and returns the Recall (at this cutoff, if specified). 
	    If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.
	    Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. '''

        all_rankings, all_relevantdocs, all_relateddocs = self._read_scorefile(scorefile)
	recall_at_list = []
	for i,ranking in enumerate(all_rankings):
	    relevantdocs = all_relevantdocs[i]
	    relateddocs = all_relateddocs[i]
	    if relevantdocs != []:# or (relateddocs != [] and include_related_posts): # We only compute the score for queries that actually do have duplicates in the indexed set.
				  # With the above extra check included, it can happen that the scores decrease when including related posts.
                                  # This is because some queries only have related posts, leading to a higher number of scores in precision_at_list.
		
		if cutoff:
            	    ranking = ranking[:cutoff]
        	relevant_in_ranking = len([w for w in relevantdocs if w in ranking])
		relevant_to_find = float(len(relevantdocs))
		if include_related_posts:
		    half_relevant_in_ranking = len([w for w in relateddocs if w in ranking]) / 2.0
		    relevant_in_ranking += half_relevant_in_ranking
		    relevant_to_find += len(relateddocs) / 2.0
        	recall_at_list.append(relevant_in_ranking/relevant_to_find)

	return sum(recall_at_list) / len(recall_at_list)

    def average_precision_at(self, scorefile, cutoff=None, include_related_posts=False):
	''' Takes a file with scores and optionally a cutoff point as input and returns the Precision (at this cutoff, if specified). 
	    If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.
	    Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. '''
	
	all_rankings, all_relevantdocs, all_relateddocs = self._read_scorefile(scorefile)
	precision_at_list = []
	for i,ranking in enumerate(all_rankings):
	    relevantdocs = all_relevantdocs[i]
	    relateddocs = all_relateddocs[i]
            if relevantdocs != []:# or (relateddocs != [] and include_related_posts): # We only compute the score for queries that actually do have duplicates in the indexed set.
				  # With the above extra check included, it can happen that the scores decrease when including related posts.
				  # This is because some queries only have related posts, leading to a higher number of scores in precision_at_list.

        	if cutoff:
            	    ranking = ranking[:cutoff]
            	relevant_in_ranking = len([w for w in relevantdocs if w in ranking]) # relevant docs is most likely shorter than ranking, so it is fastest this way around.
		if include_related_posts:
                    half_relevant_in_ranking = len([w for w in relateddocs if w in ranking]) / 2.0
                    relevant_in_ranking += half_relevant_in_ranking
            	precision_at_list.append(relevant_in_ranking/float(len(ranking)))

	return sum(precision_at_list) / len(precision_at_list)


    def mean_average_precision(self, scorefile, include_related_posts=False):
        ''' Takes a file with scores as input and returns the Mean Average Precision (MAP) score.
	    If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.
	    Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. '''
        
        all_rankings, all_relevantdocs, all_relateddocs = self._read_scorefile(scorefile)
        average_precisions = []
        for i,ranking in enumerate(all_rankings):
	    relevantdocs = all_relevantdocs[i]
	    relateddocs = all_relateddocs[i]
            if relevantdocs != []:# or (relateddocs != [] and include_related_posts): # We only compute the score for queries that actually do have duplicates in the indexed set.
				  # With the above extra check included, it can happen that the scores decrease when including related posts.
                                  # This is because some queries only have related posts, leading to a higher number of scores in precision_at_list.

		if include_related_posts:
		    av_p = self._average_precision(ranking, relevantdocs, relateddocs=relateddocs)
		else:
                    av_p = self._average_precision(ranking, relevantdocs)
                average_precisions.append(av_p)
        
        return sum(average_precisions) / len(average_precisions)


    def _average_precision(self, ranking, relevantdocs, relateddocs=[]):
        ''' Takes a ranking and a set of relevant documents as input and returns the average precision.
	    An optional third argument of relateddocs can be supplied if related docs need to be counted as half relevant. '''
        precisions = []
	numerator = 0
        for rank,doc in enumerate(ranking):
            if doc in relevantdocs:
		numerator += 1
                precisions.append(numerator/float(rank+1)) # enumerate starts to count from 0, but for the AP we need to start from 1. Hence the +1 here.
	    elif doc in relateddocs:
		numerator += 0.5
		precisions.append(numerator/float(rank+1))
        if precisions != []:
            return sum(precisions)/len(precisions)
        else:
            return 0.0

    def mean_reciprocal_rank(self, scorefile):
        ''' Takes a file with scores as input and returns the Mean Reciprocal Rank (MRR) score. '''
	# Unfortunately we cannot count related questions as half relevant here. It does not make sense.
	
        all_rankings, all_relevantdocs, all_relateddocs = self._read_scorefile(scorefile)
        reciprocal_ranks = []
        for i,ranking in enumerate(all_rankings):
	    relevantdocs = all_relevantdocs[i]
            if relevantdocs != []: # We only compute the score for queries that actually do have duplicates in the indexed set.
                rr = self._reciprocal_rank(ranking, relevantdocs)
                reciprocal_ranks.append(rr)
	
        return sum(reciprocal_ranks) / len(reciprocal_ranks)

    def _reciprocal_rank(self, ranking, relevantdocs):
	''' Takes a ranking and a set of relevant documents as input and returns the reciprocal rank. '''
	# Unfortunately we cannot count related questions as half relevant here. It does not make sense.
        for i,doc in enumerate(ranking):
            if doc in relevantdocs:
                return 1.0/(i+1)
        return 0.0


    #########################################
    # Evaluation metrics for classification #
    #########################################

    def evaluate_classification(self, scorefile):
	''' Takes a file with scores as input and returns a dictionary with the Precision, Recall, F1-score, Accuracy and precision and Recall per class.
	    The file with scores should have the same format as the classification training and test sets:
	    One line per classification with two space separated postids followed by a 1 for duplicates, or 0 for non-duplicates. '''
	truenegatives = 0
	truepositives = 0
	falsenegatives = 0 # Type II errors
	falsepositives = 0 # Type I errors
	
	with open(scorefile) as fileobject:
            for line in fileobject:
	        postid, compareid, verdict = line.split()
	        if compareid in self.get_duplicates(postid):
	            goldstandard = '1'
	        else:
		    goldstandard = '0'
	        if goldstandard == '0':
		    if verdict == '0':
		        truenegatives += 1
	 	    else:
		        falsepositives += 1
	        elif verdict == '1':
		    truepositives += 1
	        else:
		    falsenegatives += 1

	precision = self._compute_precision(truenegatives, truepositives, falsenegatives, falsepositives)
	recall = self._compute_recall(truenegatives, truepositives, falsenegatives, falsepositives)
	fscore = self._compute_fscore(recall, precision)
	accuracy = self._compute_accuracy(truenegatives, truepositives, falsenegatives, falsepositives)
	prec_pos, prec_neg = self._compute_precision_oneclass(truenegatives, truepositives, falsenegatives, falsepositives)
        rec_pos, rec_neg = self._compute_recall_oneclass(truenegatives, truepositives, falsenegatives, falsepositives)
        return {'precision': precision, 'recall': recall, 'fscore': fscore, 'accuracy': accuracy, 'precision_positive_class': prec_pos, 'precision_negative_class': prec_neg, 'recall_positive_class': rec_pos, 'recall_negative_class': rec_neg}

    def plot_roc(self, scorefile, plotfilename):
	''' Takes a file with scores and a the name of a plot file (png) as input and returns the false positive rates (list), true positive rates (list), thresholds at which they were computed (list) and the area under the curve (float). The plot will be written to the supplied plot file. 
	The scores can either be probability estimates of the positive class, confidence values, or binary decisions. 
	This method requires scikit-learn to be installed: http://scikit-learn.org/stable/install.html 
	This method only computes the ROC curve for the positive class. See http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html for an example on how to make curves for multiple classes (for instance when you have a third class for the related questions).       '''
	# A simple example on how to use roc_curve: http://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics

	import numpy as np
	from sklearn.metrics import roc_curve
	from sklearn.metrics import roc_auc_score
	import matplotlib.pyplot as plt

	y_list = []
	scores_list = []
	with open(scorefile) as fileobject:
            for line in fileobject:
                postid, compareid, verdict = line.split()
		scores_list.append(float(verdict))
                if compareid in self.get_duplicates(postid):
                    y_list.append(1)
                else:
                    y_list.append(0)

	y = np.array(y_list) # y need to contains the true binary values
	scores = np.array(scores_list) # the scores can either be probability estimates of the positive class, confidence values, or binary decisions.
	fpr, tpr, thresholds = roc_curve(y, scores, pos_label=1) 
	auc = roc_auc_score(y, scores)

	plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic curve')
        plt.legend(loc="lower right")
	plt.savefig(plotfilename)
        #plt.show()

	return fpr, tpr, thresholds, auc

    def _compute_precision(self, truenegatives, truepositives, falsenegatives, falsepositives):
        ''' Takes the nr of truenegatives, truepositives, falsenegatives, and falsepositives as input and returns the precision. '''
        predicted_positives = float(truepositives + falsepositives)
        if predicted_positives > 0.0:
            return truepositives / predicted_positives
        return 0.0

    def _compute_recall(self, truenegatives, truepositives, falsenegatives, falsepositives):
        ''' Takes the nr of truenegatives, truepositives, falsenegatives, and falsepositives as input and returns the recall. '''
        all_positives = float(truepositives + falsenegatives)
        if all_positives > 0.0:
            return truepositives / all_positives
        return 0.0

    def _compute_fscore(self, recall, precision):
        ''' Takes the recall and precision as input and returns the F1-score. '''
        pr = precision + recall
        if pr > 0.0:
            return 2 * ((precision * recall) / pr)
        return 0.0

    def _compute_accuracy(self, truenegatives, truepositives, falsenegatives, falsepositives):
        ''' Takes the nr of truenegatives, truepositives, falsenegatives, and falsepositives as input and returns the accuracy. '''
        return (truepositives + truenegatives) / float(truepositives + falsepositives + truenegatives + falsenegatives)

    def _compute_precision_oneclass(self, truenegatives, truepositives, falsenegatives, falsepositives):
        ''' Takes the nr of truenegatives, truepositives, falsenegatives, and falsepositives as input and returns the precision for both the positive and the negative class. '''
        # For the positive class (this is the same as normal precision):
        predicted_positives = float(truepositives + falsepositives)
        if predicted_positives > 0.0:
            precision_for_positives = truepositives / predicted_positives
        else:
            precision_for_positives = 0.0

        # For the negative class:
        predicted_negatives = float(truenegatives + falsenegatives)
        if predicted_negatives > 0.0:
            precision_for_negatives = truenegatives / predicted_negatives
        else:
            precision_for_negatives = 0.0

        return precision_for_positives, precision_for_negatives


    def _compute_recall_oneclass(self, truenegatives, truepositives, falsenegatives, falsepositives):
        ''' Takes the nr of truenegatives, truepositives, falsenegatives, and falsepositives as input and returns the recall for both the positive and the negative class. '''
        # For the positive class (this is the same as normal precision):
        all_positives = float(truepositives + falsenegatives)
        if all_positives > 0.0:
            recall_for_positives = truepositives / all_positives
        else:
            recall_for_positives = 0.0

        # For the negative class:
        all_negatives = float(truenegatives + falsepositives)
        if all_negatives > 0.0:
            recall_for_negatives = truenegatives / all_negatives
        else: # not likely, but we need to check anyway
            recall_for_negatives = 0.0

        return recall_for_positives, recall_for_negatives


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)



####################################################################################
	
def usage():
    usage_text = '''
    This script can be used to query the StackExchange data downloaded from http://nlp.cis.unimelb.edu.au/resources/cqadupstack/.

    The script contains a main function called load_subforum(). It has one argument: a StackExchange subforum.zip file.
    load_subforum() uses this file to create a 'Subforum' object and returns this.
    Alternatively, you can make a subforum object directly by calling the class 'Subforum' yourself. Just like load_subforum() it needs a zipped subforum file as its only argument.

    Subforum objects can be queried using the following methods:

'''

    strhelp = pydoc.render_doc(Subforum, "Help on %s")
    i = strhelp.find('below')
    strhelp = strhelp[i+9:]
    usage_text += strhelp
    usage_text += '\n\n    The input to the evaluation metric methods (the scorefile), should be a plain text file with one query per line in the following format:'
    usage_text += '\n\n    queryid1    result1 result2 result3 etc.'
    usage_text += '\n    queryid2    result1 result2 result3 etc.'
    usage_text += '\n\n    Both the query id and results should be post ids. They should be separated either by a space or a TAB.'
    usage_text += '\n\n    -----------------------------'
    usage_text += '\n\n    Here are some examples of how to use the script:'
    usage_text += '''\n\n    >>> import query_cqadupstack as qcqa
    >>> o = qcqa.load_subforum('/home/hoogeveen/datasets/CQADupStack/webmasters.zip')
    >>> testset, develset, indexset = o.split_for_retrieval()
    >>> len(develset)
    1862
    >>> for i in develset:
    ...     if o.get_duplicates(i) != []:
    ...         print i, o.get_duplicates(i)
    ... 
    69050 [u'8710']
    68979 [u'52812']
    68897 [u'6073']
    68856 [u'6073']
    68689 [u'20838']
    etc.
    >>> o.get_posttitle('18957')
    u'What do you consider a "mobile" device?'
    >>> o.get_postbody('18957')
    u'<p>I\'m implementing a mobile-friendly version of our corporate web site and will be using <a href="http://wurfl.sourceforge.net/" rel="nofollow" title="WURFL">WURFL</a> to detect mobile browsers and redirect them to our mobile site.  Having recently purchased an Android tablet, I\'ve found that many sites consider it to be a mobile device even though it has a large 10" screen and it\'s perfectly capable of handling sites designed using standard desktop resolutions.</p>\n\n<p>My plan is to use WURFL, examine the device capabilities and treat anything with a resolution width of less than 700px as a mobile device, but I\'d like some input as to that sweet spot for determining mobile vs desktop.</p>\n'
    >>> o.perform_cleaning(o.get_postbody('18957'))
    u'i am implementing a mobile-friendly version of our corporate web site and will be using wurfl to detect mobile browsers and redirect them to our mobile site . having recently purchased an android tablet , i have found that many sites consider it to be a mobile device even though it has a large 10" screen and it is perfectly capable of handling sites designed using standard desktop resolutions . my plan is to use wurfl , examine the device capabilities and treat anything with a resolution width of less than 700px as a mobile device , but i would like some input as to that sweet spot for determining mobile vs desktop .'
    >>> for a in o.get_answers('18957'):
    ...     print a, o.get_answerscore(a)
    ... 
    18985 1
    18980 0
    >>> o.get_posttags(o.get_random_postid())
    [u'wordpress', u'redirects', u'blog', u'plugin']
    >>> o.get_postuserid('18957')
    u'1907'
    >>> o.get_user_posts('1907')
    [u'18957']
    >>> o.get_user_views('1907')
    6
    >>> o.stopwords
    ['in', 'on', 'at', 'a', 'an', 'is', 'be', 'was', 'I', 'you', 'the', 'do', 'did', 'of', 'so', 'for', 'with']
    >>> o.supply_stopwords('new_stopwords_testfile.txt')
    >>> o.stopwords
    [u'new_stopword1', u'new_stopword2', u'new_stopword3']
    >>> o.change_to_default_stopwords()
    >>> o.stopwords
    ['in', 'on', 'at', 'a', 'an', 'is', 'be', 'was', 'I', 'you', 'the', 'do', 'did', 'of', 'so', 'for', 'with']'''
    usage_text += '\n\n    -----------------------------'
    usage_text += '\n\n    Please see the README file that came with this script for more information on the data.\n'
    print usage_text 
    sys.exit(' ')

#-------------------------------
if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        usage()
    else:
        main(sys.argv[1])


