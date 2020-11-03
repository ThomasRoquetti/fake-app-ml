from userRequestProcessor import UserProcessor
from fakeUserPredict import UserPredict
from apiCall import ApiCall
import json

apiCall = ApiCall()
userProcessor = UserProcessor()
userPredict = UserPredict()

class StartProcess ():


    def dataProcess (self, userText):
        print("Starting data processing")

        googleApi = apiCall.googleApi(text_content=userText['text'])

        client = googleApi['client']
        document = googleApi['document']
        encoding = googleApi['encoding_type']

        sentiment = userProcessor.sentiment(client,document,encoding)
        entities = userProcessor.entities(client,document,encoding)
        syntax = userProcessor.syntax(client,document,encoding)
        text_lens = userProcessor.text_lens(document)
        pausality = userProcessor.pausality_calc(document)


        userProcessed ={
            'number_of_tokens': text_lens['number_of_tokens'],
            'number_of_words_in_uppercase': text_lens['number_of_words_in_uppercase'],
            'number_of_verbs': syntax['number_of_verbs'],
            'number_of_subj_imp_verbs': syntax['number_of_subj_imp_verbs'],    
            'number_of_nouns': syntax['number_of_nouns'],
            'number_of_adjectives': syntax['number_of_adjectives'],
            'number_of_adverbs': syntax['number_of_adverbs'],
            'number_of_modal_verbs': syntax['number_of_modal_verbs'],    
            'number_of_singular_fs_pron': syntax['number_of_singular_fs_pron'],
            'number_of_plural_f_pron': syntax['number_of_plural_f_pron'],    
            'number_of_pronouns': syntax['number_of_pronouns'],
            'pausality': pausality['pausality'],
            'number_of_chars': text_lens['number_of_chars'],
            'average_sent_len': text_lens['average_sent_len'],
            'average_word_len': text_lens['average_word_len'],
            "document_score": sentiment['document_score'], 
            "document_magnitude": sentiment['document_magnitude'],
            'EVENT': entities['EVENT'],
            'LOCATION': entities['LOCATION'],
            'ORGANIZATION': entities['ORGANIZATION'],
            'PERSON': entities['PERSON']
        }

        valuesToClassify = list(userProcessed.values())
        classifiedValue = userPredict.predict(valuesToClassify)
        self.format_response(classifiedValue)
        
        return self.format_response(classifiedValue)



    def format_response(self, classifiedValue):

        label = classifiedValue[0]
        prob_true = float(classifiedValue[4]) * 100
        prob_false = float(classifiedValue[5]) * 100

        response = {
            "predicted_label": label,
            "probabilidade": {
                "TRUE": round(prob_true, 2),
                "FAKE": round(prob_false, 2)
            }
        }
        return response

if __name__ == '__main__':
    startProcess = StartProcess()
    print("Starting process")


    userText = {'text': 'Saiba o que Marcela e Alexandre de Moraes fizeram e pode destruir a reputação do presidente. Marcela Temer e o ministro Alexandre de Moraes possuem um recente passado em comum, este fato que pode vir à tona nos próximos dias poderá por fim aos planos de Alexandre de Moraes de chegar ao STF, e de Michel Temer continuar presidente. O juiz Hilmar Castelo Branco Raposo Filho, da 21a Vara Cível do Tribunal de Justiça do Distrito Federal, proibiu o jornal Folha de S.Paulo e outros veículos da imprensa de reproduzir informações sobre o caso do hacker que chantageou o casal Temer após clonar o celular da primeira-dama, Marcela. A ordem foi dada atendendo a pedido de advogados de Marcela, depois que a Folha publicou nesta sexta-feira 10 a mensagem enviada pelo hacker pedindo R$ 300 mil para não divulgar um áudio que, segundo ele, colocaria o nome de Michel Temer na lama. Claudio Julio Tognolli é jornalista há 35 anos e já passou por Veja, Jornal da Tarde, Caros Amigos, Joyce Pascowitch, Rolling Stone, Galileu, Consultor Jurídico, rádios CBN, Eldorado e Jovem Pan e Folha de S. Paulo. Em sua decisão, publicada às 18h56 desta sexta, o juiz argumenta que a inviolabilidade da intimidade de Marcela tem resguardo legal claro. A medida foi concedida em caráter de urgência. O caso aconteceu em abril de 2016. No áudio, segundo relatório da Polícia Federal sobre a investigação, Marcela falava com o irmão Karlo Augusto Araújo sobre um marqueteiro que faz a parte baixo nível do marido. Quem cuidou do caso, na época, foi o então secretário de Segurança Pública de São Paulo, Alexandre de Moraes. Ele montou uma equipe e em 40 dias, sem alarde, prendeu Silvonei José de Jesus Souza, condenado em um prazo de apenas seis meses  considerado célere para o Judiciário brasileiro  a uma pena de cinco anos e dez meses de prisão pelos crimes de estelionato e extorsão. No processo, que teve seu sigilo levantado agora, o hacker dizia ter fotos, contas de e-mail e também um áudio que arruinaria a reputação de Temer, segundo reportagem da Folha de S.Paulo. A mensagem de voz, que teria sido obtida pelo hacker após clonagem do celular de Marcela, foi enviada por ela ao irmão, Karlo Augusto Araújo. Pois bem como achei que esse video [na verdade, áudio] joga o nome de vosso marido [Temer] na lama. Quando você disse q ele tem um marqueteiro q faz a parte baixo nível pensei em ganhar algum com isso!!!!, escreveu o hacker a Marcela, que pediu R$ 300 mil para não divulgar o arquivo. Moraes, então secretário de Segurança Pública de São Paulo, comandou o caso pessoalmente e, sem alarde, prendeu o hacker em 40 dias. Foi criada na Polícia Civil uma força-tarefa com cinco delegados, 25 investigadores e três peritos para investigar o caso. Ao prender o hacker, Moraes se tornou credor de quem agora o indicou ao STF, a despeito de todas as suas polêmicas. A mais recente foi a sabatina informal com senadores num barco-motel.'}

    response = startProcess.dataProcess(userText)