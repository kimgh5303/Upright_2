import sys
import User
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

#  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
def alarm(text):
    # API 키와 API 시크릿을 파일에서 직접 읽어옴
    api_key = None
    api_secret = None
    from_number = None
    file_path = 'api_pwd.txt'  # 상대 경로로 파일 위치를 지정

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("api_key"):
                    api_key = line.split("=")[1].strip()
                elif line.startswith("api_secret"):
                    api_secret = line.split("=")[1].strip()
                elif line.startswith("from_number"):
                    from_number = line.split("=")[1].strip()
    except Exception as e:
        print(f"Failed to read API credentials: {str(e)}")
        return

    if api_key is not None and api_secret is not None:
        # 4 params(to, from, type, text)는 필수입니다.
        params = dict()
        params['type'] = 'sms'  # 메시지 유형 (sms, lms, mms, ata)
        params['to'] = User.user.phone  # 수신자 번호, 예: '01000000000,01000000001'
        params['from'] = from_number    # 발신자 번호
        params['text'] = text  # 메시지 내용

        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
    else:
        print("API credentials not available")