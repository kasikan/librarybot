import json
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging
import os.path
import sys
import multiprocessing

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    i = 0
    output = open(outp, 'w', encoding='utf-8')
    inp = r"C:\Users\kanka\Downloads\test\ThaiQACorpus-DevelopmentDataset.json"

with open(inp, 'r', encoding='utf-8') as f:
    data = json.load(f)  # Load JSON data
    
    if 'data' in data:  # Check if 'data' key exists in the JSON
        for item in data['data']:  # Iterate over the list of items under 'data'
            if 'question' in item:  # Check if 'question' key exists in the item
                question_text = item['question']  # Retrieve the question text
                answer_text = item['answer']
                output.write(question_text + "\n")
                output.write(answer_text + "\n")
                i += 1
                if i % 10000 == 0:
                    logger.info("Saved " + str(i) + " articles")
            else:
                logger.warning("Skipping item: 'question' key not found")
    else:
        logger.warning("No 'data' key found in JSON")

output.close()
logger.info("Finished Saved " + str(i) + " articles")
