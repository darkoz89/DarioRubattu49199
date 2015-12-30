# Copyright (c) 2015 Dario Rubattu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from libcontractvm import Wallet, ConsensusManager, DappManager

class BookManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (BookManager, self).__init__(consensusManager, wallet)

	def createPost (self, title, body):
		cid = self.produceTransaction ('book.createPost', [title, body])
		return cid

	def createComment (self, postid, comment):
		cid = self.produceTransaction ('book.createComment', [postid, comment])
		return cid

	def getList (self):
		return self.consensusManager.jsonConsensusCall ('book.getlist', [])['result']

	def getListcomments (self, postid):
		return self.consensusManager.jsonConsensusCall ('book.getlistcomments', [postid])['result']

	
