import pandas as pd
%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import glob
import os.path
import html5lib
from bs4 import BeautifulSoup
import bs4 as bs
import requests
import requests_random_user_agent
import edgar
import yfinance as yf
import time
import datetime
from datetime import datetime
download_directory=r'C:\Users\cwesterb\Stocks\EDGAR_Files'
since_year=1993
