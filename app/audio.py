import boto3

# [6] Generating mp3 file : Answer [text] -> Audio [mp3]
def get_mp3_from_txt(text):
    polly_client = boto3.client('polly', region_name='ap-northeast-2')
    ssml_text = f"""
    <speak>
        <prosody rate="80%">{text}</prosody>
    </speak>
    """

    response = polly_client.synthesize_speech(VoiceId='Seoyeon',
                                            OutputFormat='mp3',
                                            TextType='ssml',
                                            Text=ssml_text)

    # 음성 파일 저장
    with open('../audios/example.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())