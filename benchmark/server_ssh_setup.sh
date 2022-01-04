#!/usr/bin/bash
# Adds the hosts to the known_hosts file.
for host in $@; do
  ssh-keyscan -T 10 $host >>~/.ssh/known_hosts
done
