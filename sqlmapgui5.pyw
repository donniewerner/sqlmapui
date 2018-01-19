#!/usr/bin/python2
# -*- coding: utf-8 -*-

'''
gui for SQLmap

mwood note: this was found from an unknown version in Chinese
			I am simply builing on that work, credits to the
			original authors, and the translated version this
			is built from.

additions / to do:
done! --sql-shell
done! --forms
done! --no-cast
done! -g -q GOOGLEDORK

done! New tab
done! --os-cmd=OSCMD      Execute an operating system command
done! --os-shell          Prompt for an interactive operating system shell
done! --os-pwn            Prompt for an OOB shell, Meterpreter or VNC
done! --priv-esc          Database process user privilege escalation
done! --msf-path=MSFPATH  Local path where Metasploit Framework is installed
done! --tmp-path=TMPPATH  Remote absolute path of temporary files directory
done! append the lasturi log and add new line
done! fixed -v not working

--update
--identify-waf
--mobile
--skip-urlencode
how works? -s SESSIONFILE      Load session from a stored (.sqlite) file
--file-write=WFILE  Write a local file on the back-end DBMS file system
--file-dest=DFILE   Back-end DBMS absolute filepath to write to

'''
from Tkinter import *
import ttk
import os
import subprocess
import re
from urlparse import urlparse

#os.path.expanduser("~")
#os.path.join(os.path.expanduser("~"), ".sqlmap")
from os.path import expanduser
home = expanduser("~")


class app(Frame):
	def __init__(self, mw):
		Frame.__init__(self, mw)
		self.grid( sticky='nswe' )
		self.rowconfigure( 0, weight=1 )
		self.columnconfigure( 0, weight=1 )
		#
		n = ttk.Notebook(self)
		BuilderFrame = ttk.Frame(n)
		WatchLog = ttk.Frame(n)
		HelpMe = ttk.Frame(n)
		# Main Frames
		n.add(BuilderFrame, text='Builder')
		n.add(WatchLog, text='Watch Log')
		n.add(HelpMe, text='Help')
		n.rowconfigure( 0, weight=1 )
		n.columnconfigure( 0, weight=1 )
		n.grid(row=0, column=0, sticky='nswe')
		BuilderFrame.rowconfigure( 0, weight=1 )
		BuilderFrame.columnconfigure( 0, weight=1)
		# Help SqlMAP
		lfhelp = ttk.Labelframe(HelpMe)
		lfhelp.grid(sticky='nswe')
		scrolHelp = ttk.Scrollbar(lfhelp)
		scrolHelp.grid(row=0, column=1, sticky='ns')
		HelpMe.rowconfigure( 0, weight=1 )
		HelpMe.columnconfigure( 0, weight=1)
		lfhelp.rowconfigure( 0, weight=1 )
		lfhelp.columnconfigure( 0, weight=1)

