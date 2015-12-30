# Copyright (c) 2015 Dario Rubattu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from contractvmd import dapp, config, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)


class BookProto:
	DAPP_CODE = [ 0x50, 0x55 ]
	METHOD_POST = 0x02
	METHOD_COMMENT = 0X03
	METHOD_LIST = [METHOD_POST, METHOD_COMMENT]

	
class BookMessage (message.Message):
	def createPost (title, body):
		m = BookMessage ()
		m.Title = title
		m.Body = body
		m.DappCode = BookProto.DAPP_CODE
		m.Method = BookProto.METHOD_POST
		return m

	def createComment (postid, comment):
		m = BookMessage ()
		m.Postid = postid
		m.Comment = comment
		m.DappCode = BookProto.DAPP_CODE
		m.Method = BookProto.METHOD_COMMENT
		return m

	def toJSON (self):
		data = super (BookMessage, self).toJSON ()

		if self.Method == BookProto.METHOD_POST:
			data['title'] = self.Title
			data['body'] = self.Body
		elif self.Method == BookProto.METHOD_COMMENT:
			data['postid'] = self.Postid
			data['comment'] = self.Comment
		else:
			return None

		return data



class BookCore (dapp.Core):
	def __init__ (self, chain, database):
		super (BookCore, self).__init__ (chain, database)
		database.init ('participants', [])
		database.init ('comments', [])		
		
	def createPost (self, hashs, title, body):
		self.database.listappend ('participants', {'hash': hashs, 'title': title, 'body': body})

	def createComment (self, hashs, postid, comment):
		self.database.listappend ('comments', {'hash': hashs, 'postid': postid, 'comment': comment})
			
	def getlist (self):
		return self.database.get ('participants')
	
	def getlistcomments (self, postid):
		a = self.database.get ('participants')
		b = self.database.get ('comments')
		
		for i in a:
			number=0
			if i['hash'] == postid:
				lis = i
				for j in b:
					if j['postid'] == postid:
						number += 1
						lis['commid' + str(number)] = j['hash']
						lis['comment' + str(number)] = j['comment']
					else:
						continue
				return lis
			else:
				continue

		for i in a:
			if i['hash'] == postid:
				return i
			else:
				continue


class BookAPI (dapp.API):
	def __init__ (self, core, dht, api):
		self.api = api
		rpcmethods = {}

		rpcmethods["getlist"] = {
			"call": self.method_getlist,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["getlistcomments"] = {
			"call": self.method_getlistcomments,
			"help": {"args": ["postid"], "return": {}}
		}

		rpcmethods["createPost"] = {
			"call": self.method_createPost,
			"help": {"args": ["title", "body"], "return": {}}
		}

		rpcmethods["createComment"] = {
			"call": self.method_createComment,
			"help": {"args": ["postid", "comment"], "return": {}}
		}

		errors = { }

		super (BookAPI, self).__init__(core, dht, rpcmethods, errors)


	def method_getlist (self):
		return self.core.getlist ()

	def method_getlistcomments (self, postid):
		return self.core.getlistcomments (postid)

	def method_createPost (self, title, body):
		msg = BookMessage.createPost ( title, body)
		return self.createTransactionResponse (msg)

	def method_createComment (self, postid, comment):
		msg = BookMessage.createComment ( postid, comment)
		return self.createTransactionResponse (msg)


class book (dapp.Dapp):
	def __init__ (self, chain, db, dht, apiMaster):
		self.core = BookCore (chain, db)
		apiprov = BookAPI (self.core, dht, apiMaster)
		super (book, self).__init__(BookProto.DAPP_CODE, BookProto.METHOD_LIST, chain, db, dht, apiprov)

	def handleMessage (self, m):
		if m.Method == BookProto.METHOD_POST:
			logger.pluginfo ('Found new message %s:', m.Hash)
			self.core.createPost (m.Hash, m.Data['title'], m.Data['body'])	
		if m.Method == BookProto.METHOD_COMMENT:
			logger.pluginfo ('Found new comment %s:', m.Hash)
			self.core.createComment (m.Hash, m.Data['postid'], m.Data['comment'])			
