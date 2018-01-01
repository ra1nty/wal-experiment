# The runtime support for running a wal program

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twilio.rest import TwilioRestClient
from datetime import datetime

class WalInterpreter:

	# initialize the interpreter.
	# prog is dict with (line, statement) mapping
	def init(self, prog):
		
		self.prog = prog
		
		chrome_options = Options()
    	chrome_options.add_argument("--headless")
    	self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def eval(self, expr):
    	# evaluate expression

    def releval(self, expr):
    	# evaluate relational expression

    def assign(self, expr):
    	# all variables assignment

    def run(self):


