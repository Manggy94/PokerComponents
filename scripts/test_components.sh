#!/bin/sh
echo "Testing Poker Components"
python -m pytest --cov=components --cov-report html Tests/
python -m pytest --cov=components Tests/
