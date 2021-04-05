## Task 1 ##

* [x] Create a crawler,
* [x] download more or equal to 100 pages' texts,
* [x] store them to archive,
* [x] create an index.txt file that contains pages' IDs and their full links

We use Scrapy framework to do this task. It provides a 
functionality for web-crawlers. 

To run spider:
```bash 
cd "task1_rawler"
scrapy crawl spider-task
```
***


## Task 2 ##

* [x] Separate single words from 1st task files (tokenization)
* [x] Save words from a previous task to file in format  
    * \<word1>\n \<word2>\n ... \<wordn> (words.txt)
* [x] From words get lemmas and collect them into file. Format of data:  
    * \<lemma1> \<word1> \<word2> ...\n  
    * \<lemma2> \<word1> \<word2> ...\n ... (tokens.txt)

Source code in a file 'Tokenization/token_and_lemma.py'. 

To run start main.py in project (mySearch) base dir. 
```bash
python main.py
```
***


## Task 3 ##

* [x] Build an inverted index
* [x] Implement Boolean search in created index

Boolean search implemented in BooleanSearch class in 
'Index/index_search.py' file. It creates an inverted index 
within initialization.

To run start main.py in project (mySearch) base dir. 
```bash
python main.py
```
***


## Task 4 ##

* [x] Calculate tf for terms
* [x] Calculate idf
* [x] Calculate tf-idf
* [x] Write results to file in format:
   * \<term> \<idf> \<tf-idf>\n
  
To run:
```bash
python main.py
```
***

## Task 5 ##
* [x] Implement fully operational search engine with written index

```bash
python manage.py runserver
```
***