The scripts in this directory can be used to manipulate the CQADupStack data, downloadable from http://nlp.cis.unimelb.edu.au/resources/cqadupstack/.

CQADupStack contains 12 Stackexchange (http://stackexchange.com/) subforums which have been preprocessed as described in the paper mentioned below.
The StackExchange data dump that forms the basis of this set is the version released on September 26, 2014.

stackexchange_xmldump_to_cqadupstack.py was used to change the StackExchange dump into CQADupStack.

query_cqadupstack.py enables easy access to all the different fields in CQADupStack. It can be used to split the data into pre-defined retrieval or classification splits, and it can be used to evaluate the output of your system, using one of several evaluation metrics available.

Please cite the following paper when making use of CQADupStack:

@inproceedings{hoogeveen2015,
 author = {Hoogeveen, Doris and Verspoor, Karin M. and Baldwin, Timothy},
 title = {CQADupStack: A Benchmark Data Set for Community Question-Answering Research},
 booktitle = {Proceedings of the 20th Australasian Document Computing Symposium (ADCS)},
 series = {ADCS '15},
 year = {2015},
 isbn = {978-1-4503-4040-3},
 location = {Parramatta, NSW, Australia},
 pages = {3:1--3:8},
 articleno = {3},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/2838931.2838934},
 doi = {10.1145/2838931.2838934},
 acmid = {2838934},
 publisher = {ACM},
 address = {New York, NY, USA},
} 

For licensing information please see the LICENCE file.

For more information on the structure of the files in the data set, please see the README file that comes with the data.
The README file you are reading now contains information on the query script (query_cqadupstack.py) only.

query_cqadupstack.py contains a main function called load_subforum(). It has one argument: a StackExchange subforum.zip file from CQADupStack.
load_subforum() uses this file to create a 'Subforum' object and returns this.
Alternatively, you can make a subforum object directly by calling the class 'Subforum' yourself. Just like load_subforum() it needs a zipped subforum file as its only argument.

Subforum objects can be queried using the following methods: (examples on how to use them can be found at the end of this file)

### SPLIT METHODS ###

 |  split_for_classification(self)
 |      Takes no input and makes twelve plain text files: a small test set, a large test set, and 10 files for the training set (trainpairs_[01-10].txt, testpairs_small.txt and testpairs_large.txt).
 |      Each line in these sets contains two postids and a label (1 for duplicate, 0 for non-duplicate), separated by a space. Each of these pairs is a training or test instance.
 |      The training pairs have been divided over ten different files. These can be used for ten-fold cross-validation.
 |      
 |      To make the split all posts are ordered according to date. Next the set is cut into two at a certain date.
 |      This date is chosen such that the test set will ideally contain at least 200 duplicate pairs, or if that iss not possible, as many as possible, with a minimum of 100, and the train set contains at least four times as many.
 |      The test set contains pairs of posts with a date after the cutoff date. Posts are only combined with older posts, as would be the case in a real world setting. The training set contains pairs of posts with a date before the cutoff date. Again, posts are only combined with older posts. 
 |      A consequence of this approach is that we lose a number of duplicate pairs, namely the ones that are posted after the cutoff date, but their duplicate was posted before. 
 |      Both testpairs_large.txt and the trainpairs files will contain millions of pairs.
 |      Testpairs_small.txt contains a subset of testpairs_large.txt. It is a smaller and more balanced set, which contains ten times more non-duplicate pairs than duplicate pairs.
 |  
 |  split_for_retrieval(self)
 |      Takes no input and returns three lists: one with test ids, one with development ids and one with ids to be indexed.
 |      The test and development sets contain the most recent posts in the subforum, such that each contains about 15% of all the posts that have duplicates.
 |      They have been assigned alternately to the test and devel sets, so they are quite similar.
 |      Both test and development sets also contain posts that do not have any duplicates, in the actual proportion of the particular subforum.
 |  

### GENERAL POST/QUESTION METHODS ###

 |  get_posts_with_and_without_duplicates(self)
 |      Takes no input and returns two lists: one with all posts that have at least one duplicate, and one with all posts that don't have any duplicates. In that order.
 |      Calling this method is quicker than calling get_posts_with_duplicates() followed by get_posts_without_duplicates() is you want both dups and non-dups.
 |  
 |  get_posts_with_duplicates(self)
 |      Takes no input and returns a list of all posts that have at least one duplicate.
 |  
 |  get_posts_without_duplicates(self)
 |      Takes no input and returns a list of all posts that don't have any duplicates.
 |   
 |  get_ordered_list_of_posts(self)
 |      Takes no input and returns a list of tuples (postid, datetime object), ordered chronologically from newest to oldest post.
 |   
 |  get_random_pair_of_posts(self)
 |      Takes no input and returns a tuple with two random post ids and a duplicate verdict. The second is always lower than the first. 
 |      Example: (4865, 553, 'dup')
 |      Other values for the verdict are: 'related' and 'nondup'.
 |  
 |  get_random_postid(self)
 |      Takes no input and returns a random post id.
 |  
 |  get_all_postids(self)
 |      Takes no input and returns a list of ALL post ids.
 |  

### PARTICULAR POST/QUESTION METHODS ###

 |  get_posttitle(self, postid)
 |      Takes a post id as input and returns the title of the post.
 |  
 |  get_postbody(self, postid)
 |      Takes a post id as input and returns the body of the post.
 |  
 |  get_post_title_and_body(self, postid)
 |      Takes a post id as input and returns the title and the body of the post together as one string, so in other words, the full initial post.
 |  
 |  get_postdate(self, postid)
 |      Takes a post id as input and returns the date the post was posted in YYYY-MM-DD format.
 |  
 |  get_posttime(self, postid)
 |      Takes a post id as input and returns the time the post was posted in HH:MM:SS format.
 |  
 |  get_viewcount(self, postid)
 |      Takes a post id as input and returns the number of times the post has been looked at by users.
 |  
 |  get_favoritecount(self, postid)
 |      Takes a post id as input and returns an integer representing the nr of times this post has been favoured by a user.
 |      More information on what that means can be found here: http://meta.stackexchange.com/questions/53585/how-do-favorite-questions-work
 |  
 |  get_postscore(self, postid)
 |      Takes a post id as input and returns the score of the post. This is the number of upvotes minus the number of downvotes is has received.
 |  
 |  get_postuserid(self, postid)
 |      Takes a post id as input and returns the userid of the person that posted it. Returns False if the user is not known.
 |  
 |  get_duplicates(self, postid)
 |      Takes a post id as input and returns a list of ids of posts that have been labeled as a duplicate of it.
 |    
 |  get_related(self, postid)
 |      Takes a post id as input and returns a list of ids of posts that have been labeled as related to it.
 |  
 |  get_tags(self, postid)
 |      Takes a post id as input and returns a list of tags.
 |  

### ANSWER METHODS ###

 |  get_answers(self, postid)
 |      Takes a post id as input and returns a list of answer ids.
 |  
 |  get_answercount(self, postid)
 |      Takes a post id as input and returns an integer representing the number of answers it has received.
 |  
 |  get_answer_parentid(self, answerid)
 |      Takes an answer id as input and returns its parent id: the id of the post it is an answer of.
 |  
 |  get_acceptedanswer(self, postid)
 |      Takes a post id as input and returns the answer id of the accepted answer if it exists, else it returns False.
 |  
 |  get_answerbody(self, answerid)
 |      Takes an answer id as input and returns the body of the answer. That is the text of the answer.
 |  
 |  get_answerdate(self, answerid)
 |      Takes an answer id as input and returns the date the answer was posted in YYYY-MM-DD format.
 |  
 |  get_answertime(self, answerid)
 |      Takes an answer id as input and returns the time the answer was posted in HH:MM:SS format.
 |  
 |  get_answerscore(self, answerid)
 |      Takes an answer id as input and returns an integer representing the score of the answer. This is the number of upvotes minus the number of downvotes is has received.
 |  
 |  get_answeruserid(self, answerid)
 |      Takes an answer id as input and returns the userid of the person that posted it. Returns False if the user is not known.
 |  

### COMMENT METHODS ###

 |  get_post_comments(self, postid)
 |      Takes a post id as input and returns a list of comment ids.
 |  
 |  get_answer_comments(self, answerid)
 |      Takes an answer id as in put and returns a list of comment ids.
 |  
 |  get_post_commentcount(self, postid)
 |      Takes a post id as input and returns and integer representing the number of comments this post has received.
 |  
 |  get_answer_commentcount(self, answerid)
 |      Takes an answer id as input and returns and integer representing the number of comments this answer has received.
 |  
 |  get_comment_parentid(self, commentid)
 |      Takes a comment id as input and returns its parent id: the id of the post or answer it is a comment to.
 |  
 |  get_comment_parenttype(self, commentid)
 |      Takes a comment id as input and returns either 'question' or 'answer', depending on the type of its parent id.
 |  
 |  get_commentbody(self, commentid)
 |      Takes a comment id as input and returns the body of the comment.
 |  
 |  get_commentdate(self, commentid)
 |      Takes a comment id as input and returns the date the comment was posted, in YYYY-MM-DD format.
 |  
 |  get_commenttime(self, commentid)
 |      Takes a comment id as input and returns the time the comment was posted, in HH:MM:SS format.
 |  
 |  get_commentscore(self, commentid)
 |      Takes a comment id as input and returns an integer representing the score of the comment. This is the number of upvotes minus the number of downvotes is has received.
 |  
 |  get_commentuserid(self, commentid)
 |      Takes a comment id as input and returns the id of the user that posted the comment.
 |  

### USER METHODS ###

 |  get_user_reputation(self, userid)
 |      Takes a user id as input and outputs an integer representing the reputation of the user.
 |      Information on what this means and how it is calculated can be found here http://stackoverflow.com/help/whats-reputation
 |  
 |  get_user_views(self, userid)
 |      Takes a user id as input and outputs an integer representing how often people have viewed a post by this user.
 | 
 |  get_user_upvotes(self, userid)
 |      Takes a user id as input and outputs an integer representing how many upvotes on posts or answers this user has received.
 |  
 |  get_user_downvotes(self, userid)
 |      Takes a user id as input and outputs an integer representing how many downvotes on posts or answers this user has received.
 |  
 |  get_user_joindate(self, userid)
 |      Takes a user id as input and outputs the date this user joined this subforum, in YYYY-MM-DD format.
 |  
 |  get_user_lastaccess(self, userid)
 |      Takes a user id as input and outputs the last time this user has logged into this subforum, in YYYY-MM-DD format.
 |  
 |  get_user_age(self, userid)
 |      Takes a user id as input and outputs the user's age as an integer, if known. Else it returns 'unknown'.
 |  
 |  get_user_posts(self, userid)
 |      Takes a user id as input and returns a list of the question posts he/she has made.
 |   
 |  get_user_answers(self, userid)
 |      Takes a user id as input and returns a list of the answers he/she has written.
 |  
 |  get_user_badges(self, userid)
 |      Takes a user id as input and returns a list of the badges this user has earned. 
 |      Information on what badges are and which ones can be earned can be found here: http://stackoverflow.com/help/badges
 |  

### CLEANING/PREPROCESSING METHODS ###

 |  tokenize(self, s)
 |      Takes a string as input, tokenizes it using NLTK (http://www.nltk.org) and returns a list of the tokens.
 |  
 |  supply_stopwords(self, filename)
 |      Takes as input a plain text file encoded in UTF-8 with one stop word per line and saves these internally in a stop word list.
 |      This list will be used in cleaning if perform_cleaning() is called with remove_stopwords=True.
 |  
 |  Data descriptor stopwords:
 |      Returns the current list of words that is used as the stop word list. It can be accessed via self.stopwords

 |  change_to_default_stopwords(self, stopwordset='middle')
 |      Changes the stopword list to one of the supplied ones: 'nltk', 'indri', 'short' or 'middle'. 'Middle' is the default.
 |      The NLTK stopword list contains 127 stopwords. (http://www.nltk.org/book/ch02.html#code-unusual)
 |      The Indri stopword list contains 418 stopwords. (http://www.lemurproject.org/stopwords/stoplist.dft)
 |      Short = ["a", "an", "the", "yes", "no", "thanks"]
 |      Middle = ["in", "on", "at", "a", "an", "is", "be", "was", "I", "you", "the", "do", "did", "of", "so", "for", "with", "yes", "thanks"]
 |      To be able to use the NLTK stopwords, they need to be downloaded first. See: http://www.nltk.org/data.html for more info.
 |      If the data is not downloaded first, the script will default to the NLTK stopword list of November 2015.
 |  
 |  perform_cleaning(self, s, remove_stopwords=False, remove_punct=False, stem=False)
 |      Takes a string as input and returns a cleaned version.
 |      - The string will be lowercased and newlines removed.
 |      - HTML tags will be removed.
 |      - Mentions of possible duplicates will be removed.
 |      - URLs pointing to other StackExchange threads are turned into 'stackexchange-url'.
 |      - Blocks of code will be removed.
 |      - Contracted forms will be expanded. E.g. "didn't" --> "did not".
 |      - '&amp;' will be turned into 'and'.
 |      - Other HTML entities will be removed, and string matching the following pattern too: '&#?[a-z]+;'.
 |      - Whitespace is added around punctuation
 |      OPTIONAL ARGUMENTS:
 |      remove_stopwords: removed stop words. (Values: True or False)
 |      remove_punct: punctuation is removed, except for punctuation in URLs and numbers. (Values: True or False)
 |      stem: stemming is performed via the Porter stemmer as implemented in the NLTK (http://www.nltk.org/). (Values: True or False)
 |  

### EVALUATION METHODS FOR RETRIEVAL ###

 |  average_ndcg_at(self, scorefile, cutoff=None, include_related_posts=False)
 |      Takes a file with scores and a cutoff point as input and returns the Normalised Discounted Cumulative Gain at the cutoff point. The default is 10.
 |      If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant. 
 |      See "Cumulated Gain-based Evaluation of IR Techniques" by Jarvelin and Kekalainen 2002 for more information on this metric.
 |      Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. 
 |      Just for extra information: Taking related posts into account can lower the score if these documents are not returned, because they appear in the ideal ranking that is used in the calculation of the metric. This is not the case for the other retrieval evaluation metrics.
 |  
 |  average_precision_at(self, scorefile, cutoff=None, include_related_posts=False)
 |      Takes a file with scores and optionally a cutoff point as input and returns the Precision (at this cutoff, if specified). 
 |      If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.
 |      Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable.
 |  
 |  average_recall_at(self, scorefile, cutoff=None, include_related_posts=False)
 |      Takes a file with scores and optionally a cutoff point as input and returns the Recall (at this cutoff, if specified). 
 |      If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.
 |      Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable.
 |  
 |  mean_average_precision(self, scorefile, include_related_posts=False)
 |      Takes a file with scores as input and returns the Mean Average Precision (MAP) score.
 |      If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.
 |      Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable.
 |  
 |  mean_reciprocal_rank(self, scorefile)
 |      Takes a file with scores as input and returns the Mean Reciprocal Rank (MRR) score.
 |  

    The input to the evaluation metric methods (the scorefile), should be a plain text file with one query per line in the following format:

    queryid1    result1 result2 result3 etc.
    queryid2    result1 result2 result3 etc.

    Both the query id and results should be post ids. They should be separated either by a space or a TAB.


### EVALUATION METHODS FOR CLASSIFICATION ###

 |  evaluate_classification(self, scorefile)
 |      Takes a file with scores as input and returns a dictionary with the Precision, Recall, F1-score and Accuracy.
 |      The file with scores should have the same format as the classification training and test sets:
 |      One line per classification with two space separated postids followed by a 1 for duplicates, or 0 for non-duplicates.
 |  


    -----------------------------

    Here are some examples of how to use the script:

    >>> import query_cqadupstack as qcqa
    >>> o = qcqa.load_subforum('/home/hoogeveen/datasets/stackexchange/webmasters.zip')
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
    u'<p>I'm implementing a mobile-friendly version of our corporate web site and will be using <a href="http://wurfl.sourceforge.net/" rel="nofollow" title="WURFL">WURFL</a> to detect mobile browsers and redirect them to our mobile site.  Having recently purchased an Android tablet, I've found that many sites consider it to be a mobile device even though it has a large 10" screen and it's perfectly capable of handling sites designed using standard desktop resolutions.</p>

<p>My plan is to use WURFL, examine the device capabilities and treat anything with a resolution width of less than 700px as a mobile device, but I'd like some input as to that sweet spot for determining mobile vs desktop.</p>
'
    >>> o.perform_cleaning(o.get_postbody('18957'))
    u'i am implementing a mobile-friendly version of our corporate web site and will be using wurfl to detect mobile browsers and redirect them to our mobile site . having recently purchased an android tablet , i have found that many sites consider it to be a mobile device even though it has a large 10" screen and it is perfectly capable of handling sites designed using standard desktop resolutions . my plan is to use wurfl , examine the device capabilities and treat anything with a resolution width of less than 700px as a mobile device , but i would like some input as to that sweet spot for determining mobile vs desktop .'
    >>> for a in o.get_answers('18957'):
    ...     print a, o.get_answerscore(a)
    ... 
    18985 1
    18980 0
    >>> o.get_tags(o.get_random_postid())
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
    ['in', 'on', 'at', 'a', 'an', 'is', 'be', 'was', 'I', 'you', 'the', 'do', 'did', 'of', 'so', 'for', 'with']

    -----------------------------

For questions please contact Doris Hoogeveen at doris dot hoogeveen at gmail.
