The scripts in this directory can be used to manipulate the CQADupStack data, downloadable from http://nlp.cis.unimelb.edu.au/resources/cqadupstack/.

CQADupStack contains 12 Stackexchange (http://stackexchange.com/) subforums which have been preprocessed as described in the paper mentioned below.
The StackExchange data dump that forms the basis of this set is the version released on September 26, 2014.

query_cqadupstack.py enables easy access to all the different fields in CQADupStack. It can be used to split the data into pre-defined retrieval or classification splits, and it can be used to evaluate the output of your system, using one of several evaluation metrics available.

Please cite the following paper when making use of CQADupStack:

@inproceedings{hoogeveen2015, <br />
 author = {Hoogeveen, Doris and Verspoor, Karin M. and Baldwin, Timothy}, <br />
 title = {CQADupStack: A Benchmark Data Set for Community Question-Answering Research}, <br />
 booktitle = {Proceedings of the 20th Australasian Document Computing Symposium (ADCS)}, <br />
 series = {ADCS '15}, <br />
 year = {2015}, <br />
 isbn = {978-1-4503-4040-3}, <br />
 location = {Parramatta, NSW, Australia}, <br />
 pages = {3:1--3:8}, <br />
 articleno = {3}, <br />
 numpages = {8}, <br />
 url = {http://doi.acm.org/10.1145/2838931.2838934}, <br />
 doi = {10.1145/2838931.2838934}, <br />
 acmid = {2838934}, <br />
 publisher = {ACM}, <br />
 address = {New York, NY, USA}, <br />
} 

For licensing information please see the LICENCE file.

For more information on the structure of the files in the data set, please see the README file that comes with the data.
The README file you are reading now contains information on the query script (query_cqadupstack.py) only.

query_cqadupstack.py contains a main function called load_subforum(). It has one argument: a StackExchange subforum.zip file from CQADupStack.
load_subforum() uses this file to create a 'Subforum' object and returns this.
Alternatively, you can make a subforum object directly by calling the class 'Subforum' yourself. Just like load_subforum() it needs a zipped subforum file as its only argument.

Subforum objects can be queried using the following methods: (examples on how to use them can be found at the end of this file)

#### SPLIT METHODS ####

-  split_for_classification(self) <br />
        Takes no input and makes twelve plain text files: a small test set, a large test set, and 10 files for the training set (trainpairs_[01-10].txt, testpairs_small.txt and testpairs_large.txt). <br />
        Each line in these sets contains two postids and a label (1 for duplicate, 0 for non-duplicate), separated by a space. Each of these pairs is a training or test instance. <br />
        The training pairs have been divided over ten different files. These can be used for ten-fold cross-validation. <br />
         <br />
        To make the split all posts are ordered according to date. Next the set is cut into two at a certain date. <br />
        This date is chosen such that the test set will ideally contain at least 200 duplicate pairs, or if that iss not possible, as many as possible, with a minimum of 100, and the train set contains at least four times as many. <br />
        The test set contains pairs of posts with a date after the cutoff date. Posts are only combined with older posts, as would be the case in a real world setting. The training set contains pairs of posts with a date before the cutoff date. Again, posts are only combined with older posts.  <br />
        A consequence of this approach is that we lose a number of duplicate pairs, namely the ones that are posted after the cutoff date, but their duplicate was posted before.  <br />
        Both testpairs_large.txt and the trainpairs files will contain millions of pairs. <br />
        Testpairs_small.txt contains a subset of testpairs_large.txt. It is a smaller and more balanced set, which contains ten times more non-duplicate pairs than duplicate pairs. <br />
     <br />
-  split_for_retrieval(self) <br />
        Takes no input and returns three lists: one with test ids, one with development ids and one with ids to be indexed. <br />
        The test and development sets contain the most recent posts in the subforum, such that each contains about 15% of all the posts that have duplicates. <br />
        They have been assigned alternately to the test and devel sets, so they are quite similar. <br />
        Both test and development sets also contain posts that do not have any duplicates, in the actual proportion of the particular subforum. <br />
     <br />

#### GENERAL POST/QUESTION METHODS ####

-  get_posts_with_and_without_duplicates(self) <br />
        Takes no input and returns two lists: one with all posts that have at least one duplicate, and one with all posts that don't have any duplicates. In that order. <br />
        Calling this method is quicker than calling get_posts_with_duplicates() followed by get_posts_without_duplicates() is you want both dups and non-dups. <br />
   <br />
-  get_posts_with_duplicates(self) <br />
        Takes no input and returns a list of all posts that have at least one duplicate. <br />
   <br />
-  get_posts_without_duplicates(self) <br />
        Takes no input and returns a list of all posts that don't have any duplicates. <br />
    <br />
-  get_ordered_list_of_posts(self) <br />
        Takes no input and returns a list of tuples (postid, datetime object), ordered chronologically from newest to oldest post. <br />
    <br />
-  get_random_pair_of_posts(self) <br />
        Takes no input and returns a tuple with two random post ids and a duplicate verdict. The second is always lower than the first.  <br />
        Example: (4865, 553, 'dup') <br />
        Other values for the verdict are: 'related' and 'nondup'. <br />
    <br />
-  get_random_postid(self) <br />
        Takes no input and returns a random post id. <br />
    <br />
-  get_all_postids(self) <br />
        Takes no input and returns a list of ALL post ids. <br />
    <br />
-  get_true_label(self, postid1, postid2) <br />
	Takes two postids as input and returns the true label, which is one of "dup", "nodup" or "related". <br />
    <br />

#### PARTICULAR POST/QUESTION METHODS ####

-  get_posttitle(self, postid) <br />
        Takes a post id as input and returns the title of the post. <br />
    <br />
-  get_postbody(self, postid) <br />
        Takes a post id as input and returns the body of the post. <br />
    <br />
-  get_post_title_and_body(self, postid) <br />
        Takes a post id as input and returns the title and the body of the post together as one string, so in other words, the full initial post. <br />
    <br />
-  get_postdate(self, postid) <br />
        Takes a post id as input and returns the date the post was posted in YYYY-MM-DD format. <br />
    <br />
-  get_posttime(self, postid) <br />
        Takes a post id as input and returns the time the post was posted in HH:MM:SS format. <br />
    <br />
-  get_viewcount(self, postid) <br />
        Takes a post id as input and returns the number of times the post has been looked at by users. <br />
    <br />
-  get_favoritecount(self, postid) <br />
        Takes a post id as input and returns an integer representing the nr of times this post has been favoured by a user. <br />
        More information on what that means can be found here: http://meta.stackexchange.com/questions/53585/how-do-favorite-questions-work <br />
    <br />
-  get_postscore(self, postid) <br />
        Takes a post id as input and returns the score of the post. This is the number of upvotes minus the number of downvotes is has received. <br />
    <br />
-  get_postuserid(self, postid) <br />
        Takes a post id as input and returns the userid of the person that posted it. Returns False if the user is not known. <br />
    <br />
-  get_duplicates(self, postid) <br />
        Takes a post id as input and returns a list of ids of posts that have been labeled as a duplicate of it. <br />
      <br />
-  get_related(self, postid) <br />
        Takes a post id as input and returns a list of ids of posts that have been labeled as related to it. <br />
    <br />
-  get_tags(self, postid) <br />
        Takes a post id as input and returns a list of tags. <br />
    <br />

#### ANSWER METHODS ####

-  get_answers(self, postid) <br />
        Takes a post id as input and returns a list of answer ids. <br />
    <br />
-  get_answercount(self, postid) <br />
        Takes a post id as input and returns an integer representing the number of answers it has received. <br />
    <br />
-  get_answer_parentid(self, answerid) <br />
        Takes an answer id as input and returns its parent id: the id of the post it is an answer of. <br />
    <br />
-  get_acceptedanswer(self, postid) <br />
        Takes a post id as input and returns the answer id of the accepted answer if it exists, else it returns False. <br />
    <br />
-  get_answerbody(self, answerid) <br />
        Takes an answer id as input and returns the body of the answer. That is the text of the answer. <br />
    <br />
-  get_answerdate(self, answerid) <br />
        Takes an answer id as input and returns the date the answer was posted in YYYY-MM-DD format. <br />
    <br />
-  get_answertime(self, answerid) <br />
        Takes an answer id as input and returns the time the answer was posted in HH:MM:SS format. <br />
    <br />
-  get_answerscore(self, answerid) <br />
        Takes an answer id as input and returns an integer representing the score of the answer. This is the number of upvotes minus the number of downvotes is has received. <br />
    <br />
-  get_answeruserid(self, answerid) <br />
        Takes an answer id as input and returns the userid of the person that posted it. Returns False if the user is not known. <br />
    <br />

#### COMMENT METHODS ####

-  get_post_comments(self, postid) <br />
        Takes a post id as input and returns a list of comment ids. <br />
    <br />
-  get_answer_comments(self, answerid) <br />
        Takes an answer id as in put and returns a list of comment ids. <br />
    <br />
-  get_post_commentcount(self, postid) <br />
        Takes a post id as input and returns and integer representing the number of comments this post has received. <br />
    <br />
-  get_answer_commentcount(self, answerid) <br />
        Takes an answer id as input and returns and integer representing the number of comments this answer has received. <br />
  <br />  
-  get_comment_parentid(self, commentid) <br />
        Takes a comment id as input and returns its parent id: the id of the post or answer it is a comment to. <br />
    <br />
-  get_comment_parenttype(self, commentid) <br />
        Takes a comment id as input and returns either 'question' or 'answer', depending on the type of its parent id. <br />
    <br />
-  get_commentbody(self, commentid) <br />
        Takes a comment id as input and returns the body of the comment. <br />
    <br />
-  get_commentdate(self, commentid) <br />
        Takes a comment id as input and returns the date the comment was posted, in YYYY-MM-DD format. <br />
    <br />
-  get_commenttime(self, commentid) <br />
        Takes a comment id as input and returns the time the comment was posted, in HH:MM:SS format. <br />
    <br />
-  get_commentscore(self, commentid) <br />
        Takes a comment id as input and returns an integer representing the score of the comment. This is the number of upvotes minus the number of downvotes is has received. <br />
    <br />
-  get_commentuserid(self, commentid) <br />
        Takes a comment id as input and returns the id of the user that posted the comment. <br />
    <br />

#### USER METHODS ####

-  get_user_reputation(self, userid) <br />
        Takes a user id as input and outputs an integer representing the reputation of the user. <br />
       Information on what this means and how it is calculated can be found here http://stackoverflow.com/help/whats-reputation <br />
    <br />
-  get_user_views(self, userid) <br />
        Takes a user id as input and outputs an integer representing how often people have viewed a post by this user. <br />
   <br />
-  get_user_upvotes(self, userid) <br />
        Takes a user id as input and outputs an integer representing how many upvotes on posts or answers this user has received. <br />
    <br />
-  get_user_downvotes(self, userid) <br />
        Takes a user id as input and outputs an integer representing how many downvotes on posts or answers this user has received. <br />
    <br />
-  get_user_joindate(self, userid) <br />
        Takes a user id as input and outputs the date this user joined this subforum, in YYYY-MM-DD format. <br />
    <br />
-  get_user_lastaccess(self, userid) <br />
        Takes a user id as input and outputs the last time this user has logged into this subforum, in YYYY-MM-DD format. <br />
  <br />  
-  get_user_age(self, userid) <br />
        Takes a user id as input and outputs the user's age as an integer, if known. Else it returns 'unknown'. <br />
    <br />
-  get_user_posts(self, userid) <br />
        Takes a user id as input and returns a list of the question posts he/she has made. <br />
     <br />
-  get_user_answers(self, userid) <br />
        Takes a user id as input and returns a list of the answers he/she has written. <br />
    <br />
-  get_user_badges(self, userid) <br />
        Takes a user id as input and returns a list of the badges this user has earned.  <br />
        Information on what badges are and which ones can be earned can be found here: http://stackoverflow.com/help/badges <br />
  <br />  

#### CLEANING/PREPROCESSING METHODS ####

-  tokenize(self, s) <br />
        Takes a string as input, tokenizes it using NLTK (http://www.nltk.org) and returns a list of the tokens. <br />
    <br />
-  supply_stopwords(self, filename) <br />
        Takes as input a plain text file encoded in UTF-8 with one stop word per line and saves these internally in a stop word list. <br />
        This list will be used in cleaning if perform_cleaning() is called with remove_stopwords=True. <br />
    <br />
-  Data descriptor stopwords: <br />
        Returns the current list of words that is used as the stop word list. It can be accessed via self.stopwords <br />

-  change_to_default_stopwords(self, stopwordset='middle') <br />
        Changes the stopword list to one of the supplied ones: 'nltk', 'indri', 'short' or 'middle'. 'Middle' is the default. <br />
        The NLTK stopword list contains 127 stopwords. (http://www.nltk.org/book/ch02.html#code-unusual) <br />
        The Indri stopword list contains 418 stopwords. (http://www.lemurproject.org/stopwords/stoplist.dft) <br />
        Short = ["a", "an", "the", "yes", "no", "thanks"] <br />
        Middle = ["in", "on", "at", "a", "an", "is", "be", "was", "I", "you", "the", "do", "did", "of", "so", "for", "with", "yes", "thanks"] <br />
        To be able to use the NLTK stopwords, they need to be downloaded first. See: http://www.nltk.org/data.html for more info. <br />
        If the data is not downloaded first, the script will default to the NLTK stopword list of November 2015. <br />
    <br />
-  perform_cleaning(self, s, remove_stopwords=False, remove_punct=False, stem=False) <br />
        Takes a string as input and returns a cleaned version. <br />
        - The string will be lowercased and newlines removed. <br />
        - HTML tags will be removed. <br />
        - Mentions of possible duplicates will be removed. <br />
        - URLs pointing to other StackExchange threads are turned into 'stackexchange-url'. <br />
        - Blocks of code will be removed. <br />
        - Contracted forms will be expanded. E.g. "didn't" --> "did not". <br />
        - '&amp;' will be turned into 'and'. <br />
        - Other HTML entities will be removed, and string matching the following pattern too: '&#?[a-z]+;'. <br />
        - Whitespace is added around punctuation <br />
        OPTIONAL ARGUMENTS: <br />
        remove_stopwords: removed stop words. (Values: True or False) <br />
        remove_punct: punctuation is removed, except for punctuation in URLs and numbers. (Values: True or False) <br />
        stem: stemming is performed via the Porter stemmer as implemented in the NLTK (http://www.nltk.org/). (Values: True or False) <br />
    <br />
-  url_cleaning(self, s) <br />
	Takes a string as input and removes references to possible duplicate posts, and other stackexchange urls.
   <br />

#### EVALUATION METHODS FOR RETRIEVAL ####

-  average_ndcg_at(self, scorefile, cutoff=None, include_related_posts=False) <br />
        Takes a file with scores and a cutoff point as input and returns the Normalised Discounted Cumulative Gain at the cutoff point. The default is 10. <br />
        If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant.  <br />
        See "Cumulated Gain-based Evaluation of IR Techniques" by Jarvelin and Kekalainen 2002 for more information on this metric. <br />
        Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable.  <br />
        Just for extra information: Taking related posts into account can lower the score if these documents are not returned, because they appear in the ideal ranking that is used in the calculation of the metric. This is not the case for the other retrieval evaluation metrics. <br />
    <br />
-  average_precision_at(self, scorefile, cutoff=None, include_related_posts=False) <br />
        Takes a file with scores and optionally a cutoff point as input and returns the Precision (at this cutoff, if specified).  <br />
        If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant. <br />
        Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. <br />
    <br />
-  average_recall_at(self, scorefile, cutoff=None, include_related_posts=False) <br />
        Takes a file with scores and optionally a cutoff point as input and returns the Recall (at this cutoff, if specified).  <br />
        If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant. <br />
        Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. <br />
    <br />
-  mean_average_precision(self, scorefile, include_related_posts=False) <br />
        Takes a file with scores as input and returns the Mean Average Precision (MAP) score. <br />
        If the optional argument 'include_related_posts' is set to True, then related posts are treated as half relevant. <br />
        Only queries with relevant posts are taken into account. Queries with ONLY related posts are ignored, even with include_related_posts=True, to make the scores better comparable. <br />
    <br />
-  mean_reciprocal_rank(self, scorefile) <br />
        Takes a file with scores as input and returns the Mean Reciprocal Rank (MRR) score. <br />
    

    The input to the evaluation metric methods (the scorefile), should be a plain text file with one query per line in the following format:

        queryid1    result1 result2 result3 etc. <br />
        queryid2    result1 result2 result3 etc.

    Both the query id and results should be post ids. They should be separated either by a space or a TAB.


#### EVALUATION METHODS FOR CLASSIFICATION ####

-  evaluate_classification(self, scorefile) <br />
        Takes a file with scores as input and returns a dictionary with the Precision, Recall, F1-score, Accuracy and Precision and Recall per class. <br />
        The file with scores should have the same format as the classification training and test sets: <br />
        One line per classification with two space separated postids followed by a 1 for duplicates, or 0 for non-duplicates. <br />
   <br />
-  plot_roc(self, scorefile, plotfilename) <br />
	Takes a file with scores and a the name of a plot file (png) as input and returns the false positive rates (list), true positive rates (list), thresholds at which they were computed (list) and the area under the curve (float). The plot will be written to the supplied plot file. 
        The scores can either be probability estimates of the positive class, confidence values, or binary decisions. 
        This method requires scikit-learn to be installed: http://scikit-learn.org/stable/install.html 
        This method only computes the ROC curve for the positive class. See http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html for an example on how to make curves for multiple classes (for instance when you have a third class for the related questions).   <br />


    -----------------------------

    Here are some examples of how to use the script:

    >\>\>\> import query_cqadupstack as qcqa <br />
    >\>\>\> o = qcqa.load_subforum('/home/hoogeveen/datasets/CQADupStack/webmasters.zip') <br />
    >\>\>\> testset, develset, indexset = o.split_for_retrieval() <br />
    >\>\>\> len(develset) <br />
    >1862 <br />
    >\>\>\> for i in develset: <br />
    >        ...     if o.get_duplicates(i) != []: <br />
    >        ...         print i, o.get_duplicates(i) <br />
    >        ...  <br />
    >69050 [u'8710'] <br />
    >68979 [u'52812'] <br />
    >68897 [u'6073'] <br />
    >68856 [u'6073'] <br />
    >68689 [u'20838'] <br />
    >etc. <br />
    >\>\>\> o.get_posttitle('18957') <br />
    >u'What do you consider a "mobile" device?' <br />
    >\>\>\> o.get_postbody('18957') <br />
    >u'\<p\>I'm implementing a mobile-friendly version of our corporate web site and will be using \<a href="http://wurfl.sourceforge.net/" rel="nofollow" title="WURFL"\>WURFL\</a\> to detect mobile browsers and redirect them to our mobile site.  Having recently purchased an Android tablet, I've found that many sites consider it to be a mobile device even though it has a large 10" screen and it's perfectly capable of handling sites designed using standard desktop resolutions.\</p\>\<p\>My plan is to use WURFL, examine the device capabilities and treat anything with a resolution width of less than 700px as a mobile device, but I'd like some input as to that sweet spot for determining mobile vs desktop.\</p\>
\' <br />
    >\>\>\> o.perform_cleaning(o.get_postbody('18957')) <br />
    >u'i am implementing a mobile-friendly version of our corporate web site and will be using wurfl to detect mobile browsers and redirect them to our mobile site . having recently purchased an android tablet , i have found that many sites consider it to be a mobile device even though it has a large 10" screen and it is perfectly capable of handling sites designed using standard desktop resolutions . my plan is to use wurfl , examine the device capabilities and treat anything with a resolution width of less than 700px as a mobile device , but i would like some input as to that sweet spot for determining mobile vs desktop .' <br />
    >\>\>\> for a in o.get_answers('18957'): <br />
    >        ...     print a, o.get_answerscore(a) <br />
    >        ...  <br />
    >18985 1 <br />
    >18980 0 <br />
    >\>\>\> o.get_tags(o.get_random_postid()) <br />
    >[u'wordpress', u'redirects', u'blog', u'plugin'] <br />
    >\>\>\> o.get_postuserid('18957') <br />
    >u'1907' <br />
    >\>\>\> o.get_user_posts('1907') <br />
    >[u'18957'] <br />
    >\>\>\> o.get_user_views('1907') <br />
    >6 <br />
    >\>\>\> o.stopwords <br />
    >['in', 'on', 'at', 'a', 'an', 'is', 'be', 'was', 'I', 'you', 'the', 'do', 'did', 'of', 'so', 'for', 'with'] <br />
    >\>\>\> o.supply_stopwords('new_stopwords_testfile.txt') <br />
    >\>\>\> o.stopwords <br />
    >[u'new_stopword1', u'new_stopword2', u'new_stopword3'] <br />
    >\>\>\> o.change_to_default_stopwords() <br />
    >\>\>\> o.stopwords <br />
    >['in', 'on', 'at', 'a', 'an', 'is', 'be', 'was', 'I', 'you', 'the', 'do', 'did', 'of', 'so', 'for', 'with'] <br />

    -----------------------------

For questions please contact Doris Hoogeveen at doris dot hoogeveen at gmail.
