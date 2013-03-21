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
		self.window.set_size_request(450,100)
		self.window.set_title('创建安装任务')

		self.vbox=gtk.VBox()	
		self.window.add(self.vbox)

		hline=gtk.HSeparator()
		self.vbox.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox.pack_start(fixed,False,False,0)
		label=gtk.Label('任务名称')
		fixed.put(label,20,20)
		self.hostname=gtk.Entry()
		self.hostname.set_size_request(180,25)
		fixed.put(self.hostname,20,45)
		hline=gtk.HSeparator()
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
	def toggled_role(self,cell,path,treeview):
		selection=treeview.get_selection()
		model,selected_path=selection.get_selected()
		if selected_path is not None:
			model[selected_path][2]=False
		model[path][2] = not model[path][2]
		selection.select_path(path)
		return
	def toggled_soft(self,cell,path,treeview):
		model=treeview.get_model()
		selection=treeview.get_selection()
		model[path][1] = not model[path][1]
		selection.select_path(path)
		return
	def default_toggled(self,radio):
		self.softview.set_sensitive(False)
	def custom_toggled(self,radio):
		self.softview.set_sensitive(True)
	def mkey_toggled(self,radio):
		self.roleview.set_sensitive(False)
	def cloud_toggled(self,radio):
		self.roleview.set_sensitive(True)
	def quit(self,widget):
		self.window.destroy()
	def choose_role(self,widget):
		hostname=self.hostname.get_text()
		port=self.port.get_text()
		username=self.username.get_text()
		password=self.password.get_text()
		self.vbox.hide()
		self.vbox2.show()
	def choose_soft(self,widget):
		self.vbox2.hide()
		selection=self.roleview.get_selection()
		model,path=selection.get_selected()
		value=model[path][1]
		conn=sqlite3.connect('db/map.db')
		c=conn.cursor()
		c.execute("select package from map where id='%s'"%value)
		data=c.fetchone()
		pkg=str(data[0]).split(',')	
		model=self.softview.get_model()
		iter=model.get_iter_first()
		if iter is not None:
			model.set_value(iter,1,False)
			while True:
				iter=model.iter_next(iter)
				if iter is not None:
					model.set_value(iter,1,False)
				else:
					break
		iter=model.get_iter_first()
		if iter is not None:
			for item in pkg:
				while True:
					value=model.get_value(iter,0).split('-')[0]
					if item == value :
						model.set_value(iter,1,True)
						break
					else:
						iter=model.iter_next(iter)
						if iter is None:
							iter=model.get_iter_first()
		self.vbox3.show()
	def roleview_foreach(self,model,path,iter,data):
		for item in data:	
			print item
			value=model[path][0].split('-')[0]
			if item == value:
				model[path][1]=True
			else:
				model[path][1]=False
	def get_soft(self,model):
		pkg_list=[]
		iter=model.get_iter_first()
		if iter is not None:
			if model.get_value(iter,1):
				pkg_list.append(model.get_value(iter,0))
			while model.iter_next(iter) is not None:
				iter=model.iter_next(iter)
				if model.get_value(iter,1):
					pkg_list.append(model.get_value(iter,0))
		return pkg_list
	def return_1(self,widget):
		self.vbox2.hide()
		self.vbox.show()
	def return_2(self,widget):
		self.vbox3.hide()
		self.vbox2.show()
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
