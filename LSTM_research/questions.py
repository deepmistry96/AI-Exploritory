import spacy
from gensim.models import Word2Vec
from collections import Counter
import string
import random

nlp = spacy.load("en_core_web_sm")

def read_and_process_file_for_word2vec(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    doc = nlp(text.lower())
    sentences = [sent.text.split() for sent in doc.sents]
    return sentences
word2vec_dataset = read_and_process_file_for_word2vec("nflx.txt")

word2vec = Word2Vec(word2vec_dataset, min_count=1)

def calculate_word_weights(paragraph):
    doc = nlp(paragraph.lower())
    weights = Counter()
    for i, token in enumerate(doc):
        if not token.is_stop and token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB'] and token.text in word2vec.wv:
            neighbors = [doc[i - 1].text, doc[i + 1].text] if 0 < i < len(doc) - 1 else []
            weights[token.text] += sum(word2vec.wv.similarity(token.text, neighbor) 
                                       for neighbor in neighbors if neighbor in word2vec.wv)
    return weights


def generate_questions(paragraph, nlp):
    questions = []
    word_weights = calculate_word_weights(paragraph)
    top_word = word_weights.most_common(1)[0][0] if word_weights else None

    if top_word:
        questions.append(f"What is the significance of '{top_word}' in: '{paragraph}'?\n")
    
    nouns = extract_nouns(paragraph, nlp)
    for noun in nouns:
        questions.append(f"How does {noun} impact the analysis in the context: '{paragraph}'?\n")

    key_sentence = find_key_sentence(paragraph, nlp)
    if key_sentence:
        questions.append(f"What are the implications of the statement: '{key_sentence}'?\n")

    return questions

def extract_nouns(paragraph, nlp):
    doc = nlp(paragraph)
    nouns = set()
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] and token.text not in string.punctuation:
            nouns.add(token.text)
    return list(nouns)

def find_key_sentence(paragraph, nlp):
    doc = nlp(paragraph)
    sentences = [sent for sent in doc.sents]
    return random.choice(sentences).text if sentences else None

def read_paragraphs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split('\n\n')

def write_to_file(questions, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for question in questions:
            file.write(question + '\n')

def main(input_file, output_file1, output_file2):
    paragraphs = read_paragraphs(input_file)
    all_questions = []
    word2vec_questions = []

    for paragraph in paragraphs:
        questions = generate_questions(paragraph, nlp)
        all_questions.extend(questions)
        
        word_weights = calculate_word_weights(paragraph)
        top_word = word_weights.most_common(1)[0][0] if word_weights else None
        if top_word:
            word2vec_questions.append(f"What is the significance of '{top_word}' in '{paragraph}'?\n")

    write_to_file(all_questions, output_file1)
    write_to_file(word2vec_questions, output_file2)


input_file = 'nflx.txt'
output_file1 = 'output_general_questions.txt'
output_file2 = 'output_word2vec_questions.txt'

main(input_file, output_file1, output_file2)

