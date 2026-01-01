# transaction-risk-analyzer

## Business problem

Companies often process large volumes of transactional data where:
- errors,
- fraud,
- or abnormal orders

are detected too late or manually.

This project demonstrates how such risks can be flagged automatically.

## What this solution does

- analyzes transaction quantity and price
- compares them against historical patterns
- assigns a risk score (0–100)
- produces a human-readable decision:
  - LOW RISK
  - MEDIUM RISK
  - HIGH RISK

## How to run

pip install -r requirements.txt  
python main.py

## Example output

The system produces a CSV with:
- risk score
- decision
- explanation

See `output/example_result.csv`.

## Project status

This repository contains a demo / proof-of-concept version.
The full version is developed privately.

