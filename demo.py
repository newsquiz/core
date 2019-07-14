from generator.generator import QuestionGenerator
from aqg.sentence_selector import SentenceSelector
from tuan_summary.summarizer import Summarizer
from utils import DocumentGraph
from db_utils import save_article
import subprocess
import random
import json
import pdb

sample_input = {
    "topic": "society",
    "thumbnail": "data/xb.jpg",
    "type": "audio",
    "title": "How to spend money after winning hackathon challenge?",
    "level": "medium",
    "content": "<div></div>",
    "audio": "data/die.wav",
    "publisher":"bbc",
    "source_url": "https://www.bbc.co.uk/",
    "questions": [{
        "content": "Who is president of the USA",
        "options": [
            "Bui Manh Thang",
            "Luong Tung Dung",
            "Phan Ngoc Lan",
            "Bui Duy Tuan"
        ],
        "answer": "Bui Manh Thang",
        "type": "choice"
    }]
}

def main():
    # read full doc
    print("read json data")
    with open("voa_crawler/data.json", "r") as f:
        data = json.loads(f.read())
    # summary
    print("summary")
    summarizer = Summarizer()
    # generate questions
    print("generate questions")
    question_generator = QuestionGenerator()
    for doc in data:
        questions = []
        sentences = summarizer.predict(doc["content"])
        paragraph = " ".join(sentences)
        docgraph = DocumentGraph(paragraph)
        sentences = question_generator.sen_tokenizer.transform(paragraph)
        for i in range(len(sentences)):
            for e in docgraph.get_sentence_entities(i):
                if (e.refer == None):
                    continue
                while (e.refer.refer != None):
                    e.refer = e.refer.refer
                sentences[i] = sentences[i].replace(e.text, e.refer.text, 1)
            # gen sentences
            temp_questions = question_generator.transform(sentences[i])
            if len(temp_questions) > 0:
                questions.append(random.choice(temp_questions))
            print(questions)
        




if __name__ == "__main__":
    main()