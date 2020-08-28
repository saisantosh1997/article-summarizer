#import argparse
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict


#content=open('example.txt','r')

#content = sanitize_input(content)

#sentence_tokens, word_tokens = tokenize_content(content)  
#sentence_ranks = score_tokens(word_tokens, sentence_tokens)

#summary = summarize(sentence_ranks, sentence_tokens, args.length)



def sanitize_input(content):
    replace = {
        ord('\f') : ' ',
        ord('\t') : ' ',
        ord('\n') : ' ',
        ord('\r') : None
    }

    return content.translate(replace)
    #content.replace(" ", " ")
    #content.replace("\t"," ")
    #content.replace("\n"," ")

    #return content

#print (sanitize_input(content))

def tokenize_content(content):
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(content.lower())
    
    return [
        sent_tokenize(content),
        [word for word in words if word not in stop_words]    
    ]

def score_tokens(filterd_words, sentence_tokens):
    word_freq = FreqDist(filterd_words)

    ranking = defaultdict(int)

    for i, sentence in enumerate(sentence_tokens):
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                ranking[i] += word_freq[word]

    return ranking

def summarize(ranks, sentences, length):
    #if int(length) > len(sentences): 
     #   print("Error, more sentences requested than available. Adjust the length.")
      #  exit()

    indexes = nlargest(length, ranks, key=ranks.get)
    final_sentences = [sentences[j] for j in sorted(indexes)]
    return ' '.join(final_sentences) 

from flask import Flask, jsonify, flash, render_template, request
from sqlalchemy import true

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/', methods=['POST','GET'])
def home():
    #content_fd=open('example1.txt','r')  #give the file name to be read
    #content=content_fd.read()
    #length = float(input("Enter length of summary: "))
    return render_template("summary_form.html")

@app.route('/col',methods=['POST','GET'])
def col():
    if request.method:'POST'
    text=request.form['n1']
    length=int(request.form['n2'])
    content = sanitize_input(text)

    sentence_tokens, word_tokens = tokenize_content(content)  
    sentence_ranks = score_tokens(word_tokens, sentence_tokens)
    sen_len=len(sentence_tokens)
    if length>sen_len:
        return render_template("err.html")
    summ = summarize(sentence_ranks, sentence_tokens, length)
    return render_template("secondpage.html",summ=summ)
    #print(summary)
    #<h1> final_summary </h1>
    #<p> summary <p>
    #return jsonify({'summary':summary})
app.run()