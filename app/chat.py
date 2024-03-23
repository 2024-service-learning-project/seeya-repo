import openai
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
import dotenv
import requests
from bs4 import BeautifulSoup


dotenv.load_dotenv(override=True)
open_ai_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=open_ai_key)

# [1] GPT-4-vision : Screenshot:filepath -> Website:string
class GetDesktopURL():
    def __init__(self):
        pass 
    def _get_query(self, image_url: str):
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system",
                "content": "너는 이미지에서 상품명을 알려주는 인공지능이야. 제품의 이름을 부가 설명 없이 string으로 말해줘. 만약 상품명을 알 수 없다면 손님에게 '약간만 아래로 스크롤해주세요.'라고 말해줘."},
                {
                "role": "user",
                "content": [
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                    },
                ],
                }
            ],
            max_tokens=1500,
            )
        
        product_name=response.choices[0].message.content
        return product_name
    
    def get_url(self, image_url: str):
        query=self._get_query(image_url)
        base_url = f"https://www.musinsa.com/search/musinsa/integration?q={query}"

        response = requests.get(base_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        li_inner_divs = soup.find_all('div', class_='li_inner')
        links = [div.find('a')['href'] for div in li_inner_divs if div.find('a')]

        return links[0]




# [3] GPT-4 : Crawled_text:string -> Detail_1:string
def get_detail_1() -> str:
    with open("../texts/test1.txt", "r", encoding="utf-8") as text_file:
        product_texts = text_file.read()
        
    user_prompt = "제공된 텍스트로부터 [상품에 대한 한줄 요약, 상품의 가격, 상품의 브랜드명, 어떤 성별을 대상으로 한 상품인지, 상품의 상세 카테고리 분류]를 dictionary 형태로 알려주세요. 답변에는 dictionary만을 포함하세요"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": product_texts},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


# [4] GPT-4-vision : Image:image -> Detail_2:string
def get_detail_2(img_path) -> str:
    image_folder_path = img_path
    # 폴더 내의 모든 파일 및 디렉토리 목록을 가져옵니다
    files = os.listdir(image_folder_path)
    encoded_images = []
    # 모든 파일 순회
    for file in files:
        # 파일 경로를 생성
        img_path = os.path.join(image_folder_path, file)
        with open(img_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            encoded_images.append(base64_image)

    user_prompt = "제공된 이미지로부터 [상품의 재질, 촉감, 착용하기 좋은 계절]을 dictionary 형태로 알려주세요. 답변에는 dictionary 만을 포함하세요"

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                    }
                ]
            },
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content



# [5] GPT-4 : Question:string -> Answer:string 
def response(question:str) -> str:
    with open("../details/example.txt", "r", encoding="utf-8") as text_file:
        product_details = text_file.read()

    system_prompt = f"""
        당신은 의류에 대해 자세히 설명하는 친절한 직원입니다. 
        사용자가 의류에 대한 질문을 하게 되면, 상품 페이지의 정보와 옷의 상세 묘사 정보를 참고하여 친절하게 한글로 답변해주세요.
        제품 정보 : {product_details}\n
        """
    user_prompt = f"질문 : {question}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

