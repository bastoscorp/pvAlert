# pvAlert

Need to have aws cli installed with iam user with at least the following privileges:

`
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sns:Publish",
                "sns:GetTopicAttributes"
            ],
            "Resource": "*"
        }
    ]
}
`