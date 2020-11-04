from google.protobuf.json_format import MessageToDict
from google.cloud.language_v1 import enums
import string
import nltk
import json
import re

 #set api

class UserProcessor():

    #analyze sentiment
    def sentiment (self, client, document, encoding):
        print('Starting sentiment analyze')
        response = client.analyze_sentiment(document, encoding_type=encoding)
        return {"document_score":response.document_sentiment.score, "document_magnitude":response.document_sentiment.magnitude}


    #analyze entities
    def entities (self, client, document, encoding):
        print('Starting entity analyze')
        response = client.analyze_entities(document, encoding_type=encoding)
        types = {'EVENT':[0,0],'LOCATION':[0,0],'ORGANIZATION':[0,0],'PERSON':[0,0]}

        for entity in response.entities:
            # Get entity type, PERSON, LOCATION, ORGANIZATION, EVENT
            name = enums.Entity.Type(entity.type).name
            if name == 'EVENT' or name == 'LOCATION' or name == 'ORGANIZATION' or name == 'PERSON':
                types[name][1] += 1
                types[name][0] += entity.salience

        types['EVENT'] = types['EVENT'][0] / types['EVENT'][1]
        types['LOCATION'] = types['LOCATION'][0] / types['LOCATION'][1]
        types['ORGANIZATION'] = types['ORGANIZATION'][0] / types['ORGANIZATION'][1]
        types['PERSON'] = types['PERSON'][0] / types['PERSON'][1]

        return types

    #analyze syntax
    def syntax (self, client, document, encoding):
        print('Starting syntax analyze')
        response = client.analyze_syntax(document, encoding_type=encoding)
        response = MessageToDict(response)

        number_of_verbs = 0
        number_of_subj_imp_verbs = 0
        number_of_nouns = 0
        number_of_adjectives = 0
        number_of_adverbs = 0
        number_of_modal_verbs = 0
        number_of_singular_fs_pron = 0
        number_of_plural_f_pron = 0
        number_of_pronouns = 0

        for token in response['tokens']:
            
            if 'dependencyEdge' in token:
                if 'label' in token['dependencyEdge']:
                    if token['dependencyEdge']['label'] == 'VMOD':
                        number_of_modal_verbs += 1

            if 'partOfSpeech' in token:
                if 'tag' in token['partOfSpeech']:
                    if token['partOfSpeech']['tag'] == 'VERB':
                        number_of_verbs += 1

                    if token['partOfSpeech']['tag'] == 'NOUN':
                        number_of_nouns += 1

                    if token['partOfSpeech']['tag'] == 'ADJ':
                        number_of_adjectives += 1

                    if token['partOfSpeech']['tag']== 'ADV':
                        number_of_adverbs += 1

                    if token['partOfSpeech']['tag'] == 'PRON':
                        number_of_pronouns += 1

                    if 'mood' in token['partOfSpeech']:
                        if token['partOfSpeech']['tag'] == 'VERB' and token['partOfSpeech']['mood'] == 'SUBJUNCTIVE' or token['partOfSpeech']['mood'] == 'IMPERATIVE':
                            number_of_subj_imp_verbs += 1

                    if 'person' in token['partOfSpeech'] and 'number' in token['partOfSpeech']:
                        if token['partOfSpeech']['tag'] == 'PRON' and token['partOfSpeech']['person'] == 'FIRST' and token['partOfSpeech']['number'] == 'PLURAL':
                            number_of_plural_f_pron += 1
                        
                        if token['partOfSpeech']['tag'] == 'PRON' and token['partOfSpeech']['number'] == 'SINGULAR' and token['partOfSpeech']['person'] == 'FIRST' or token['partOfSpeech']['person'] == 'SECOND':
                            number_of_singular_fs_pron += 1

        syntax = {
            'number_of_verbs': number_of_verbs,
            'number_of_subj_imp_verbs': number_of_subj_imp_verbs,
            'number_of_nouns': number_of_nouns,
            'number_of_adjectives': number_of_adjectives,
            'number_of_adverbs': number_of_adverbs,
            'number_of_modal_verbs': number_of_modal_verbs,
            'number_of_plural_f_pron': number_of_plural_f_pron,
            'number_of_singular_fs_pron': number_of_singular_fs_pron,
            'number_of_pronouns': number_of_pronouns
        }

        return syntax


    #analyze syntax with nltk
    def text_lens(self, document):
        print('Starting text_lens analyze')
        number_of_tokens = len(nltk.word_tokenize(document['content']))

        clean_text = re.sub('\W+',' ', document['content'])
        words = clean_text.split()
        average_word_len = sum(len(word) for word in words) / len(words)

        sents = document['content'].split('.')
        average_sent_len = sum(len(x.split()) for x in sents) / len(sents)

        number_words_in_uppercase = sum(map(str.isupper, words))

        number_of_chars = len(''.join(e for e in document['content'] if e.isalnum()))

        lengths = {
            'number_of_tokens': number_of_tokens,
            'number_of_words_in_uppercase': number_words_in_uppercase,
            'number_of_chars': number_of_chars,
            'average_sent_len': average_sent_len,
            'average_word_len': average_word_len,
        }

        return lengths

    def pausality_calc (self, document):
        print('Starting pausality analyze')
        number_of_setences = len(document['content'].split('.'))
        count = lambda l1,l2: sum([1 for x in l1 if x in l2])
        quantity_punctuation = count(document['content'],set(string.punctuation)) 
        
        return {'pausality':quantity_punctuation / number_of_setences}


    