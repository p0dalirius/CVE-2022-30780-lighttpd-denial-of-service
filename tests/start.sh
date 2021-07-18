#!/bin/bash

for version in $(find . -type d -maxdepth 1); do
  echo $version
done