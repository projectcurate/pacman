import os
import boto3

s3 = boto3.resource('s3')
fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')  # <-- absolute dir the script is in

def test_put_file():
    scrape_fixture = os.path.join(fixtures_dir, 'dummy_scrape_data.json')
    json_file = open(scrape_fixture, 'rb')
    result = s3.Object('project-curate-test', 'dummy_scrape_data.json').put(Body=json_file)
    print(result)
    assert result['ResponseMetadata']['HTTPStatusCode'] == 200