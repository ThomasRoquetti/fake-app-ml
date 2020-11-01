""""
number of tokens -> done,
number of words without punctuation,
number of types,
number of words in upper case,
number of verbs,
number of subjuntive and imperative verbs,
number of nouns,
number of adjectives,
number of adverbs,
number of modal verbs,
number of singular first and second personal pronouns,
number of plural first personal pronouns,
number of pronouns,
pausality,
number of chracteres -> need to remove punctuation,
average sentence length -> got number of sentences,
average word length,
percentage of news with speeling errors,
document_score -> done,
document_magnitude -> done,
EVENT -> done,
LOCATION -> done,
ORGANIZATION -> done,
PERSON -> done
"""
from google.protobuf.json_format import MessageToDict
from google.cloud.language_v1 import enums
from apiCall import ApiCall
import json
import re

#set api
apiCall = ApiCall()

with open ('userRe/userRequest.json','r',encoding="utf8") as userRequest:
    text = json.load(userRequest)
    text = text['text']

googleApi = apiCall.googleApi(text_content=text)

client = googleApi['client']
document = googleApi['document']
encoding = googleApi['encoding_type']


#analyze sentiment
def sentiment (client, document, encoding):
    response = client.analyze_sentiment(document, encoding_type=encoding)
    return {"document_score":response.document_sentiment.score, "document_magnitude":response.document_sentiment.magnitude}


#analyze entities
def entities (client, document, encoding):
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

def syntax (client, document, encoding):
    document['content'] = re.sub('\W+',' ', document['content'])
    response = client.analyze_syntax(document, encoding_type=encoding)
    #len of things
    number_of_tokens = len(response.tokens)
    number_of_sentences = len(response.sentences)
    number_of_characters = len(document['content'])

    # Loop through tokens returned from the API
    with open ('userRequest.json','w',encoding="utf8") as userRequest:
        text = MessageToDict(response)
        json.dump(text, userRequest, ensure_ascii=False)

    for sentence in response.sentences:
        cleanString = re.sub('\W+',' ', sentence.text.content)
        print(cleanString)
        input()
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        print(u"Token text: {}".format(text.content))
        # Get the part of speech information for this token.
        # Parts of spech are as defined in:
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        part_of_speech = token.part_of_speech
        # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
        print(
            u"Part of Speech tag: {}".format(
                enums.PartOfSpeech.Tag(part_of_speech.tag).name
            )
        )
        # Get the voice, e.g. ACTIVE or PASSIVE
        print(u"Voice: {}".format(enums.PartOfSpeech.Voice(part_of_speech.voice).name))
        # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
        print(u"Tense: {}".format(enums.PartOfSpeech.Tense(part_of_speech.tense).name))
        # See API reference for additional Part of Speech information available
        # Get the lemma of the token. Wikipedia lemma description
        # https://en.wikipedia.org/wiki/Lemma_(morphology)
        print(u"Lemma: {}".format(token.lemma))
        # Get the dependency tree parse information for this token.
        # For more information on dependency labels:
        # http://www.aclweb.org/anthology/P13-2017
        dependency_edge = token.dependency_edge
        print(u"Head token index: {}".format(dependency_edge.head_token_index))
        print(
            u"Label: {}".format(enums.DependencyEdge.Label(dependency_edge.label).name)
        )
    print("number_of_tokens: "+str(number_of_tokens))
    print("number_of_sentences: "+str(number_of_sentences))
    print("number_of_characters: "+str(number_of_characters))
    return 0 #para de da erro pora


#sentiment = sentiment(client,document,encoding)  ---ta comentado pra n ficar puxando da api, tem que descomentar dps
#entities = entities(client,document,encoding)
syntax = syntax(client,document,encoding)
