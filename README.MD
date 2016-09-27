This software was created as a submission to an assignment given as a part of the course called Information Retrieval, taught at BITS Pilani Hyderabad Campus

##Pre-requisites:##
Before running the software please make sure you have **nltk** package installed. Also make sure you have downloaded nltk's *brown* corpus.

##How to run:##
Run following command in a terminal:
				python run.py

##Files:##
**indexer.py:**
This module generates tokens out of the documents and creates necessary data structures and also serialize those data structures. \nThis module ultimately creates the inverted indexes needed for further processing.

**normalize.py:**
This module helps to calculate normalized vectors of each document based on the inverted indexes.

**query.py:**
This module helps the user to query the corpus and fetch the relevant documents

**first_run.indicator:**
Indicates if the software is running for the first time. If so, the system would creates tokens and create indexes in a fresh manner. If not, it would just use the indexes already built.