# HELP
# orig was -h, -hh is full verbose
		manual_sqlmap = 'python2 sqlmap.py -hh'
		process = subprocess.Popen(manual_sqlmap, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		helpTXT = Text(lfhelp, yscrollcommand=scrolHelp.set, width = 73, height=24,bg='black', fg='#99E335')
		helpTXT.insert('1.0', process.communicate()[0])
		scrolHelp.config(command= helpTXT.yview)
		helpTXT.grid(row=0, column=0,ipadx=30,sticky='nswe')
		helpTXT.bind('<Button-3>',self.rClicker, add='')

# Load Log...
		lfWatchLog = ttk.Labelframe(WatchLog, text='')
		WatchLog.rowconfigure( 0, weight=1 )
		WatchLog.columnconfigure( 0, weight=1)
		lfWatchLog.grid(row = 0, column =0, sticky='nswe', columnspan=4)
		lfWatchLog.rowconfigure( 0, weight=1 )
		lfWatchLog.columnconfigure( 0, weight=1)
		scrolSes = ttk.Scrollbar(lfWatchLog)
		scrolSes.grid(row=0, column=1, sticky='ns')
		self.sesTXT = Text(lfWatchLog, yscrollcommand=scrolSes.set, width = 73, height=22,bg='black', fg='#99E335')
		scrolSes.config(command= self.sesTXT.yview)
		self.sesTXT.grid(row=0, column=0,ipadx=30,sticky='nswe')
		self.sesTXT.bind('<Button-3>',self.rClicker, add='')
		#
				
		targetbut = ttk.Button(WatchLog)
		targetbut.config(text ="target", command=self.target)
		targetbut.grid(row =1, column=1,sticky='ws')
		
		logbut = ttk.Button(WatchLog)
		logbut.config(text ="log", command=self.logs)
		logbut.grid(row =1, column=2, sticky='ws')
		#
		sesbut = ttk.Button(WatchLog)
		sesbut.config(text ="session", command=self.session)
		sesbut.grid(row =1, column=4,sticky='ws')

		fuckbut = ttk.Button(WatchLog)
		fuckbut.config(text ="del-log", command=self.fuck)
		fuckbut.grid(row =1, column=3,sticky='ws')
		
		#
		panedUrl = ttk.Panedwindow(BuilderFrame, orient=VERTICAL)
		panedUrl.rowconfigure( 0, weight=1 )
		panedUrl.columnconfigure( 0, weight=1 )

	#--url=URL
		urlLF = ttk.Labelframe(panedUrl, text='Target url', width=100, height=100)
		urlLF.rowconfigure( 0, weight=1 )
		urlLF.columnconfigure( 0, weight=1)
		panedUrl.add(urlLF)
		# history log
		self.urlentry = ttk.Combobox(urlLF)
		self.urlentry.grid(row=0, column=0,sticky = 'we', pady=5)
		texturl = open(r""+home+"/.sqlmap/sqlmapgui.log", 'a+').readlines()
		self.urlentry['values'] = texturl
		self.urlentry.bind('<Button-3>',self.rClicker, add='')
		
#query to sqlmap
		queryLF = ttk.Labelframe(panedUrl, text='query to sqlmap:', width=100, height=100)
		queryLF.rowconfigure( 0, weight=1 )
		queryLF.columnconfigure( 0, weight=1 )
		panedUrl.add(queryLF)
		self.sql_var = StringVar()
		self.sqlEdit = ttk.Entry(queryLF)
		self.sqlEdit.config(text="", textvariable = self.sql_var)
		self.sqlEdit.grid(sticky = 'we', pady=5)
		self.sqlEdit.columnconfigure(0, weight=1)
		self.sqlEdit.bind('<Button-3>',self.rClicker, add='')
		#
		panedUrl.grid(row=0, column=0, sticky='we', rowspan =2)

# main frame
		noBF = ttk.Notebook(BuilderFrame)
		setingsF = ttk.Frame(noBF)
		enumerationF = ttk.Frame(noBF)
		requestF = ttk.Frame(noBF)
		fileF = ttk.Frame(noBF)
		ospwntabF = ttk.Frame(noBF)
		noBF.add(setingsF, text='Setings')
		noBF.add(enumerationF, text='Enumeration')
		noBF.add(requestF, text='Request')
		noBF.add(fileF, text='File Ops')
		noBF.add(ospwntabF, text='OS Pwn')
		noBF.columnconfigure(0, weight=1)
		noBF.grid(sticky = 'nswe')
		#
		setingsF.columnconfigure(0, weight=1)
		requestF.columnconfigure(0, weight=1)
		fileF.columnconfigure(0, weight=1)

# take query SqlMAP
		but = ttk.Button(BuilderFrame)
		but.config(text ="get query",width = 10, command=self.commands)
		#
		but.grid(row=3,column=0, sticky='nw')
		#
		butInj = ttk.Button(BuilderFrame)
		butInj.config(text ="start",width = 10, command=self.injectIT)
		butInj.grid(row=3,column=0, sticky='ne')
		# Group (I-njections,T-ampers,O-ptimize)
		panedITO = ttk.Panedwindow(setingsF, orient=HORIZONTAL)
		panedITO.rowconfigure( 0, weight=1 )
		panedITO.columnconfigure( 0, weight=1 )
		#
		injectionLF = ttk.Labelframe(panedITO, text='Injection')
		injectionLF.rowconfigure( 0, weight=1 )
		injectionLF.columnconfigure( 0, weight=1 )
		#
		tampersLF = ttk.Labelframe(panedITO, text='Tampers')
		tampersLF.rowconfigure( 0, weight=1 )
		tampersLF.columnconfigure( 0, weight=1 )
		#
		panedITO.add(injectionLF)
		panedITO.add(tampersLF)
		panedITO.grid(row=0, column=0, sticky='nswe')
		#############################
		panedO = ttk.Panedwindow(setingsF, orient=HORIZONTAL)
		panedO.rowconfigure( 0, weight=1 )
		panedO.columnconfigure( 0, weight=1 )
		#
		optimizLF = ttk.Labelframe(panedO, text='')
		optimizLF.rowconfigure( 0, weight=1)
		optimizLF.columnconfigure( 0, weight=1 )
		#
		panedO.add(optimizLF)
		panedO.grid(row=0, column=1, sticky='nswe', rowspan=2)
		
#-p TESTPARAMETER    Testable parameter(s)
		self.entryParam = ttk.Entry(injectionLF)
		self.entryParam.config(width=15)
		self.entryParam.grid(row=3,column=1, sticky='nswe')
		self.entryParam.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkParam = ttk.Checkbutton(injectionLF)
		self.chkParam_var = StringVar()
		self.chkParam.config(text="parametr", variable= self.chkParam_var, onvalue= "on" , offvalue = "off", command= self.chekParam)
		self.chkParam.grid(row=3,column = 0, sticky = 'w')
#--dbms Select database
		self.chk_dbms = ttk.Checkbutton(injectionLF)
		self.chk_dbms_var = StringVar()
		self.chk_dbms.config(text="dbms", variable= self.chk_dbms_var, onvalue= "on" , offvalue = "off", command= self.chek_dbms)
		self.chk_dbms.grid(row=0,column=0,sticky = 'sw')
		#
		self.box = ttk.Combobox(injectionLF)
		self.box_value = StringVar()
		self.box.config(textvariable=self.box_value, state='disabled', width = 15)
		self.box['values'] = ("mysql", "access", "firebird", "maxdb", "mssql", "oracle", "pgsql", "sqlite", "sybase")
		self.box.current(0)
		self.box.bind('<<ComboboxSelected>>', self.chek_dbms)
		self.box.grid(row=0,column=1,sticky ='sw')
	# Prefix:
		self.entryPrefix = ttk.Entry(injectionLF)
		self.entryPrefix.config(text="" , textvariable="", width = 15)
		self.entryPrefix.grid(row=4,column=1, sticky='nswe')
		self.entryPrefix.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkPrefix = ttk.Checkbutton(injectionLF)
		self.chkPrefix_var = StringVar()
		self.chkPrefix.config(text="prefix", variable= self.chkPrefix_var, onvalue= "on" , offvalue = "off", command= self.chekPrefix)
		self.chkPrefix.grid(row=4,column = 0, sticky ='w')
	# Suffix:
		self.entrySuffix = ttk.Entry(injectionLF)
		self.entrySuffix.config(text="" , textvariable="", width = 15)
		self.entrySuffix.grid(row=5,column=1, sticky='nswe')
		self.entrySuffix.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkSuffix = ttk.Checkbutton(injectionLF)
		self.chkSuffix_var = StringVar()
		self.chkSuffix.config(text="suffix", variable= self.chkSuffix_var, onvalue= "on" , offvalue = "off", command= self.chekSuffix)
		self.chkSuffix.grid(row=5,column = 0, sticky ='w')
	# --os
		self.entryOS = ttk.Entry(injectionLF)
		self.entryOS.config(text="" , textvariable="", width = 15)
		self.entryOS.grid(row=6,column=1, sticky='nswe')
		self.entryOS.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkOS = ttk.Checkbutton(injectionLF)
		self.chkOS_var = StringVar()
		self.chkOS.config(text="OS", variable= self.chkOS_var, onvalue= "on" , offvalue = "off", command= self.chekOS)
		self.chkOS.grid(row=6,column = 0, sticky = 'w')
	#--skip
		self.entrySkip = ttk.Entry(injectionLF)
		self.entrySkip.config(text="" , textvariable="", width = 15)
		self.entrySkip.grid(row=7,column=1, sticky='nswe')
		self.entrySkip.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkSkip = ttk.Checkbutton(injectionLF)
		self.chkSkip_var = StringVar()
		self.chkSkip.config(text="skip", variable= self.chkSkip_var, onvalue= "on" , offvalue = "off", command= self.chekSkip)
		self.chkSkip.grid(row=7,column = 0, sticky = 'w')
	# was Banner ( does anyone use it even? )
	# --no-cast
		self.chk_Banner = ttk.Checkbutton(injectionLF)
		self.chk_Banner_var = StringVar()
		self.chk_Banner.config(text="no-cast", variable= self.chk_Banner_var, onvalue= "on", offvalue = "off", command= self.chekBanner)
		self.chk_Banner.grid(row=8,column=0, sticky= 'w')
	
	#-Tamper:
		self.Ltamper=Listbox(tampersLF,height=8,width=31,selectmode=EXTENDED)
		# *.py in listbox, exclude __init__.py
		# the fuq edit works and not ./tamper
		files_tamper = os.listdir('tamper')
		tampers = filter(lambda x: x.endswith('.py'), files_tamper)
		for tamp_list in tampers:
			if tamp_list not in "__init__.py":
				self.Ltamper.insert(END,tamp_list)
		self.Ltamper.rowconfigure( 0, weight=1 )
		self.Ltamper.columnconfigure( 0, weight=1 )
		self.Ltamper.grid(row =0, column = 0, padx=5, sticky='nswe')
	# Tamper Scroll
		scrollTamper = ttk.Scrollbar(tampersLF, orient=VERTICAL, command=self.Ltamper.yview)
		self.Ltamper['yscrollcommand'] = scrollTamper.set
		scrollTamper.grid(row=0,column=1, sticky='ns')
	
# Optimizations
		optimiz_LF = ttk.Labelframe(optimizLF, text='Optimizations')
		optimiz_LF.grid(row=0, sticky='nw', pady=1)
	#-o turn on optimizations
		self.chkOpt = ttk.Checkbutton(optimiz_LF)
		self.chkOpt_var = StringVar()
		self.chkOpt.config(text="o (all optimizations)", variable= self.chkOpt_var, onvalue= "on" , offvalue = "off", command= self.chekOpt)
		self.chkOpt.grid(row=0,column = 0, sticky = 'wn', pady=1)
	#--predict-output    Predict common queries output
		self.chkPred = ttk.Checkbutton(optimiz_LF)
		self.chkPred_var = StringVar()
		self.chkPred.config(text="predict-output", variable= self.chkPred_var, onvalue= "on" , offvalue = "off", command= self.chekPred)
		self.chkPred.grid(row=1,column = 0, sticky = 'wn', pady=1)
	#--keep-alive
		self.chkKeep = ttk.Checkbutton(optimiz_LF)
		self.chkKeep_var = StringVar()
		self.chkKeep.config(text="keep-alive", variable= self.chkKeep_var, onvalue= "on" , offvalue = "off", command= self.chekKeep)
		self.chkKeep.grid(row=2,column = 0, sticky = 'wn', pady=1)
	#--null-connection   Retrieve page length without actual HTTP response body
		self.chkNull = ttk.Checkbutton(optimiz_LF)
		self.chkNull_var = StringVar()
		self.chkNull.config(text="null-connection", variable= self.chkNull_var, onvalue= "on" , offvalue = "off", command= self.chekNull)
		self.chkNull.grid(row=3,column = 0, sticky = 'wn', pady=1)
	#--threads=THREADS   Max number of concurrent HTTP(s) requests (default 1)
		self.chk_thr = ttk.Checkbutton(optimiz_LF)
		self.chk_thr_var = StringVar()
		self.chk_thr.config(text="threads", variable= self.chk_thr_var, onvalue= "on", offvalue = "off", command= self.chek_thr)
		self.chk_thr.grid(row=4,column=0,sticky = 'wn', pady=1)
		self.thr = ttk.Combobox(optimiz_LF)
		self.thr_value = StringVar()
		self.thr.config(textvariable=self.thr_value, state='disable', width = 5)
		self.thr['values'] = ('1','2', '3','4','5','6','7','8','9','10')
		self.thr.current(0)
		self.thr.bind('<<ComboboxSelected>>', self.chek_thr)
		self.thr.grid(row=4,column=1,sticky ='w')
	# Verbose
		otherLF = ttk.Labelframe(optimizLF, text='other')
		otherLF.grid(row=1, sticky='nwe')
	#-f, --fingerprint
		self.chk_fing = ttk.Checkbutton(otherLF)
		self.chk_fing_var = StringVar()
		self.chk_fing.config(text="fingerprint", variable= self.chk_fing_var, onvalue= "on", offvalue = "off", command= self.chekFing)
		self.chk_fing.grid(row=0,column=0, sticky= 'nw')

	# was --logic-negative
		self.chkNeg = ttk.Checkbutton(otherLF)
		self.chkNeg_var = StringVar()
		self.chkNeg.config(text="invalid-logical", variable= self.chkNeg_var, onvalue= "on" , offvalue = "off", command= self.chekNeg)
		self.chkNeg.grid(row=1,column = 0, sticky = 'w')

	# --hex
		self.chk_Hex = ttk.Checkbutton(otherLF)
		self.chk_Hex_var = StringVar()
		self.chk_Hex.config(text="hex", variable= self.chk_Hex_var, onvalue= "on", offvalue = "off", command= self.chekHex)
		self.chk_Hex.grid(row=2,column=0, sticky= 'nw')
	# --forms
		self.chk_Forms = ttk.Checkbutton(otherLF)
		self.chk_Forms_var = StringVar()
		self.chk_Forms.config(text="forms", variable= self.chk_Forms_var, onvalue= "on", offvalue = "off", command= self.chekForms)
		self.chk_Forms.grid(row=3,column=0, sticky= 'nw')
	# Verbose
		self.chk_verb = ttk.Checkbutton(otherLF)
		self.chk_verb_var = StringVar()
		self.chk_verb.config(text="verbose", variable= self.chk_verb_var, onvalue= "on", offvalue = "off", command= self.chek_verb)
		self.chk_verb.grid(row=4,column=0, sticky='wn')
		self.box_verb = ttk.Combobox(otherLF)
		self.box_verb_value = StringVar()
		self.box_verb.config(textvariable=self.box_verb_value, state='disabled', width = 5)
		self.box_verb['values'] = ('1', '2', '3','4','5','6')
		self.box_verb.current(0)
		self.box_verb.bind('<<ComboboxSelected>>', self.chek_verb)
		self.box_verb.grid(row=4,column=1,sticky ='e')
	
	# Group (Detections,Techniques,Other)
		panedDTO = ttk.Panedwindow(setingsF, orient=HORIZONTAL)
		panedDTO.rowconfigure( 0, weight=1 )
		panedDTO.columnconfigure( 0, weight=1 )
		#
		detectionLF = ttk.Labelframe(panedDTO, text='Detection', width=100, height=100)
		detectionLF.rowconfigure( 0, weight=1 )
		detectionLF.columnconfigure( 0, weight=1 )
		#
		techniqueLF = ttk.Labelframe(panedDTO, text='Technique', width=100, height=100)
		techniqueLF.rowconfigure( 0, weight=1 )
		techniqueLF.columnconfigure( 0, weight=1 )
		#
		panedDTO.add(detectionLF)
		panedDTO.add(techniqueLF)
		panedDTO.grid(row=1, column=0, columnspan=1,sticky='we',ipady=0)
	# String:
		self.entryStr = ttk.Entry(detectionLF)
		self.entryStr.config(text="" , textvariable="")
		self.entryStr.grid(row=0,column=1, sticky = 'we')
		self.entryStr.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkStr = ttk.Checkbutton(detectionLF)
		self.chkStr_var = StringVar()
		self.chkStr.config(text="String", variable= self.chkStr_var, onvalue= "on" , offvalue = "off", command= self.chekStr)
		self.chkStr.grid(row=0,column = 0, sticky = 'sw')
	#--regexp=REGEXP
		self.entryReg = ttk.Entry(detectionLF)
		self.entryReg.config(text="" , textvariable="", width = 22)
		self.entryReg.grid(row=1,column=1)
		self.entryReg.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkReg = ttk.Checkbutton(detectionLF)
		self.chkReg_var = StringVar()
		self.chkReg.config(text="Regexp", variable= self.chkReg_var, onvalue= "on" , offvalue = "off", command= self.chekReg)
		self.chkReg.grid(row=1,column = 0, sticky = 'sw')
	#--code=CODE
		self.chkCode = ttk.Checkbutton(detectionLF)
		self.chkCode_var = StringVar()
		self.chkCode.config(text="Code", variable= self.chkCode_var, onvalue= "on" , offvalue = "off", command= self.chekCode)
		self.chkCode.grid(row=3,column = 0, sticky = 'w')
		#old
		#self.entryCode = ttk.Entry(detectionLF)
		#self.entryCode.config(text="" , textvariable="", width = 22)
		#self.entryCode.grid(row=3,column=1)
#added by wood - common HTTP codes
		self.boxCode = ttk.Combobox(detectionLF)
		self.boxCode_value = StringVar()
		self.boxCode.config(textvariable=self.boxCode_value, state='disabled', width = 5)
		self.boxCode['values'] = ('200', '301', '302', '403', '500', '400', '401', '404')
		self.boxCode.current(0)
		self.boxCode.bind('<<ComboboxSelected>>', self.chekCode)
		self.boxCode.grid(row=3,column=1,sticky = 'w')

	#--level=LEVEL
		self.chk_level = ttk.Checkbutton(detectionLF)
		self.chk_level_var = StringVar()
		self.chk_level.config(text="level", variable= self.chk_level_var, onvalue= "on" , offvalue = "off", command= self.chek_level)
		self.chk_level.grid(row=4,column=0,sticky = 'w')
		#
		self.box_level = ttk.Combobox(detectionLF)
		self.box_level_value = StringVar()
		self.box_level.config(textvariable=self.box_level_value, state='disabled', width = 5)
		self.box_level['values'] = ('0','1', '2', '3', '4', '5')
		self.box_level.current(0)
		self.box_level.bind('<<ComboboxSelected>>', self.chek_level)
		self.box_level.grid(row=4,column=1,sticky = 'w')
	#--risk=RISK
		self.chk_risk = ttk.Checkbutton(detectionLF)
		self.chk_risk_var = StringVar()
		self.chk_risk.config(text="risk", variable= self.chk_risk_var, onvalue= "on", offvalue = "off", command= self.chek_risk)
		self.chk_risk.grid(row=5,column=0,sticky = 'w')
		#
		self.box_risk = ttk.Combobox(detectionLF)
		self.box_risk_value = StringVar()
		self.box_risk.config(textvariable=self.box_risk_value, state='disabled', width = 5)
		self.box_risk['values'] = ('0','1', '2', '3')
		self.box_risk.current(0)
		self.box_risk.bind('<<ComboboxSelected>>', self.chek_risk)
		self.box_risk.grid(row=5,column=1,sticky = 'w')
	#--text-only
		self.chkTxt = ttk.Checkbutton(detectionLF)
		self.chk_Txt_var = StringVar()
		self.chkTxt.config(text="text-only", variable= self.chk_Txt_var, onvalue= "on" , offvalue = "off", command= self.chekTxt)
		self.chkTxt.grid(row=4,column = 1, sticky = 'e')
	#--titles
		self.chkTit = ttk.Checkbutton(detectionLF)
		self.chk_Tit_var = StringVar()
		self.chkTit.config(text="titles", variable= self.chk_Tit_var, onvalue= "on" , offvalue = "off", command= self.chekTit)
		self.chkTit.grid(row=5,column = 1, sticky = 'e', padx=22)
	#--technique=TECH
		self.chk_tech = ttk.Checkbutton(techniqueLF)
		self.chk_tech_var = StringVar()
		self.chk_tech.config(text="technique", variable= self.chk_tech_var, onvalue= "on", offvalue = "off", command= self.chek_tech)
		self.chk_tech.grid(row=0,column=0,sticky = 'nw')
		#
		self.boxInj = ttk.Combobox(techniqueLF)
		self.boxInj_value = StringVar()
		self.boxInj.config(textvariable=self.boxInj_value, state='disabled', width = 15)
		self.boxInj['values'] = ('BU','SU','BEUS','B','E','U','S','T','Q')
		self.boxInj.current(0)
		self.boxInj.bind('<<ComboboxSelected>>', self.chek_tech)
		self.boxInj.grid(row=0,column=1,sticky ='nwe')
		#

		sep = ttk.Separator(techniqueLF, orient=HORIZONTAL)
		sep.grid(row = 4, sticky='w', pady=10)

	#--union-cols
		self.entryCol = ttk.Entry(techniqueLF)
		self.entryCol.config(text = "" , textvariable = "", width = 15)
		self.entryCol.grid(row = 1,column = 1, sticky='nwe')
		#
		self.chkCol = ttk.Checkbutton(techniqueLF)
		self.chkCol_var = StringVar()
		self.chkCol.config(text="UNION cols", variable= self.chkCol_var, onvalue= "on" , offvalue = "off", command= self.chekCol)
		self.chkCol.grid(row=1,column = 0, sticky = 'nw')
	#--union-char
		self.entryChar = ttk.Entry(techniqueLF)
		self.entryChar.config(text="" , textvariable="", width = 15)
		self.entryChar.grid(row=2,column=1, sticky='nwe')
		#
		self.chkChar = ttk.Checkbutton(techniqueLF)
		self.chkChar_var = StringVar()
		self.chkChar.config(text="UNION char", variable= self.chkChar_var, onvalue= "on" , offvalue = "off", command= self.chekChar)
		self.chkChar.grid(row=2,column = 0, sticky = 'nw')

	#--time-sec
		self.entrySec = ttk.Entry(techniqueLF)
		self.entrySec.config(text="" , textvariable="", width = 15)
		self.entrySec.grid(row=3,column=1, sticky='nwe')
		self.chkSec = ttk.Checkbutton(techniqueLF)
		self.chkSec_var = StringVar()
		self.chkSec.config(text="time-sec", variable= self.chkSec_var, onvalue= "on" , offvalue = "off", command= self.chekSec)
		self.chkSec.grid(row=3,column = 0, sticky = 'nw')

#added Google
#
		self.entryGoo = ttk.Entry(techniqueLF)
		self.entryGoo.config(text="" , textvariable="", width = 15)
		self.entryGoo.grid(row=4,column=1, sticky='nwe')
		self.chkGoo = ttk.Checkbutton(techniqueLF)
		self.chkGoo_var = StringVar()
		self.chkGoo.config(text="Google", variable= self.chkGoo_var, onvalue= "on" , offvalue = "off", command= self.chekGoo)
		self.chkGoo.grid(row=4,column = 0, sticky = 'nw')
		self.entryGoo.bind('<Button-3>',self.rClicker, add='')
		
	# data
		dataLF = ttk.Labelframe(requestF, text='data')
		dataLF.grid(row = 0, column =0, sticky='we')
		dataLF.columnconfigure(0, weight=1)
		#
		self.chkdata = ttk.Checkbutton(dataLF)
		self.chkdata_var = StringVar()
		self.chkdata.config(text = "", variable= self.chkdata_var, onvalue= "on" , offvalue = "off", command= self.chekdata)
		self.chkdata.grid(row=0,column=0, sticky='w')
		#
		self.entryData = ttk.Entry(dataLF)
		self.entryData.grid(row =0,column=0, sticky='we', padx=30)
		self.entryData.bind('<Button-3>',self.rClicker, add='')
		# cookie:
		cookieLF = ttk.Labelframe(requestF, text='cookie')
		cookieLF.grid(row = 1, column =0, sticky='we')
		cookieLF.columnconfigure(0, weight=1)
		#
		self.chkCook = ttk.Checkbutton(cookieLF)
		self.chkCook_var = StringVar()
		self.chkCook.config(text="", variable= self.chkCook_var, onvalue= "on" , offvalue = "off", command= self.chekCook)
		self.chkCook.grid(row=0,column=0, sticky='w')
		#
		self.entryCook = ttk.Entry(cookieLF)
		self.entryCook.grid(row=0,column=0, sticky='snwe', padx=30)
		self.entryCook.bind('<Button-3>',self.rClicker, add='')

##########################
#OSPwn tab by wood
		OSPwnLF = ttk.Labelframe(ospwntabF, text='Operating system access')
		OSPwnLF.grid(row = 0, column = 0, padx=10, pady = 10, sticky='w')
		
	# set one static box --foo
	# --os-shell
		self.chkOs_shell = ttk.Checkbutton(OSPwnLF)
		self.chkOs_shell_var = StringVar()
		self.chkOs_shell.config(text="os shell", variable= self.chkOs_shell_var, onvalue= "on" , offvalue = "off", command= self.chekOs_shell)
		self.chkOs_shell.grid(row=0,column=0,sticky = 'w')
	# set a box with data entry option --foo=bar
	# --os-cmd=
		self.entryOs_cmd = ttk.Entry(OSPwnLF)
		self.entryOs_cmd.config(text="" , textvariable="", width = 35)
		self.entryOs_cmd.grid(row=1,column=1, sticky='nwe')
		self.entryOs_cmd.bind('<Button-3>',self.rClicker, add='')
		self.chkOs_cmd = ttk.Checkbutton(OSPwnLF)
		self.chkOs_cmd_var = StringVar()
		self.chkOs_cmd.config(text="os cmd", variable= self.chkOs_cmd_var, onvalue= "on" , offvalue = "off", command= self.chekOs_cmd)
		self.chkOs_cmd.grid(row=1,column = 0, sticky = 'nw')

#--os-pwn
		self.chkOs_pwn = ttk.Checkbutton(OSPwnLF)
		self.chkOs_pwn_var = StringVar()
		self.chkOs_pwn.config(text="os pwn", variable= self.chkOs_pwn_var, onvalue= "on" , offvalue = "off", command= self.chekOs_pwn)
		self.chkOs_pwn.grid(row=3,column=0,sticky = 'w')


#--msf-path=MSFPATH  Local path where Metasploit Framework is installed
		self.entryMsf_path = ttk.Entry(OSPwnLF)
		self.entryMsf_path.config(text="" , textvariable="", width = 35)
		self.entryMsf_path.grid(row=4,column=1, sticky='nwe')
		self.entryMsf_path.bind('<Button-3>',self.rClicker, add='')
		self.chkMsf_path = ttk.Checkbutton(OSPwnLF)
		self.chkMsf_path_var = StringVar()
		self.chkMsf_path.config(text="MSF path", variable= self.chkMsf_path_var, onvalue= "on" , offvalue = "off", command= self.chekMsf_path)
		self.chkMsf_path.grid(row=4,column = 0, sticky = 'nw')
#--tmp-path=TMPPATH  Remote absolute path of temporary files directory
		self.entryTmp_path = ttk.Entry(OSPwnLF)
		self.entryTmp_path.config(text="" , textvariable="", width = 35)
		self.entryTmp_path.grid(row=5,column=1, sticky='nwe')
		self.entryTmp_path.bind('<Button-3>',self.rClicker, add='')
		self.chkTmp_path = ttk.Checkbutton(OSPwnLF)
		self.chkTmp_path_var = StringVar()
		self.chkTmp_path.config(text="TMP path", variable= self.chkTmp_path_var, onvalue= "on" , offvalue = "off", command= self.chekTmp_path)
		self.chkTmp_path.grid(row=5,column = 0, sticky = 'nw')

#--priv-esc 
		self.chkPriv_esc = ttk.Checkbutton(OSPwnLF)
		self.chkPriv_esc_var = StringVar()
		self.chkPriv_esc.config(text="priv esc", variable= self.chkPriv_esc_var, onvalue= "on" , offvalue = "off", command= self.chekPriv_esc)
		self.chkPriv_esc.grid(row=2,column=0,sticky = 'w')
	

# Enumerate
		enumerateLF = ttk.Labelframe(enumerationF, text='Enumerate')
		enumerateLF.grid(row = 0, column = 0, padx=10, pady = 10, sticky='w')
	# Retrieve DBMS current user
		self.chkCurrent_user = ttk.Checkbutton(enumerateLF)
		self.chkCurrent_user_var = StringVar()
		self.chkCurrent_user.config(text="current-user", variable= self.chkCurrent_user_var, onvalue= "on" , offvalue = "off", command= self.chekCurrent_user)
		self.chkCurrent_user.grid(row=0,column=0,sticky = 'w')
	# Retrieve DBMS current database
		self.chkCurrent_db = ttk.Checkbutton(enumerateLF)
		self.chkCurrent_db_var = StringVar()
		self.chkCurrent_db.config(text="current-db", variable= self.chkCurrent_db_var, onvalue= "on" , offvalue = "off", command= self.chekCurrent_db)
		self.chkCurrent_db.grid(row=1,column=0,sticky = 'w')
	#was --is-dba   Detect if the DBMS current user is DBA
	# --all Enumerate All
		self.chk_is_dba = ttk.Checkbutton(enumerateLF)
		self.chk_is_dba_var = StringVar()
		self.chk_is_dba.config(text="enum all", variable= self.chk_is_dba_var, onvalue= "on" , offvalue = "off", command= self.chek_is_dba)
		self.chk_is_dba.grid(row=2,column=0,sticky = 'w')
	#--users             Enumerate DBMS users
		self.chk_users = ttk.Checkbutton(enumerateLF)
		self.chk_users_var = StringVar()
		self.chk_users.config(text="users", variable= self.chk_users_var, onvalue= "on" , offvalue = "off", command= self.chek_users)
		self.chk_users.grid(row=3,column=0,sticky = 'w')
	#-passwords         Enumerate DBMS users password hashes
		self.chk_passwords = ttk.Checkbutton(enumerateLF)
		self.chk_passwords_var = StringVar()
		self.chk_passwords.config(text="passwords", variable= self.chk_passwords_var, onvalue= "on" , offvalue = "off", command= self.chek_passwords)
		self.chk_passwords.grid(row=0,column=1,sticky = 'w')
#was --privileges        Enumerate DBMS users privileges
	# --sql-shell
		self.chk_privileges  = ttk.Checkbutton(enumerateLF)
		self.chk_privileges_var = StringVar()
		self.chk_privileges.config(text="sql shell", variable= self.chk_privileges_var, onvalue= "on" , offvalue = "off", command= self.chek_privileges)
		self.chk_privileges.grid(row=1,column=1,sticky = 'w')
	#--roles             Enumerate DBMS users roles
		self.chk_roles = ttk.Checkbutton(enumerateLF)
		self.chk_roles_var = StringVar()
		self.chk_roles.config(text="roles", variable= self.chk_roles_var, onvalue= "on" , offvalue = "off", command= self.chek_roles)
		self.chk_roles.grid(row=2,column=1,sticky = 'w')
	#-dbs               Enumerate DBMS databases
		self.chk_dbs = ttk.Checkbutton(enumerateLF)
		self.chk_dbs_var = StringVar()
		self.chk_dbs.config(text="dbs", variable= self.chk_dbs_var, onvalue= "on" , offvalue = "off", command= self.chek_dbs)
		self.chk_dbs.grid(row=3,column=1,sticky = 'w')
	#--tables            Enumerate DBMS database tables
		self.chk_tables = ttk.Checkbutton(enumerateLF)
		self.chk_tables_var = StringVar()
		self.chk_tables.config(text="tables", variable= self.chk_tables_var, onvalue= "on" , offvalue = "off", command= self.chek_tables)
		self.chk_tables.grid(row=0,column=2,sticky = 'w')
	#--columns           Enumerate DBMS database table columns
		self.chk_columns = ttk.Checkbutton(enumerateLF)
		self.chk_columns_var = StringVar()
		self.chk_columns.config(text="columns", variable= self.chk_columns_var, onvalue= "on" , offvalue = "off", command= self.chek_columns)
		self.chk_columns.grid(row=1,column=2,sticky = 'w')
	#--schema            Enumerate DBMS schema
		self.chk_schema = ttk.Checkbutton(enumerateLF)
		self.chk_schema_var = StringVar()
		self.chk_schema.config(text="schema", variable= self.chk_schema_var, onvalue= "on" , offvalue = "off", command= self.chek_schema)
		self.chk_schema.grid(row=2,column=2,sticky = 'w')
	#--count             Retrieve number of entries for table(s)
		self.chk_count  = ttk.Checkbutton(enumerateLF)
		self.chk_count_var = StringVar()
		self.chk_count.config(text="count", variable= self.chk_count_var, onvalue= "on" , offvalue = "off", command= self.chek_count)
		self.chk_count.grid(row=3,column=2,sticky = 'w')
	
	#--dump              Dump DBMS database table entries
		dumpLF = ttk.Labelframe(enumerationF, text='Dump')
		dumpLF.grid(row = 0, column=1, pady = 10, padx=10, sticky='w')
		#
		self.chk_dump = ttk.Checkbutton(dumpLF)
		self.chk_dump_var = StringVar()
		self.chk_dump.config(text="dump", variable= self.chk_dump_var, onvalue= "on" , offvalue = "off", command= self.chek_dump)
		self.chk_dump.grid(row=1,column=1,sticky = 'w')
		
	#--dump-all          Dump all DBMS databases tables entries
		self.chk_dump_all = ttk.Checkbutton(dumpLF)
		self.chk_dump_all_var = StringVar()
		self.chk_dump_all.config(text="dump-all", variable= self.chk_dump_all_var, onvalue= "on" , offvalue = "off", command= self.chek_dump_all)
		self.chk_dump_all.grid(row=2,column=1,sticky = 'w')
	#--search            Search column(s), table(s) and/or database name(s)
		self.chk_search = ttk.Checkbutton(dumpLF)
		self.chk_search_var = StringVar()
		self.chk_search.config(text="search", variable= self.chk_search_var, onvalue= "on" , offvalue = "off", command= self.chek_search)
		self.chk_search.grid(row=3,column=1,sticky = 'w')
	#--exclude-sysdbs    Exclude DBMS system databases when enumerating tables
		self.chk_exclude = ttk.Checkbutton(dumpLF)
		self.chk_exclude_var = StringVar()
		self.chk_exclude.config(text="exclude-sysdbs", variable= self.chk_exclude_var, onvalue= "on" , offvalue = "off", command= self.chek_exclude)
		self.chk_exclude.grid(row=4,column=1,sticky = 'w')

	#-D DB   DBMS database to enumerate БД, Таблица, Колонка
		dtcLF = ttk.Labelframe(enumerationF, text='DB, Table, Column')
		dtcLF.grid(row = 1, column=0, pady = 10, ipady=5, padx=10, sticky='we', columnspan=5)
		dtcLF.columnconfigure(0, weight=1)
		#
		self.entryD = ttk.Entry(dtcLF)
		self.entryD.config(text="" , textvariable="")
		self.entryD.grid(row=0,column=0, sticky='we', padx=30)
		self.entryD.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkD = ttk.Checkbutton(dtcLF)
		self.chkD_var = StringVar()
		self.chkD.config(text="D", variable= self.chkD_var, onvalue= "on" , offvalue = "off", command= self.chekD)
		self.chkD.grid(row=0,column = 0, sticky = 'w')
	#-T TBL  DBMS database table to enumerate
		self.entryT = ttk.Entry(dtcLF)
		self.entryT.config(text="" , textvariable="")
		self.entryT.grid(row=1,column=0,sticky='we', padx=30)
		self.entryT.bind('<Button-3>',self.rClicker, add='')
		self.chkT = ttk.Checkbutton(dtcLF)
		self.chkT_var = StringVar()
		self.chkT.config(text="T", variable= self.chkT_var, onvalue= "on" , offvalue = "off", command= self.chekT)
		self.chkT.grid(row=1,column = 0, sticky = 'w')
	#-C COL  DBMS database table column to enumerate
		self.entryC = ttk.Entry(dtcLF)
		self.entryC.config(text="" , textvariable="")
		self.entryC.grid(row=2,column=0, sticky='we', padx=30)
		self.entryC.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkC = ttk.Checkbutton(dtcLF)
		self.chkC_var = StringVar()
		self.chkC.config(text="C", variable= self.chkC_var, onvalue= "on" , offvalue = "off", command= self.chekC)
		self.chkC.grid(row=2,column = 0, sticky = W)
		
		
	#--sql-query=:
		sqlQueryLF = ttk.Labelframe(enumerationF, text='SQL-query:')
		sqlQueryLF.grid(row = 2, column=0, ipady=5, pady = 10, padx=10, sticky='we', columnspan=5)
		sqlQueryLF.columnconfigure(0, weight=1)
		#
		self.entryQuery = ttk.Entry(sqlQueryLF)
		self.entryQuery.config(text="" , textvariable="")
		self.entryQuery.grid(row=0,column=0, sticky='we', padx=30)
		self.entryQuery.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkQuery = ttk.Checkbutton(sqlQueryLF)
		self.chkQuery_var = StringVar()
		self.chkQuery.config(text="", variable= self.chkQuery_var, onvalue= "on" , offvalue = "off", command= self.chekQuery)
		self.chkQuery.grid(row=0,column=0,sticky = 'w')

#rare1	
	#--start=LIMITSTART  First query output entry to retrieve
		limitLF = ttk.Labelframe(enumerationF, text='limit')
		limitLF.grid(row = 0, column=4, pady=10, padx=10, sticky='w')
		#
		self.entry_start= ttk.Entry(limitLF)
		self.entry_start.config(text="" , textvariable="", width = 5)
		self.entry_start.grid(row=1,column=1)
		#
		self.chk_start = ttk.Checkbutton(limitLF)
		self.chk_start_var = StringVar()
		self.chk_start.config(text="start", variable= self.chk_start_var, onvalue= "on" , offvalue = "off", command= self.chek_start)
		self.chk_start.grid(row=1,column = 0, sticky = W)
	#--stop=LIMITSTOP    Last query output entry to retrieve
		self.entry_stop= ttk.Entry(limitLF)
		self.entry_stop.config(text="" , textvariable="", width = 5)
		self.entry_stop.grid(row=2,column=1)
		#
		self.chk_stop = ttk.Checkbutton(limitLF)
		self.chk_stop_var = StringVar()
		self.chk_stop.config(text="stop", variable= self.chk_stop_var, onvalue= "on" , offvalue = "off", command= self.chek_stop)
		self.chk_stop.grid(row=2,column = 0, sticky = W)
	#--first=FIRSTCHAR   First query output word character to retrieve
		charblindLF = ttk.Labelframe(enumerationF, text='For blind')
		charblindLF.grid(row = 0, column = 3, pady=10, padx=10, sticky='w')
		#
		self.entry_first= ttk.Entry(charblindLF)
		self.entry_first.config(text="" , textvariable="", width = 5)
		self.entry_first.grid(row=0,column=1)
		#
		self.chk_first = ttk.Checkbutton(charblindLF)
		self.chk_first_var = StringVar()
		self.chk_first.config(text="first", variable= self.chk_first_var, onvalue= "on" , offvalue = "off", command= self.chek_first)
		self.chk_first.grid(row=0,column = 0)
	#--last=LASTCHAR     Last query output word character to retrieve
		self.entry_last= ttk.Entry(charblindLF)
		self.entry_last.config(text="" , textvariable="", width = 5)
		self.entry_last.grid(row=1,column=1)
		#
		self.chk_last = ttk.Checkbutton(charblindLF)
		self.chk_last_var = StringVar()
		self.chk_last.config(text="last", variable= self.chk_last_var, onvalue= "on" , offvalue = "off", command= self.chek_last)
		self.chk_last.grid(row=1,column = 0)
## end rare1

	#--file-read:
		filereadLF = ttk.Labelframe(fileF, text='File read:')
		filereadLF.grid(sticky='we', ipady=3)
		filereadLF.columnconfigure(0, weight=1)
		#
		self.entryFile_read = ttk.Entry(filereadLF)
		self.entryFile_read.grid(row=0,column=0, sticky='we', padx=30)
		self.entryFile_read.bind('<Button-3>',self.rClicker, add='')
		#
		self.chkFile_read = ttk.Checkbutton(filereadLF)
		self.chkFile_read_var = StringVar()
		self.chkFile_read.config(text="", variable= self.chkFile_read_var, onvalue= "on" , offvalue = "off", command= self.chekFile_read)
		self.chkFile_read.grid(row=0,column=0,sticky = 'w')
		#
		self.viewfile_read = ttk.Button(fileF)
		self.viewfile_read.config(text ="view in Watch log", command=self.vfile)
		self.viewfile_read.grid(row =0, column=1,sticky='es')



#Default *log,*config
		configDL = ttk.Panedwindow(fileF, orient=HORIZONTAL, width=100, height=240)
		configDL.rowconfigure( 0, weight=1 )
		configDL.columnconfigure( 0, weight=1)
		#
		catLF = ttk.Labelframe(configDL, text='Category')
		catLF.rowconfigure( 0, weight=1 )
		catLF.columnconfigure( 0, weight=1 )
		#
		listLF = ttk.Labelframe(configDL, text='Default *log, *config')
		listLF.rowconfigure( 0, weight=1 )
		listLF.columnconfigure( 0, weight=1 )
		#
		configDL.add(catLF)
		configDL.add(listLF)
		configDL.grid(row=1,columnspan=2, sticky='we', pady=5)
		#Category ./cfg_dir/*.txt
		self.Lcat = Listbox(catLF,height=100,width=20,selectmode=EXTENDED)
		files_cat = os.listdir('./cfg_dir')
		cats = filter(lambda x: x.endswith('.txt'), files_cat)
		for cat_list in cats:
			cat_list = cat_list.replace('.txt', '')
			self.Lcat.insert(END, cat_list)
		self.Lcat.grid(row =0, column = 0)
		self.Lcat.bind("<Double-Button-1>", self.show_def_log)
		# Scroll
		scrollcat = ttk.Scrollbar(catLF, orient=VERTICAL, command=self.Lcat.yview)
		self.Lcat['yscrollcommand'] = scrollcat.set
		scrollcat.grid(row=0,column=1, sticky='ns')
		#Show Default *log, *config
		s_def_log = ttk.Scrollbar(listLF)
		s_def_log.grid(row=0, column=1, sticky='ns')
		#
		self.d_log_TXT = Text(listLF, yscrollcommand=s_def_log.set, width = 73, height=50,bg='black', fg='#99E335')
		s_def_log.config(command= self.d_log_TXT.yview)
		self.d_log_TXT.grid(row=0, column=0,ipadx=30,sticky='nswe')
		self.d_log_TXT.bind('<Button-3>',self.rClicker, add='')

	# ####################################################
	#Func:
	# ####################################################
	def show_def_log(self, *args):
		load_d_log = self.Lcat.curselection()
		self.d_log_TXT.delete("1.0",END)
		if 1 == len(load_d_log):
			file_d_log = ','.join([self.Lcat.get(ind) for ind in load_d_log])
			self.d_log_TXT.insert(END, open(r'./cfg_dir/'+file_d_log+'.txt', 'r').read())
			self.d_log_TXT.mark_set(INSERT, '1.0')
			self.d_log_TXT.focus()
		else:
			self.d_log_TXT.insert(END, u"Default-Log-File-Empty.")

	def vfile(self):
		load_file = self.entryFile_read.get()
		load_url = self.urlentry.get()
		self.sesTXT.delete("1.0",END)
		load_file = load_file.replace("/", "_")
		load_host = urlparse(load_url).netloc
		try:
			log_size = os.path.getsize(""+home+"/.sqlmap/output/"+load_host+"/files/"+load_file)
			if log_size != 0:
				self.sesTXT.insert(END, open(r""+home+"/.sqlmap/output/"+load_host+"/files/"+load_file, 'r').read())
				self.sesTXT.mark_set(INSERT, '1.0')
				self.sesTXT.focus()
			else:
				self.sesTXT.insert(END, u"File-Empty. ")
		except (IOError,OSError):
			self.sesTXT.insert(END, u"File-Not-Found.")
		return
	# file-read
	def chekFile_read(self):
		sqlFile_read = self.chkFile_read_var.get()
		if sqlFile_read == "on" :
			file_read_sql= ' --file-read="'+self.entryFile_read.get()+'"'
		else:
			file_read_sql= ''
		return file_read_sql
	# sql-query
	def chekQuery(self):
		sqlQuery = self.chkQuery_var.get()
		if sqlQuery == "on" :
			query_sql= ' --sql-query="'+self.entryQuery.get()+'"'
		else:
			query_sql= ''
		return query_sql
	# data
	def chekdata(self):
		sqlData = self.chkdata_var.get()
		if sqlData == "on" :
			data_sql= ' --data="'+self.entryData.get()+'"'
		else:
			data_sql= ''
		return data_sql
	# Cookie:
	def chekCook(self):
		sqlCook = self.chkCook_var.get()
		if sqlCook == "on" :
			cook_sql= ' --cookie="'+self.entryCook.get()+'"'
		else:
			cook_sql= ''
		return cook_sql
	# Prefix
	def chekPrefix(self):
		sqlPrefix = self.chkPrefix_var.get()
		if sqlPrefix == "on" :
			prefix_sql= ' --prefix="'+self.entryPrefix.get()+'"'
		else:
			prefix_sql= ''
		return    prefix_sql
	# Suffix
	def chekSuffix(self):
		sqlSuffix = self.chkSuffix_var.get()
		if sqlSuffix == "on" :
			suffix_sql= ' --suffix="'+self.entrySuffix.get()+'"'
		else:
			suffix_sql= ''
		return suffix_sql
	# os
	def chekOS(self):
		sqlOS = self.chkOS_var.get()
		if sqlOS == "on" :
			os_sql= ' --os="'+self.entryOS.get()+'"'
		else:
			os_sql= ''
		return os_sql
	# skip
	def chekSkip(self):
		sqlSkip = self.chkSkip_var.get()
		if sqlSkip == "on" :
			skip_sql= ' --skip="'+self.entrySkip.get()+'"'
		else:
			skip_sql= ''
		return skip_sql
# logic-negative
# wtf! there not this option in sqlmap lol
# prolly mistranslation for --invalid-logical 
	def chekNeg(self):
		sqlNeg = self.chkNeg_var.get()
		if sqlNeg == "on" :
			neg_sql= '  --invalid-logical'
		else:
			neg_sql= ''
		return neg_sql
	# was -b --Banner
	# no-cast
	def chekBanner(self):
		sqlBanner = self.chk_Banner_var.get()
		if sqlBanner == "on" :
			banner_sql= " --no-cast"
		else:
			banner_sql= ''
		return banner_sql		
		
	# string
	def chekStr(self):
		sqlStr = self.chkStr_var.get()
		if sqlStr == "on" :
			str_sql= ' --string="'+self.entryStr.get()+'"'
		else:
			str_sql= ''
		return    str_sql
	# regexp
	def chekReg(self):
		sqlReg = self.chkReg_var.get()
		if sqlReg == "on" :
			reg_sql= ' --regexp="'+self.entryReg.get()+'"'
		else:
			reg_sql= ''
		return reg_sql
	# code
		
	def chekCode(self, *args):
		sqlCode = self.chkCode_var.get()
		if sqlCode == "on" :
			self.boxCode.config(state = 'readonly')
			code_sql = " --code="+self.boxCode_value.get()

		else:
			self.boxCode.config(state = 'disabled')
			code_sql= ''
		return code_sql
		
		

	# uCols
	def chekCol(self):
		sqlCol = self.chkCol_var.get()
		if sqlCol == "on" :
			col_sql= ' --union-cols="'+self.entryCol.get()+'"'
		else:
			col_sql= ''
		return    col_sql
	# uChar
	def chekChar(self):
		sqlChar = self.chkChar_var.get()
		if sqlChar == "on" :
			char_sql= ' --union-char="'+self.entryChar.get()+'"'
		else:
			char_sql= ''
		return char_sql

#	
	def chekSec(self):
		sqlSec = self.chkSec_var.get()
		if sqlSec == "on" :
			sec_sql= ' --time-sec="'+self.entrySec.get()+'"'
		else:
			sec_sql= ''
		return sec_sql
		
##google!
	def chekGoo(self):
		sqlGoo = self.chkGoo_var.get()
		if sqlGoo == "on" :
			goo_sql= ' -g -q="'+self.entryGoo.get()+'"'
		else:
			goo_sql= ''
		return goo_sql		
		
	# -o
	def chekOpt(self):
		sqlOpt = self.chkOpt_var.get()
		if sqlOpt == "on" :
			opt_sql= " -o"
		else:
			opt_sql= ''
		return opt_sql
	#--predict-output
	def chekPred(self):
		sqlPred = self.chkPred_var.get()
		if sqlPred == "on" :
			pred_sql= " --predict-output"
		else:
			pred_sql= ''
		return pred_sql
	#--keep-alive
	def chekKeep(self):
		sqlKeep = self.chkKeep_var.get()
		if sqlKeep == "on" :
			keep_sql= " --keep-alive"
		else:
			keep_sql= ''
		return keep_sql
	#--null-connection
	def chekNull(self):
		sqlNull = self.chkNull_var.get()
		if sqlNull == "on" :
			null_sql= " --null-connection"
		else:
			null_sql= ''
		return null_sql

	# text only
	def chekTxt(self):
		sqlTxt = self.chk_Txt_var.get()
		if sqlTxt == "on" :
			txt_sql= " --text-only"
		else:
			txt_sql= ''
		return txt_sql
	# -Title
	def chekTit(self):
		sqlTit = self.chk_Tit_var.get()
		if sqlTit == "on" :
			tit_sql= " --titles"
		else:
			tit_sql= ''
		return tit_sql


#replaced --batch with --forms cuz its usefull now		
	# --forms
	def chekForms(self):
		sqlForms = self.chk_Forms_var.get()
		if sqlForms == "on" :
			forms_sql= " --forms"
		else:
			forms_sql= ''
		return forms_sql

   #--HEX
	def chekHex(self):
		sqlHex = self.chk_Hex_var.get()
		if sqlHex == "on" :
			hex_sql= " --hex"
		else:
			hex_sql= ''
		return hex_sql


	#-f, --fingerprint
	def chekFing(self):
		sqlFing = self.chk_fing_var.get()
		if sqlFing == "on" :
			fing_sql= " --fingerprint"
		else:
			fing_sql= ''
		return fing_sql

	# DBMS
	def chek_dbms(self, *args):
		sql_dbms = self.chk_dbms_var.get()
		if sql_dbms == "on" :
			self.box.config(state = 'readonly')
			sqlDB = " --dbms="+self.box_value.get()
		else:
			self.box.config(state = 'disabled')
			sqlDB = ""
		return sqlDB
	#-p
	def chekParam(self):
		sqlParam = self.chkParam_var.get()
		if sqlParam == "on" :
			param_sql= ' -p '+self.entryParam.get()
		else:
			param_sql= ''
		return    param_sql
	#Level
	def chek_level(self, *args):
		sql_level= self.chk_level_var.get()
		if sql_level == "on" :
			self.box_level.config(state = 'readonly')
			level_sql = " --level="+self.box_level_value.get()
		else:
			self.box_level.config(state = 'disabled')
			level_sql = ""
		return level_sql
	# Risk
	def chek_risk(self, *args):
		sql_risk= self.chk_risk_var.get()
		if sql_risk == "on" :
			self.box_risk.config(state = 'readonly')
			risk_sql = " --risk="+self.box_risk_value.get()
		else:
			self.box_risk.config(state = 'disabled')
			risk_sql = ""
		return risk_sql
	# VERBOSE LEVEL Func
	def chek_verb(self, *args):
		sql_verb= self.chk_verb_var.get()
		if sql_verb == "on" :
			self.box_verb.config(state = 'readonly')
			#some reason this does not work with a space
			verb_sql = " -v"+self.box_verb_value.get()
		else:
			self.box_verb.config(state = 'disabled')
			verb_sql = ""
		return verb_sql
	# Threads chek_thr
	def chek_thr(self, *args):
		sql_thr= self.chk_thr_var.get()
		if sql_thr == "on" :
			self.thr.config(state = 'normal')
			thr_sql = ' --threads="'+self.thr_value.get()+'"'
		else:
			self.thr.config(state = 'disabled')
			thr_sql = ""
		return thr_sql
	# Tec
	def chek_tech(self, *args):
		sql_tech= self.chk_tech_var.get()
		if sql_tech == "on" :
			self.boxInj.config(state = 'normal')
			tech_sql= " --technique="+self.boxInj_value.get()
		else:
			self.boxInj.config(state = 'disabled')
			tech_sql = ""
		return tech_sql
	# tamper
	def chek_tam(self, *args):
		sel = self.Ltamper.curselection()
		if 0 < len(sel):
			tam_sql= " --tamper "+'"'+','.join([self.Ltamper.get(x) for x in sel])+'"'
		else:
			tam_sql = ""
		return tam_sql

# log viewer
	def sqlmap(self, *args):
		load_url = self.urlentry.get()
		load_host = urlparse(load_url).netloc
		text = open(r""+home+"/.sqlmap/output/"+load_host+"/log", 'r').readlines()
		pattern = re.compile(r'(?m)(^sqlmap(.*)|^---$|^Place:(.*)|^Parameter:(.*)|\s{4,}Type:(.*)|\s{4,}Title:(.*)|\s{4,}Payload:(.*)|\s{4,}Vector:(.*))$', re.DOTALL)
		mode = os.O_CREAT | os.O_TRUNC
		f = os.open(r""+home+"/.sqlmap/output/"+load_host+"/gui_log", mode)
		os.close(f)
		for x in text:
			qq = pattern.sub('', x).strip("\n")
			if len(qq) > 4:
				mode = os.O_WRONLY | os.O_APPEND
				f = os.open(r""+home+"/.sqlmap/output/"+load_host+"/gui_log", mode)
				os.write(f,qq+'\n')
				os.close(f)
#				os.remove(r"./output/"+load_host+"/gui_log")


# load log whitout query
	def logs(self, *args):
		load_url = self.urlentry.get()
		load_host = urlparse(load_url).netloc
		self.sesTXT.delete("1.0",END)
		# highlight it
		s = ['web application technology:','back-end DBMS:','available databases', 'Database:', 'Table:', 'tables', 'columns', 'database management system users', '*', 'files saved to' ]
		try:
			log_size = os.path.getsize(""+home+"/.sqlmap/output/"+load_host+"/log")
			if log_size != 0:
				self.sqlmap()
				self.sesTXT.insert(END, open(r""+home+"/.sqlmap/output/"+load_host+"/gui_log", 'r').read())
				self.sesTXT.mark_set(INSERT, '1.0')
				for tagz in s:
					idx = '1.0'
					while 1:
						idx = self.sesTXT.search(tagz, idx, nocase=1, stopindex=END)
						if not idx: break
						lastidx = '%s+%dc' % (idx, len(tagz))
						self.sesTXT.tag_add('found', idx, lastidx)
						idx = lastidx
						self.sesTXT.tag_config('found', foreground='red')
						self.sesTXT.focus()
			else:
				self.sesTXT.insert(END, u"Log Empty "+load_host+".")
		except (IOError,OSError):
			self.sesTXT.insert(END, u"Log Not Found "+load_host+".")
		return

#
	def session(self):
		load_url = self.urlentry.get()
		load_host = urlparse(load_url).netloc
		self.sesTXT.delete("1.0",END)
		s = ['available databases', 'Database:', 'Table:', '[', ']', '|' ]
		try:
			session_size = os.path.getsize(""+home+"/.sqlmap/output/"+load_host+"/session")
			if session_size != 0:
				self.sesTXT.insert(END, open(r""+home+"/.sqlmap/output/"+load_host+"/session", 'r').read())
				self.sesTXT.mark_set(INSERT, '1.0')
				self.sesTXT.focus()
			else:
				self.sesTXT.insert(END, u"Session-File Empty "+load_host+".")
		except (IOError,OSError):
			self.sesTXT.insert(END, u"Session-File Not Found "+load_host+".")
		return

###
	def fuck(self):
		load_url = self.urlentry.get()
		load_host = urlparse(load_url).netloc
		self.sesTXT.delete("1.0",END)
		try:
			fuck_size = os.path.getsize(""+home+"/.sqlmap/output/"+load_host+"/dump")
			if fuck_size != 0:
				self.sesTXT.insert(END, open(r""+home+"/.sqlmap/output/"+load_host+"/dump", 'r').read())
				self.sesTXT.mark_set(INSERT, '1.0')
				self.sesTXT.focus()
			else:
				self.sesTXT.insert(END, u"Dump Empty "+load_host+"/dump/")
		except (IOError,OSError):
			self.sesTXT.insert(END, u"Dump Not Found "+load_host+"/dump/")
			os.remove(r""+home+"/.sqlmap/output/"+load_host+"/gui_log")
		return
###########
	def target(self):
		load_url = self.urlentry.get()
		load_host = urlparse(load_url).netloc
		self.sesTXT.delete("1.0",END)
		s = ['available databases', 'Database:', 'GET', '[', ']', '|' ]
		try:
			target_size = os.path.getsize(""+home+"/.sqlmap/output/"+load_host+"/target.txt")
			if target_size != 0:
				self.sesTXT.insert(END, open(r""+home+"/.sqlmap/output/"+load_host+"/target.txt", 'r').read())
				self.sesTXT.mark_set(INSERT, '1.0')
				self.sesTXT.focus()
			else:
				self.sesTXT.insert(END, u"Target-File-Empty "+load_host+".")
		except (IOError,OSError):
			self.sesTXT.insert(END, u"Target-File-Not-Found "+load_host+".")
		return
#############
#funkin functs  Os_shell
	# OS Shell
	def chekOs_shell(self):
		sqlOs_shell = self.chkOs_shell_var.get()
		if sqlOs_shell == "on" :
			os_shell_sql= ' --os-shell'
		else:
			os_shell_sql= ''
		return os_shell_sql

	# OS Command
	def chekOs_cmd(self):
		sqlOs_cmd = self.chkOs_cmd_var.get()
		if sqlOs_cmd == "on" :
			os_cmd_sql= ' --os-cmd="'+self.entryOs_cmd.get()+'"'
		else:
			os_cmd_sql= ''
		return os_cmd_sql
	# Privelege escelation
	def chekPriv_esc(self):
		sqlPriv_esc = self.chkPriv_esc_var.get()
		if sqlPriv_esc == "on" :
			priv_esc_sql= ' --priv-esc'
		else:
			priv_esc_sql= ''
		return priv_esc_sql
		
	# OS pwn
	def chekOs_pwn(self):
		sqlOs_pwn = self.chkOs_pwn_var.get()
		if sqlOs_pwn == "on" :
			os_pwn_sql= ' --os-pwn'
		else:
			os_pwn_sql= ''
		return os_pwn_sql

	# msfpath	
	def chekMsf_path(self):
		sqlMsf_path = self.chkMsf_path_var.get()
		if sqlMsf_path == "on" :
			msf_path_sql= ' --msf-path="'+self.entryMsf_path.get()+'"'
		else:
			msf_path_sql= ''
		return msf_path_sql			
	# tmppath	
	def chekTmp_path(self):
		sqlTmp_path = self.chkTmp_path_var.get()
		if sqlTmp_path == "on" :
			tmp_path_sql= ' --tmp-path="'+self.entryTmp_path.get()+'"'
		else:
			tmp_path_sql= ''
		return tmp_path_sql	
		


	# cur-t user
	def chekCurrent_user(self):
		sqlCurrent_user = self.chkCurrent_user_var.get()
		if sqlCurrent_user == "on" :
			current_user_sql= ' --current-user'
		else:
			current_user_sql= ''
		return current_user_sql
	# current db:
	def chekCurrent_db(self):
		sqlCurrent_db = self.chkCurrent_db_var.get()
		if sqlCurrent_db == "on" :
			current_db_sql= ' --current-db'
		else:
				current_db_sql= ''
		return current_db_sql
	#was dba
	# all
	def chek_is_dba(self):
		sql_is_dba = self.chk_is_dba_var.get()
		if sql_is_dba == "on" :
			is_dba_sql= ' --all'
		else:
			is_dba_sql= ''
		return is_dba_sql
	# users
	def chek_users(self):
		sql_users = self.chk_users_var.get()
		if sql_users == "on" :
			users_sql= ' --users'
		else:
			users_sql= ''
		return users_sql
	# passwords
	def chek_passwords(self):
		sql_passwords = self.chk_passwords_var.get()
		if sql_passwords == "on" :
			passwords_sql= ' --passwords'
		else:
			passwords_sql= ''
		return passwords_sql
	# was priv
	# sql-shell
	def chek_privileges(self):
		sql_privileges = self.chk_privileges_var.get()
		if sql_privileges == "on" :
			privileges_sql= ' --sql-shell'
		else:
			privileges_sql= ''
		return privileges_sql
	# roles
	def chek_roles(self):
		sql_roles = self.chk_roles_var.get()
		if sql_roles == "on" :
			roles_sql= ' --roles'
		else:
			roles_sql= ''
		return roles_sql
	# dbs
	def chek_dbs(self):
		sql_dbs = self.chk_dbs_var.get()
		if sql_dbs == "on" :
			dbs_sql= ' --dbs'
		else:
			dbs_sql= ''
		return dbs_sql
	# tables
	def chek_tables(self):
		sql_tables = self.chk_tables_var.get()
		if sql_tables == "on" :
			tables_sql= ' --tables'
		else:
			tables_sql= ''
		return tables_sql
	# columns
	def chek_columns(self):
		sql_columns = self.chk_columns_var.get()
		if sql_columns == "on" :
			columns_sql= ' --columns'
		else:
			columns_sql= ''
		return columns_sql
	# schema
	def chek_schema(self):
		sql_schema = self.chk_schema_var.get()
		if sql_schema == "on" :
			schema_sql= ' --schema'
		else:
			schema_sql= ''
		return schema_sql
	# count
	def chek_count(self):
		sql_count = self.chk_count_var.get()
		if sql_count == "on" :
			count_sql= ' --count'
		else:
			count_sql= ''
		return count_sql
	# dump
	def chek_dump(self):
		sql_dump = self.chk_dump_var.get()
		if sql_dump == "on" :
			dump_sql= ' --dump'
		else:
			dump_sql= ''
		return dump_sql
		
#!!! wtf is this option?	
	# --target
	def chek_target(self):
		sql_target = self.chk_target_var.get()
		if sql_target == "on" :
			target_sql= ' --target'
		else:
			dump_sql= ''
		return dump_sql
	# dump-all
	def chek_dump_all(self):
		sql_dump_all = self.chk_dump_all_var.get()
		if sql_dump_all == "on" :
			dump_all_sql= ' --dump-all'
		else:
			dump_all_sql= ''
		return dump_all_sql
	# exclude-sysdbs
	def chek_exclude(self):
		sql_exclude = self.chk_exclude_var.get()
		if sql_exclude == "on" :
			exclude_sql= ' --exclude-sysdbs'
		else:
			exclude_sql= ''
		return exclude_sql
	# search
	def chek_search(self):
		sql_search = self.chk_search_var.get()
		if sql_search == "on" :
			search_sql= ' --search'
		else:
			search_sql= ''
		return search_sql
	# D DBS
	def chekD(self):
		sqlD = self.chkD_var.get()
		if sqlD == "on" :
			D_sql= ' -D "'+self.entryD.get()+'"'
		else:
			D_sql= ''
		return    D_sql
	# T TBL
	def chekT(self):
		sqlT = self.chkT_var.get()
		if sqlT == "on" :
			T_sql= ' -T "'+self.entryT.get()+'"'
		else:
			T_sql= ''
		return    T_sql
	# C COL
	def chekC(self):
		sqlC = self.chkC_var.get()
		if sqlC == "on" :
			C_sql= ' -C "'+self.entryC.get()+'"'
		else:
			C_sql= ''
		return    C_sql

#rare1 = these are rarely used in sqlmap
	# start limit
	def chek_start(self):
		sql_start= self.chk_start_var.get()
		if sql_start == "on" :
			start_sql= ' --start="'+self.entry_start.get()+'"'
		else:
			start_sql= ''
		return start_sql
	# stop limit
	def chek_stop(self):
		sql_stop= self.chk_stop_var.get()
		if sql_stop == "on" :
			stop_sql= ' --stop="'+self.entry_stop.get()+'"'
		else:
			stop_sql= ''
		return stop_sql
	# first limit
	def chek_first(self):
		sql_first= self.chk_first_var.get()
		if sql_first == "on" :
			first_sql= ' --first="'+self.entry_first.get()+'"'
		else:
			first_sql= ''
		return first_sql
	# last limit
	def chek_last(self):
		sql_last = self.chk_last_var.get()
		if sql_last == "on" :
			last_sql= ' --last="'+self.entry_last.get()+'"'
		else:
			last_sql= ''
		return last_sql
#end rare1




# sqlmap:
	def commands(self):
		target = ' -u "'+self.urlentry.get()+'"'
		z_param = ' --random-agent'
		inject = target+self.chekParam()+z_param+self.chek_tam()+ \
		        self.chekFile_read()+self.chekQuery()+self.chekdata()+ \
		        self.chek_level()+self.chek_risk()+self.chekTit()+self.chekHex()+ \
		        self.chekTxt()+self.chekCode()+self.chekReg()+self.chekStr()+ \
		        self.chekSec()+self.chek_tech()+self.chekOpt()+self.chekPred()+ \
		        self.chekGoo()+self.chekOs_shell()+self.chekOs_cmd()+self.chekPriv_esc()+ \
		        self.chekMsf_path()+self.chekTmp_path()+self.chekOs_pwn()+ \
		        self.chekKeep()+self.chekNull()+self.chek_thr()+self.chek_dbms()+ \
		        self.chekCol()+self.chekChar()+self.chekCook()+self.chekPrefix()+ \
		        self.chekSuffix()+self.chekOS()+self.chekSkip()+ self.chekNeg()+ \
		        self.chekForms()+self.chekCurrent_user()+self.chekCurrent_db()+ \
		        self.chek_is_dba()+self.chek_users()+self.chek_passwords()+ \
		        self.chek_privileges()+self.chek_roles()+self.chek_dbs()+ \
		        self.chek_tables()+self.chek_columns()+self.chek_schema()+ \
		        self.chek_count()+self.chek_dump()+self.chek_dump_all()+ \
		        self.chek_search()+self.chekD()+self.chekT()+self.chekC()+ \
		        self.chek_exclude()+self.chek_start()+self.chek_stop()+ \
		        self.chek_first()+self.chek_last()+self.chek_verb()+ \
		        self.chekFing()+self.chekBanner()
		self.sql_var.set(inject)
# GOGO!!!
# we execute here
	def injectIT(self):
		if (os.name == "posix"):
#   			cmd = "x-terminal-emulator -H -e ./sqlmap.py" + self.sqlEdit.get()
#			cmd = "lxterm -hold -e ./sqlmap.py" + self.sqlEdit.get()
			cmd = "/usr/bin/xterm -hold -e sqlmap" + self.sqlEdit.get()
		else:
#whoa windoez, do you has python Win32?
			cmd = "start cmd /k sqlmap" + self.sqlEdit.get()
	
	#Write last target
		#mode = os.O_TRUNC | os.O_WRONLY
		# bah! want to write every url!!!
#fuckyes finally append
		mode = os.O_CREAT | os.O_WRONLY | os.O_APPEND
		fwr = os.open(r""+home+"/.sqlmap/sqlmapgui.log", mode)
#fuckyes finally newline
		os.write(fwr,"\n" + self.urlentry.get())
		os.close(fwr)
		subprocess.Popen(cmd, shell = True)

# CopyPasteCut function
	def rClicker(self, e):
		try:
			def rClick_Copy(e, apnd=0):
				e.widget.event_generate('<Control-c>')

			def rClick_Cut(e):
				e.widget.event_generate('<Control-x>')

			def rClick_Paste(e):
				e.widget.event_generate('<Control-v>')

			e.widget.focus()
			nclst=[
				(' Cut', lambda e=e: rClick_Cut(e)),
				(' Copy', lambda e=e: rClick_Copy(e)),
				(' Paste', lambda e=e: rClick_Paste(e)),
				]
			rmenu = Menu(None, tearoff=0, takefocus=0)

			for (txt, cmd) in nclst:
				rmenu.add_command(label=txt, command=cmd)

			rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
		except TclError:
			pass
		return "break"

	def rClickbinder(self):
		try:
			for b in [ 'Text', 'Entry', 'Listbox', 'Label']:
				self.bind_class(b, sequence='<Button-3>', func = self.rClicker, add='')
		except TclError:
			pass
#-----------------------------------------
def main():
	root = Tk()
	s = ttk.Style()
	s.theme_use('default')
	root.title('SQLmap GUI v1.82 - for VATB-ng')
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	appl = app(mw=root)
	appl.mainloop()
#-----------------------------------------
if __name__ == '__main__':
	main()
