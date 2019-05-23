#!/bin/bash

#usage: ./find_and_command_instances.sh TYPE ENVIRONMENT VERSION REGION COMMAND

TYPE=$1
ENVIRONMENT=$2
VERSION=$3
REGION=$4
COMMAND=$5

export AWS_DEFAULT_REGION="${REGION}"

#find instances
INSTANCES=$(aws ec2 describe-instances --filters "Name=tag:Type,Values=${TYPE}" "Name=tag:Environment,Values=${ENVIRONMENT}" "Name=tag:Version,Values=${VERSION}" "Name=instance-state-name,Values=running")

echo "INSTANCES:"
echo "${INSTANCES}" | jq '.Reservations[].Instances[].Tags[] | select(.Key == "Name").Value'

IPS=$(echo "${INSTANCES}" | jq '.Reservations[].Instances[].PrivateIpAddress')

echo -e "IPS:\n${IPS}"

#while read IP; do
#    IP=$(echo $IP | tr --delete "\"") #strip quotes
#    echo "Running COMMAND (${COMMAND}) on ${IP}..."
#    ssh -t ${IP} "sudo /usr/local/<folder>/bin/release.sh ${COMMAND}" < /dev/null
#done <<< "${IPS}"

#translate newlines to spaces and remove quotes
IPS=$(echo "$IPS" | tr "\n" " ")
IPS=$(echo "$IPS" | tr --delete "\"")


if pssh -i -p 5 -t 300 -H "${IPS}" "sudo /usr/local/<folder>/bin/release.sh ${COMMAND}"; then
    echo "done!"
else
    echo "Find and command failed"
    exit 1
fi
