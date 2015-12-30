#!/usr/bin/python3
# Copyright (c) 2015 Dario Rubattu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from book import BookManager

import os
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

# Creazione portafoglio di A
walletA = WalletExplorer.WalletExplorer (wallet_file='test.walletA')
AMan = BookManager.BookManager (consMan, wallet=walletA)

# Creazione portafoglio di B
walletB = WalletExplorer.WalletExplorer (wallet_file='test.walletB')
BMan = BookManager.BookManager (consMan, wallet=walletB)

# Creazione post di A, se questo non va a buon fine stampa "Error"
try:
	postid=AMan.createPost ('Hello post', 'Post di test')
	print ('POST-A >', postid)
except:
	print ('Error')
time.sleep (5)

# Stampa post
def wlist():
	while True:
		os.system ('clear')
		print ('Lista dei post')
		listc=AMan.getList ()
		for i in listc:
			print ('POST ->',i['hash'])
			try:
				if i['hash']==postid:
					return
			except:
				continue
		time.sleep (10)

wlist()

time.sleep (10)

# Creazione commenti ad un post esistente
try:
	commid=AMan.createComment(postid, 'This is a comment')
	print ('COMMENT-A >', commid)
except:
	print ('Error')
time.sleep (5)

# Stampa la lista dei post finchè non compare il post con l'id desiderato
def wAgetpost ():
	while True:
		os.system ('clear')
		print ('Postid',)
		wApost=AMan.getListcomments (postid)
		try:	
			if wApost['commid1']==commid:
				print ('POST(',wApost['hash'],')',wApost['title'],wApost['body'],'["',wApost['comment1'],'"]')
				return	
		except:
			print ('POST(',wApost['hash'],')',wApost['title'],wApost['body'])									
		time.sleep (10)

wAgetpost()

time.sleep(10)

# Creazione post di B, se questo non va a buon fine stampa "Error"
try:
	postid2=BMan.createPost ('Hello post 2', 'Post di test 2')
	print ('POST-B >', postid2)
except:
	print ('Error')
time.sleep (5)

# Creazione commenti ad un post esistente
try:
	commid2=BMan.createComment(postid, 'This is a comment of B')
	print ('COMMENT-B >', commid2)
except:
	print ('Error')
time.sleep (5)

# Stampa la lista dei post finchè non compare il post con l'id desiderato
def wBgetpost ():
	while True:
		os.system ('clear')
		print ('Postid',)
		wBpost=BMan.getListcomments (postid)
		try:	
			if wBpost['commid2']==commid2:
				print ('POST(',wBpost['hash'],')',wBpost['title'],wBpost['body'],'["',wBpost['comment1'],'" "',wBpost['comment2'],'"]')
				return	
		except:
			print ('POST(',wBpost['hash'],')',wBpost['title'],wBpost['body'],'["',wBpost['comment1'],'"]')									
		time.sleep (10)

wBgetpost()




	
