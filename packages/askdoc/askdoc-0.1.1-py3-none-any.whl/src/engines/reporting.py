import sys
import pytesseract
from textwrap import dedent
from typing import Dict
from loguru import logger
from pdf2image import convert_from_path
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from src.utils import log_time
from src.engines.llm import LLM

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='DEBUG')


def process_image(image):
    return pytesseract.image_to_string(image).strip()

class ReportParser():
    def __init__(self) -> None:
        pass

    @log_time('report_parser')
    def __call__(self, filename: str) -> Dict:
        """
        Processes the report and returns
        a JSON object of all the elements in the report
        """
        image_ocr = {}

        images = convert_from_path(filename)

        for idx, image in enumerate(images):
            logger.info(f'Processing page number {idx} of the PDF')

            text: str = pytesseract.image_to_string(image).strip()
            image_ocr.update({idx: text})

        return image_ocr

    def parse(self, filename: str) -> Dict:
        return self(filename)

    @log_time('clean_ocr')
    def clean_ocr(self, ocr: Dict) -> Dict:
        sys_prompt = {
            'role': 'system',
            'content': dedent("""
            Assume the role of an assistant to a general physician.
            I will send you the OCR data from my medical report.
            You have to extract important details from the report OCR.
                Patient Information:
                Test Conducted:
                Test Measurement:
                Test Normal range:
                Comments:
            Always reply in JSON mode
            """)
        }

        report_cleaner = LLM(model_id='gpt-4-0125-preview', messages=[sys_prompt], keep_history=False)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(partial(report_cleaner, json_mode=True), o) for o in ocr.values()]
            results = [future.result() for future in futures]

        cleaned_ocr = {}
        for idx, o in enumerate(results):
            cleaned_ocr.update({idx: str(o)})

        return cleaned_ocr

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='Filepath of the report')

    args = parser.parse_args()

    parser = ReportParser()
    parsed_report = parser(filename=args.f)
    cleaned_ocr = parser.clean_ocr(parsed_report)

    for k, v in cleaned_ocr.items():
        print(v)
        print('\n')
