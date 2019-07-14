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
    with open("data.json", "r") as f:
        data = json.loads(f.read())
    # summary
    print("summary")
    summarizer = Summarizer()
    # generate questions
    print("generate questions")
    question_generator = QuestionGenerator()
    for doc in data["data"]:
        try:
            res = {}
            res["topic"] = doc["topic"]
            res["thumbnail"] = doc["thumbnail"]
            res["type"] = "text"
            res["title"] = doc["title"]
            res["level"] = "medium"
            res["content"] = doc["content"]
            res["audio"] = ""
            res["publisher"] = "BBC"
            res["source_url"] = "https://www.bbc.co.uk/"
            res["questions"] = []
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
            with open("temp.txt", "a") as f:
                f.write(doc["content"] + "\n")
                f.write(str(questions))
                f.write("\n\n")

            for _type, q in questions:
                if q == None:
                    continue
                content = q[0]
                content = content.strip()
                content = (content[0]).upper() + content[1:]
                if _type == "QA":
                    question = {
                        "content": content,
                        "answer" : q[1],
                        "options": [],
                        "type"   : "fill"
                    }
                    res["questions"].append(question)
                elif _type == "FF":
                    question = {
                        "content": content,
                        "answer" : q[1],
                        "options": [],
                        "type"   : "fill"
                    }
                    res["questions"].append(question)
                elif _type == "FF4":
                    question = {
                        "content": content,
                        "answer" : q[1],
                        "options": [],
                        "type"   : "choice"
                    }
                    for choice in q[2]:
                        question["options"].append(choice)
                    res["questions"].append(question)
            save_article(res)
        except:
            continue




if __name__ == "__main__":
    main()