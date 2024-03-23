from flask import Flask, request, jsonify, send_file
import boto3
from botocore.exceptions import ClientError
from io import BytesIO

from chat import GetDesktopURL, get_detail_1, get_detail_2, response
from crawler import get_info
from audio import get_mp3_from_txt


app = Flask(__name__)

polly_client = boto3.client('polly')

@app.route('/setup', methods=['POST'])
def setup():
    ###
    screenshot_url = "https://seeya-bucket.s3.ap-northeast-2.amazonaws.com/1301+%EB%AC%B4%EC%A7%80+%EB%B0%98%ED%8C%94%ED%8B%B0/IMG_619F71BCF261-1.jpeg"
    #1. GPT-4-vision (스크린 샷 -> Website)
    web_url = GetDesktopURL().get_url(screenshot_url)

    #2. Crawling (Website -> 제품 텍스트, 제품 사진)
    review = get_info(web_url) #delivery, price, size

    #3. GPT-4 vision (제품 사진 -> 의류 상세 정보)
    info_2 = get_detail_2('../crawled_images')

    #4. GPT-4 (의류 상세 정보 + 제품 텍스트 -> 의류 상세 정보)
    #info_1 = get_detail_1()
    #info = info_1 + info_2 

    # 파일로 저장할 경로
    file_path = "../details/example.txt"

    # 파일 열기 및 문자열 쓰기
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(info_2)

    pass

@app.route('/query', methods=['POST'])
def query():
    ###
    #1. GPT-4 (질문 텍스트 + 의류 상세 정보 -> 답변)
    question = "이 제품의 색상은 뭐야?"
    answer = response(question)
    #2. TTS (답변 -> 음성 답변)
    get_mp3_from_txt(answer)
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)