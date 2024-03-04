import sys
import json
import gradio as gr
from loguru import logger
from .generators import verify, medical, summarizer
from .engines import ReportParser, UserMemory
from .utils import encode_image

memory = UserMemory()

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

def verify(message, history, file):
    """
    Verifies if the user message is a valid message or not
    """
    #ToDo: Implementation
    pass


def respond(message, history, file):
    logger.debug(f'History: {history}')

    image = None

    # If a file is provided, process the file for further QnA
    if file:
        logger.info(f'Parsing the data in the file" {file}')
        try:
            if file.split('.')[-1] in ['jpg', 'jpeg', 'png']:
                image = encode_image(image_path=file)

            elif file.split('.')[-1] == 'pdf':
                parser = ReportParser()
                parsed_report = parser.parse(file)
                cleaned_report = parser.clean_ocr(parsed_report)

                # Add to memory
                memory.add_memory(
                    documents=list(cleaned_report.values()),
                    metadata=[f'Medical document, page: {k}' for k in cleaned_report.keys()]
                )

            else:
                raise NotImplementedError(f'File of type {file.split(".")[-1]} is not supported. Please upload .jpg/.pdf/.jpeg/.png')

        except Exception as err:
            raise IOError(f'Not able to parse the file: {err}')

    if len(history) % 100 == 0:
        logger.info('Summarizing the past conversation')
        with open('./history.jsonl', 'a') as fp:
            for usr, ast in history:
                fp.write(json.dumps({
                    'user': usr,
                    'assistant': ast
                }))
                fp.write('\n')

        to_remove = []
        for msg in medical.messages:
            if msg['role'] == 'system':
                continue

            if 'summary of past conversation' in msg['content'][0]['text'].lower():
                continue

            summarizer._add_msg(msg['content'][0]['text'], role=msg['role'])
            to_remove.append(msg)

        for msg in to_remove:
            medical.messages.remove(msg)

        summary = summarizer('Summarize')
        logger.info(f'Summary of the conversation: {summary}')
        memory.add_memory(
            documents=[summary],
            metadata=['Summary of the previous conversation']
        )

        medical._add_assistant_msg(summary)
        logger.info(f'Messages: {medical.messages}')

    # Query match message to the medical report, extract and then send to medical
    relevant_msg = memory.search(message)
    logger.info(f'Found relevant messages: {relevant_msg}')

    if relevant_msg:
        return medical(f'Context: {relevant_msg}\nQuery: {message}', image=image)

    return medical(message, image=image)

def main():
    demo = gr.ChatInterface(
        respond,
        chatbot=gr.Chatbot(value=[(None, "Welcome 👋. I am your personal doctor. You can ask me anything related to your medical concerns")]),
        additional_inputs=gr.File(label="Upload a medical report")
    )
    demo.launch()

if __name__ == "__main__":
    main()
