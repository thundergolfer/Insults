import boto3

client = boto3.client(
    service_name='mturk',
    endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com'
)

# Uncomment the below to connect to the live marketplace
# Region is always us-east-1
# client = boto3.client(service_name = 'mturk', region_name='us-east-1')

# This HIT id should be the HIT you just created - see the CreateHITSample.py file for generating a HIT
hit_id = 'YOUR_HIT_ID'

hit = client.get_hit(HITId=hit_id)
print 'Hit {} status: {}'.format(hit_id, hit['HIT']['HITStatus'])
response = client.list_assignments_for_hit(
    HITId=hit_id,
    AssignmentStatuses=['Submitted'],
    MaxResults=10
)

assignments = response['Assignments']
print 'The number of submitted assignments is {}'.format(len(assignments))
for assignment in assignments:
    WorkerId = assignment['WorkerId']
    assignmentId = assignment['AssignmentId']
    answer = assignment['Answer']
    print 'The Worker with ID {} submitted assignment {} and gave the answer {}'.format(WorkerId,assignmentId, answer)

    # Approve the Assignment
    print 'Approve Assignment {}'.format(assignmentId)
    client.approve_assignment(
        AssignmentId=assignmentId,
        RequesterFeedback='good',
        OverrideRejection=False
    )
