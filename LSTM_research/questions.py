import spacy
from gensim.models import Word2Vec
from collections import Counter
import string
import random

# Load the spaCy model outside of the function to avoid reloading it multiple times
nlp = spacy.load("en_core_web_sm")

def read_and_process_file_for_word2vec(file_path):
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:  # Process the file line by line to manage memory usage
            doc = nlp(line.lower())
            for sent in doc.sents:
                sentences.append([token.text for token in sent if not token.is_stop and not token.is_punct])
    return sentences

# Splitting the file reading and Word2Vec training into two steps for clarity
word2vec_dataset = read_and_process_file_for_word2vec("nflx.txt")
word2vec = Word2Vec(word2vec_dataset, min_count=1, workers=4)  # Using multiple workers for faster training

def calculate_word_weights(paragraph):
    doc = nlp(paragraph.lower())
    weights = Counter()
    for i, token in enumerate(doc):
        if not token.is_stop and token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB'] and token.text in word2vec.wv:
            neighbors = [doc[j].text for j in range(max(0, i - 1), min(len(doc), i + 2)) if j != i]
            weights[token.text] += sum(word2vec.wv.similarity(token.text, neighbor) 
                                       for neighbor in neighbors if neighbor in word2vec.wv)
    return weights

def generate_questions(paragraph):
    questions = []
    word_weights = calculate_word_weights(paragraph)
    top_word = word_weights.most_common(1)[0][0] if word_weights else None

    if top_word:
        questions.append(f"What is the significance of '{top_word}' in: '{paragraph}'?\n")
    
    nouns = extract_nouns(paragraph)
    for noun in nouns:
        questions.append(f"How does {noun} impact the analysis in the context: '{paragraph}'?\n")

    key_sentence = find_key_sentence(paragraph)
    if key_sentence:
        questions.append(f"What are the implications of the statement: '{key_sentence}'?\n")

    return questions

def extract_nouns(paragraph):
    doc = nlp(paragraph)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_punct]

def find_key_sentence(paragraph):
    doc = nlp(paragraph)
    sentences = [sent.text for sent in doc.sents]
    return random.choice(sentences) if sentences else None

def read_paragraphs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split('\n\n')

def write_to_file(questions, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for question in questions:
            file.write(question)

def main(input_file, output_file1, output_file2):
    paragraphs = read_paragraphs(input_file)
    all_questions = []
    word2vec_questions = []

    for paragraph in paragraphs:
        questions = generate_questions(paragraph)
        all_questions.extend(questions)
        
        word_weights = calculate_word_weights(paragraph)
        top_word = word_weights.most_common(1)[0][0] if word_weights else None
        if top_word:
            word2vec_questions.append(f"What is the significance of '{top_word}' in '{paragraph}'?\n")

    write_to_file(all_questions, output_file1)
    write_to_file(word2vec_questions, output_file2)

input_file = 'nflx.txt'
output_file1 = 'OPnflx1.txt'
output_file2 = 'OPnflx2.txt'

main(input_file, output_file1, output_file2)
