from google.cloud import language_v1
from google.cloud.language_v1 import enums
import os
import csv



"""
Analyzing Sentiment in a String
"""

os.environ['GOOGLE_APPLICATION_CREDENTIALS']="credentials/google.json"

client = language_v1.LanguageServiceClient()

type_ = enums.Document.Type.PLAIN_TEXT

text_content= "A AstraZeneca PLC assinou um acordo exclusivo com a chinesa Shenzhen Kangtai Biological Products para fornecer sua vacina candidata COVID-19 na China continental, informou a gigante farmacêutica britânica.\nPara atender à demanda do mercado na China, Shenzhen Kangtai é obrigada a garantir uma capacidade de produção anual de pelo menos 100 milhões de doses da injeção experimental AZD1222, que a AstraZeneca co-desenvolveu com pesquisadores da Universidade de Oxford, até o final deste ano, e uma capacidade de pelo menos 200 milhões de doses até o final do próximo ano, disse a AstraZeneca em um comunicado no site de mídia social chinês WeChat.\nAs duas empresas também vão explorar a possibilidade de cooperação na vacina candidata em outros mercados, disse a AstraZeneca.\nA AstraZeneca buscará produzir até 2 bilhões de doses da vacina até o fim de 2021. \nO laboratório já possui acordos selados com Estados Unidos (300 milhões de doses), União Europeia (300 milhões de doses), Reino Unido (100 milhões de doses) e Brasil (100 milhões de doses)"

language = "pt"
document = {"content": text_content, "type": type_, "language": language}

# Available values: NONE, UTF8, UTF16, UTF32
encoding_type = enums.EncodingType.UTF8
response = client.analyze_sentiment(document, encoding_type=encoding_type)

# Get overall sentiment of the input document
print(u"Document sentiment score: {}".format(response.document_sentiment.score))
print(
    u"Document sentiment magnitude: {}".format(
        response.document_sentiment.magnitude
    )
)
# Get sentiment for all sentences in the document
for sentence in response.sentences:
    print(u"Sentence text: {}".format(sentence.text.content))
    print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
    print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

#csv_output.writerow(response.document_sentiment.score, response.document_sentiment.magnitude, response.sentences.text.content, response.sentences.sentiment.score, response.sentences.magnitude)

    




def analyze_entities(text_content):
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']="credentials/google.json"

    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "pt"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))



from google.cloud import language_v1

def sample_analyze_syntax(text_content):
    """
    Analyzing Syntax in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'This is a short sentence.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_syntax(request = {'document': document, 'encoding_type': encoding_type})
    # Loop through tokens returned from the API
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        print(u"Token text: {}".format(text.content))
        print(
            u"Location of this token in overall document: {}".format(text.begin_offset)
        )
        # Get the part of speech information for this token.
        # Parts of spech are as defined in:
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        part_of_speech = token.part_of_speech
        # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
        print(
            u"Part of Speech tag: {}".format(
                language_v1.PartOfSpeech.Tag(part_of_speech.tag).name
            )
        )
        # Get the voice, e.g. ACTIVE or PASSIVE
        print(u"Voice: {}".format(language_v1.PartOfSpeech.Voice(part_of_speech.voice).name))
        # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
        print(u"Tense: {}".format(language_v1.PartOfSpeech.Tense(part_of_speech.tense).name))
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
            u"Label: {}".format(language_v1.DependencyEdge.Label(dependency_edge.label).name)
        )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))