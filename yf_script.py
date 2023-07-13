#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 01:00:21 2023

@author: akintayosalu
"""

import yfinance as yf

data = yf.download("MSFT", start="2023-02-02", end="2023-03-03", )