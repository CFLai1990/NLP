import re
import pandas as pd
import nltk
import os, sys
# from stanfordcorenlp import StanfordCoreNLP

shape_list = ["dot", "line", "band", "circle", "rectangle", "triangle", "star"]
color_list = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "grey", "black", "white"]
pattern_list = [r"Find(.+?)\."]


def parse_document(document):
    document = re.sub('\n', ' ', document)
    if isinstance(document, str):
       document = document
    else:
       raise ValueError('Document is not string!')
    document = document.strip()
    sentences = nltk.sent_tokenize(document)
    sentences = [sentence.strip() for sentence in sentences]
    return sentences


def nlp_nltk(text):
    # tokenize sentences
    sentences = parse_document(text)
    sentence_list = {}

    for i, sentence in enumerate(sentences):
        sentence_list['st_' + str(i)] = sentence

    # return output1 sentence_list
    # print("output1: ", sentence_list)

    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    # tag sentences and use nltk's Named Entity Chunker
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    ne_chunked_sents = [nltk.ne_chunk(tagged) for tagged in tagged_sentences]

    # extract all named entities
    # named_entities = []
    # for i, ne_tagged_sentence in enumerate(ne_chunked_sents):
    #     for tagged_tree in ne_tagged_sentence:
    #         # extract only chunks having NE labels
    #         if hasattr(tagged_tree, 'label'):
    #             entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #get NE name
    #             entity_type = tagged_tree.label() # get NE category
    #             entity = {
    #                 "entity_name": entity_name,
    #                 "entity_type": entity_type,
    #                 'name': '',
    #                 "sentence": 'st_' + str(i),
    #                 'color': '',
    #                 'boundary': '',
    #             }
    #             named_entities.append(entity)

    # print("output2: ", named_entities)


    named_entities = []

    for i, sentence in enumerate(sentences):
        results = re.findall(pattern_list[0], sentence)

        words_list = nltk.word_tokenize(sentence)
        tagged_sentences = nltk.pos_tag(words_list)
        shape = list(set(shape_list).intersection(set(words_list)))
        color = list(set(color_list).intersection(set(words_list)))
        name = [tagged[0] for tagged in tagged_sentences if tagged[1] == 'NN']
        entity = {
            "sentence": 'st_' + str(i),
            'name': name,
            'color': color,
            'shape': shape,
        }
        named_entities.append(entity)

    # print("output2: ", named_entities)

    return sentence_list, named_entities


if __name__ == '__main__':
    # sample document
    text = sys.argv[1]
    
    # text = "There is a red circle without stroke. Find the blue car."
    nlp_nltk(text)
    

    # nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2018-10-05')
    # os.environ['CORENLP_HOME'] = "/Users/Sara/Desktop/annotation_nlp/stanford-corenlp-full-2018-10-05"

    # sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
    # print('Tokenize:', nlp.word_tokenize(sentence))
    # print('Part of Speech:', nlp.pos_tag(sentence))
    # print('Named Entities:', nlp.ner(text))
    # print('Constituency Parsing:', nlp.parse(sentence))
    # print('Dependency Parsing:', nlp.dependency_parse(sentence))

    # nlp.close()

