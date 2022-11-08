import stanza
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse,ner' ,download_method = None)

print("import success\n")

def open_file(filename):
    file = open(filename,"r")
    lines = file.readlines()
    dialogues = []
    for line in lines:
        dialogue_in = line.find("\"summary\"") 
        if (dialogue_in!=-1):
            dialogues.append(line.strip()[12:-2])
    return dialogues


from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
new_stop_words = ['file_gif','file_other','\'s', '\'m', 'file_photo', 'u' , 'urgh', 'r' , 'haha' ,
                  'ok', 'eh' , '\'re', 'yeah', 'file_video' ,'oh' , 'xd' , 'yes' , 'bye' , 'yup',
                  'lol' , 'be' , 'hey', 'sure' ,  'yep' , 'know', 'really' , 'sorry', 'that', 'wtf',
                  'get', 'go' , '' , 'yea' , 'alright' 
                 ]
for word in new_stop_words:
    stop_words.add(word)

key_deprel = ['root', 'csubj', 'nsubj','xsubj', 'cop', 'vmod','dobj' ,'iobj', 'pobj']
def get_keyword_from_sentence(sentence):
    keywords = []
    doc = nlp(sentence)
    for sent in doc.sentences:
        entities = sent.entities
        entities_name = [entity.text for entity in entities]


        for word in sent.words:
            try:
                word_lemma = word.lemma.lower()
            except:
                word_lemma = ''
            if(
               (word.deprel in key_deprel  # select word with parsing
                or 
                word_lemma in entities_name # word is an entity
               )

               and word.text.lower() not in stop_words # delete stopword
               and word_lemma not in stop_words

               ):
                # keywords.append(word.text.lower())
                keywords.append(word_lemma)
    return keywords



def get_keyword_from_dialogue(dialogue):
    keywords = []
    for sentence in dialogue:
        # start_pos = sentence.find(":")
        # sentence = sentence[start_pos+2:]
        for word in get_keyword_from_sentence(sentence):
            keywords.append(word)
        clean_repeat_keywords = list(set(keywords))
    return clean_repeat_keywords

def get_keyphrase_from_file(file):
    dialogues = []
    for dialogue in file:
        sentences = dialogue.split(". ")
        dialogues.append(sentences)

    keyphrase = []
    for dialogue in dialogues:
        keyphrase.append(get_keyword_from_dialogue(dialogue))
    return keyphrase

def get_keyphrase(filename):
    file = open_file(filename)
    length = len(file)
    # length = 20
    print("file length = {}".format(length))


    keyphrase = []
    for i in range(0, length, 10):
        output_2_txt(output, get_keyphrase_from_file(file[i:i+10]))
        print("dialogue {} to {} parsed".format(i,i+9))

    return keyphrase

def output_2_txt( output, file):
    for line in file:
        for word in line:
            output.write(word+' ')
        output.write('\n')

output = open("output","w")

get_keyphrase("test.json")
