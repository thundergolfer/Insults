import boto3

client = boto3.client(
    service_name = 'mturk',
    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
)

# Uncomment the below to connect to the live marketplace
# Region is always us-east-1
# client = boto3.client(service_name = 'mturk', region_name='us-east-1')

# Test that you can connect to the API by checking your account balance
user_balance = client.get_account_balance()

# In Sandbox this always returns $10,000
print "Your account balance is {}".format(user_balance['AvailableBalance'])

task_file = open("task_template.xml", "r")
task = task_file.read()

# Create a qualification with Locale In('US', 'CA') requirement attached
localRequirements = [{
    'QualificationTypeId': '00000000000000000071',
    'Comparator': 'In',
    'LocaleValues': [{
        'Country': 'US'
    }, {
        'Country': 'CA'
    }],
    'RequiredToPreview': True
}]

# Create the HIT
response = client.create_hit(
    MaxAssignments = 10,
    LifetimeInSeconds = 600,
    AssignmentDurationInSeconds = 600,
    Reward ='0.20',
    Title = 'Answer a simple question',
    Keywords = 'question, answer, research',
    Description = 'Answer a simple question',
    Question = task,
    QualificationRequirements = localRequirements
)

# The response included several fields that will be helpful later
hit_type_id = response['HIT']['HITTypeId']
hit_id = response['HIT']['HITId']
print "Your HIT has been created. You can see it at this link:"
print "https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id)
print "Your HIT ID is: {}".format(hit_id)
