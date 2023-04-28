import boto3;

#DynamoDBクライアントを作成
dynamodb = boto3.resource('dynamodb')

#テーブル名を指定
table = dynamodb.Table('seats-test')

def lambda_handler(event, context):
    records = get_records(table)

#スキャンで取得したすべてのアイテムをのうち、seatTypeが5or6以外のレコードをUPDATEする
    for record in records:
        if record['seatType']  in [5, 6]:
            continue
# 更新するフィールドと値を指定
        update_expression= 'Set seatedStatus = :v1, seatedAt = :v2, employeeId = :v3, employeeFamilyName = :v4, employeeGivenName = :v5, company = :v6, phoneNumber = :v7, team = :v8'
        expression_attribute_values = {':v1': False, ':v2': None, ':v3': None, ':v4': None,':v5': None, ':v6': None, ':v7': None, ':v8': None}
# アップデートのリクエストを作成
        update_request = {
        'Key': {'seatId': record['seatId']},
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': expression_attribute_values
        }
# アップデートを実行
        table.update_item(**update_request)

#get_recordsメソッド：scanして、全件取得
#その後itemに詰めて返す
def get_records(table, **kwargs):
    while True:
        response = table.scan(**kwargs)
        for item in response['Items']:
            yield item
        if 'LastEvaluatedKey' not in response:
            break
        kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])