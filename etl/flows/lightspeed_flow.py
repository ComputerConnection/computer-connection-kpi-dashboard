from prefect import flow, task
import os

@task
def sync_sales():
    use_mock = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'
    if use_mock:
        print('Using mock Lightspeed data')
    else:
        print('Would sync from Lightspeed API')

@flow
def lightspeed_flow():
    sync_sales()

if __name__ == '__main__':
    lightspeed_flow()
