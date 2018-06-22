**CAUTION [2018-06-22]: This repository is currently being overhauled and in a state of disarray!**

---

Welcome to tweetspy
===================

    This is my own adaptation of a tweepy stream listener in a distributed cluster environment.
    The code is currently broken and is about 1/2 way fixed.
    Each script plays a unique role in the streaming, serving, cleaning, parsing, plotting and monitoring processes.

    Have a look at the videos below for an idea of what this collection of programs can do.

---

Video Examples
==============

Full screen demo of all 34 computers running
--------------------------------------------
    On the left screen are the workers cleaning tweets.  On the right are the streamer, monitor, file server and parser.

[![streamer.py](http://img.youtube.com/vi/66tErZ3Im3A/0.jpg)](https://www.youtube.com/watch?v=66tErZ3Im3A)

Streaming Tweets to disc - streamer.py
--------------------------------------

[![streamer.py](http://img.youtube.com/vi/UI9wrz7934Q/0.jpg)](https://www.youtube.com/watch?v=UI9wrz7934Q)

Serving downloaded Tweets local processes - fileserver.py
---------------------------------------------------------

[![fileserver.py](http://img.youtube.com/vi/pFbGDQ-eL-A/0.jpg)](https://www.youtube.com/watch?v=pFbGDQ-eL-A)

Cleaning Tweets - cleaner.py
----------------------------

[![cleaner.py](http://img.youtube.com/vi/hnJ68ZkK3MU/0.jpg)](https://www.youtube.com/watch?v=hnJ68ZkK3MU)

Parsing cleaned Tweets - parser.py
----------------------------------

[![parser.py](http://img.youtube.com/vi/jc_q7n1tGVQ/0.jpg)](https://www.youtube.com/watch?v=jc_q7n1tGVQ)
