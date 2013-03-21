#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import os
import variables
import sqlite3

class NewTask():
	def __init__(self,liststore):

		self.index=0
		self.liststore=liststore
		self.window=gtk.Window()
		self.window.set_keep_above(True)
		self.window.set_position(gtk.WIN_POS_CENTER)
		#self.window.set_decorated(False)
		self.window.set_size_request(450,175)
		self.window.set_title('新建安装任务')

		self.vbox=gtk.VBox()	
		self.window.add(self.vbox)

		hline=gtk.HSeparator()
		self.vbox.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox.pack_start(fixed,False,False,0)
		label=gtk.Label('任务名称')
		fixed.put(label,5,5)
		label=gtk.Label('服务器')
		fixed.put(label,295,5)
		self.hostname=gtk.Entry()
		self.hostname.set_size_request(150,25)
		fixed.put(self.hostname,5,25)
		self.port=gtk.ComboBoxEntry()
		self.port.set_size_request(150,25)
		fixed.put(self.port,295,25)
		label=gtk.Label('角色')
		fixed.put(label,5,60)
		label=gtk.Label('软件包')
		fixed.put(label,295,60)
		self.username=gtk.ComboBoxEntry()
		self.username.set_size_request(150,25)
		fixed.put(self.username,5,80)
		self.password=gtk.ComboBoxEntry()
		self.password.set_size_request(150,25)
		fixed.put(self.password,295,80)
		hline=gtk.HSeparator()
		hline.set_size_request(450,22)
		self.vbox.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox.pack_end(fixed,False,False,0)
		quitb=gtk.Button('退出')
		quitb.set_size_request(100,25)
		nextb=gtk.Button('确定')
		nextb.set_size_request(100,25)
		quitb.connect('clicked',self.quit)
		nextb.connect('clicked',self.quit)
		fixed.put(quitb,5,5)
		fixed.put(nextb,345,5)
		self.window.show_all()		
	def quit(self,widget):
		self.window.destroy()
	def add_server(self,widget):
		hostname=self.hostname.get_text()
		port=self.port.get_text()
		username=self.username.get_text()
		password=self.password.get_text()
		selection=self.roleview.get_selection()
		model,path=selection.get_selected()
		if path is not None:	
			role=model[path][0]
			index=model[path][1]
		if self.radio1.get_active():
			soft=self.radio1.get_label()
			flag=0
		else:
			soft=self.radio2.get_label()
			flag=1
		model=self.softview.get_model()
		pkg_list=[]
		pkg_list=self.get_soft(model)
		self.saveTodb([hostname,port,username,password,index,pkg_list])
		self.liststore.append([False,hostname,role,index,soft,flag,'准备部署','--'])
		self.window.destroy()
	def saveTodb(self,data):
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('''
					create table if not exists server
					(hostname text,port text,username text,password text,role text,package text,type text,progress text,status text)
				'''
				)
		c.execute('''
					insert into server(hostname,port,username,password,role,package,type,progress,status)
					values("%s","%s","%s","%s","%s","%s","%s","%s","%s")
				  ''' % (data[0],data[1],data[2],data[3],data[4],data[5],'0','准备部署','0')
				)
		conn.commit()
		conn.close()
	def msg(self,text):
		md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,
								gtk.BUTTONS_OK,text)
		md.run()
		md.destroy()
	def IsValid(self,text):
		list=text.split('.')
		if len(list) != 4 :
			return False
		else:
			for i in list:
				if i.isdigit() and 0 <= int(i) <= 255:
					continue
				else:
					return False
		return True
