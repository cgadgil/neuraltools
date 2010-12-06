#!/bin/bash

cat $1 |python addformulatocsv.py -f "=W_NNNN/P_NNNN" -t "df-factor-1"|python addformulatocsv.py -f "=P_NNNN/X_NNNN" -t "df-factor-2"|python addformulatocsv.py -f "=X_NNNN/AQ_NNNN" -t "df-factor-3"|python addformulatocsv.py -f "=AQ_NNNN/AI_NNNN" -t "df-factor-4"|python addformulatocsv.py -f "=AI_NNNN/AM_NNNN" -t "df-factor-5"

