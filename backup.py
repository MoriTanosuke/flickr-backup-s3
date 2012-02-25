#!/usr/bin/python
import boto
import boto.ec2
import paramiko
import time

# default AMI, ubuntu
ami = 'ami-02f2c176'
# we don't need much processing power
size = 't1.micro'
security = 'Secure'
keys = 'amazon'
keyfile = '/home/DATA/Backup/amazon-cloud/amazon'

print "Connecting to EC2..."
conn = boto.connect_ec2()
security_group = conn.get_all_security_groups(groupnames=security)
print "Starting instance..."
reservation = conn.run_instances(ami, instance_type=size, key_name=keys, security_groups=security_group)
instance = reservation.instances[0]
while instance.state != 'running':
	print instance.state + " = still waiting..."
	time.sleep(10)
	instance.update()
print "Executing command on instance:"
host = instance.public_dns_name

ssh = paramiko.SSHClient()
ssh.load_host_keys(filename=keyfile)
ssh.connect(host)
# TODO mount s3 inside the EC2 instance
# TODO install flickrtouchr.py
# TODO run flickrtouchr.py and backup images to s3 mount
# TODO umount s3
ssh.close()

print "Stopping instance..."
reservation.stop()
print "All done."

