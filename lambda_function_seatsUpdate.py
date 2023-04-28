import boto3;

#DynamoDB�N���C�A���g���쐬
dynamodb = boto3.resource('dynamodb')

#�e�[�u�������w��
table = dynamodb.Table('seats-test')

def lambda_handler(event, context):
    records = get_records(table)

#�X�L�����Ŏ擾�������ׂẴA�C�e�����̂����AseatType��5or6�ȊO�̃��R�[�h��UPDATE����
    for record in records:
        if record['seatType']  in [5, 6]:
            continue
# �X�V����t�B�[���h�ƒl���w��
        update_expression= 'Set seatedStatus = :v1, seatedAt = :v2, employeeId = :v3, employeeFamilyName = :v4, employeeGivenName = :v5, company = :v6, phoneNumber = :v7, team = :v8'
        expression_attribute_values = {':v1': False, ':v2': None, ':v3': None, ':v4': None,':v5': None, ':v6': None, ':v7': None, ':v8': None}
# �A�b�v�f�[�g�̃��N�G�X�g���쐬
        update_request = {
        'Key': {'seatId': record['seatId']},
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': expression_attribute_values
        }
# �A�b�v�f�[�g�����s
        table.update_item(**update_request)

#get_records���\�b�h�Fscan���āA�S���擾
#���̌�item�ɋl�߂ĕԂ�
def get_records(table, **kwargs):
    while True:
        response = table.scan(**kwargs)
        for item in response['Items']:
            yield item
        if 'LastEvaluatedKey' not in response:
            break
        kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])