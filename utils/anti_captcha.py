import requests
import time

API_URL = 'https://api.2captcha.com'

def create_task(site_key, url, captcha_type='RecaptchaV3TaskProxyless', min_score=0.7, api_key='7f28bd13a451bd3a2b77ca5f30bf49a7'):
    """Создание задачи для решения капчи."""
    task = {
        'clientKey': api_key,
        'task': {
            'type': captcha_type,
            'websiteURL': url,
            'websiteKey': site_key,
            "isInvisible": False
        }
    }

    if captcha_type == 'RecaptchaV3TaskProxyless' and min_score is not None:
        task['task']['minScore'] = min_score

    response = requests.post(f'{API_URL}/createTask', json=task)
    return response.json()


def get_task_result(task_id, api_key='7f28bd13a451bd3a2b77ca5f30bf49a7'):
    """Получение результата решения капчи."""
    result_request = {
        'clientKey': api_key,
        'taskId': task_id
    }

    while True:
        response = requests.post(f'{API_URL}/getTaskResult', json=result_request)
        result = response.json()
        if result['status'] == 'ready':
            return result['solution']['gRecaptchaResponse']
        elif result['status'] == 'processing':
            time.sleep(5)
        else:
            raise Exception(f"Error: {result['errorDescription']}")


def main(site_key, url, captcha_type='RecaptchaV3TaskProxyless', min_score=0.7):
    try:
        task_response = create_task(site_key, url, captcha_type, min_score)

        if task_response['errorId'] != 0:
            print(f"Error creating task: {task_response['errorDescription']}")
            return

        task_id = task_response['taskId']

        captcha_response = get_task_result(task_id)

        print("Captcha solved successfully! Response:", captcha_response)
        return captcha_response

    except Exception as e:
        print(f"An error occurred: {e}")