# Benchmark Setup
The following will outline the steps to follow in order to setup the benchmark project.

1. Create an `.ssh` directory with a SSH keypair to gain access to the EC2 instances.
```bash
mkdir -m 700 .ssh
ssh-keygen -t rsa -b 4096 -f .ssh/id_rsa -N ''
```

1. Create a new IAM user with programmatic access and attach the SSH keypair. This process with generate a set of credentials that will allow you to access AWS services via the CLI.

2. Add them to a policy group that has access to AWS EC2 instances (they will need full access).

3. Create an `.aws` directory to store the configuration files.
```bash
mkdir -m 700 .aws
```

4. Copy the contents of the credentials into the `.aws` directory.
```bash
echo "[default]" > .aws/credentials
echo "aws_access_key_id = <your access key>" >> .aws/credentials
echo "aws_secret_access_key = <your secret key>" >> .aws/credentials

echo "[default]" > .aws/config
echo "region = <your region>" >> .aws/config
echo "output = json" >> .aws/config
```
