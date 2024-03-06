import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Collector2.Collector2 import *

import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified

class Main:
	def collector2(self):
		self.Collector2=Collector2(engine=self.engine,parent=self)

	def __init__(self,engine,tables,error_log):
		self.ExtractPkg=ExtractPkg
		self.DayLogger=DayLogger
		self.Lookup=Lookup
		self.engine=engine
		self.tables=tables
		self.error_log=error_log
		self.unified=lambda line,self=self:unified.Unified.unified(self,line=line)
		self.modes={
		'1':{
		'cmds':['collect','1','item'],
		'exec':self.startCollectItemMode,
		'desc':'use to collect item data rapidly'
		},
		'1.1':{
		'cmds':['collect2','11','c2l_sep',],
		'exec':self.collector2,
		'desc':'collect barcode/itemcode pairs for later export separate of Entry Table'
		},
		'2':{
		'cmds':['list','2','+/-','cnt','count'],
		'exec':self.startListMode,
		'desc':"use as a list maker",
		},
		'3':{
		'cmds':['quit','q','3','e'],
		'exec':lambda self=self:exit("User Quit!"),
		'desc':"exit program"
		},
		'4':{
		'cmds':['import','system_import','si','4'],
		'exec':lambda self=self:self.ExtractPkg(tbl=self.tables,engine=self.engine,error_log=self.error_log),
		'desc':"Import Codes from MobileInventory Pro Backup File with *.bck"
		},
		'5':{
		'cmds':['lu','5','lookup','search'],
		'exec':lambda self=self:self.Lookup(engine=engine,tbl=self.tables),
		
		'desc':"Lookup product info!",
			},
		'6':{
		'cmds':['dl','6','daylog',],
		'exec':lambda self=self:self.DayLogger(engine=engine),
		
		'desc':"create a product tracking log for the current date!",
			},
		'7':{
		'cmds':['convert','7','cnvt',],
		'exec':lambda self=self:ConvertCode(),
		
		'desc':"convert codes upce2upca also creates a saved img!",
			},
		'8':{
		'cmds':['setCode','8','setcd',],
		'exec':lambda self=self:SetCode(engine=engine),
		
		'desc':"convert codes upce2upca also creates a saved img!",
			},
			'9':{
		'cmds':['shelf_locator','9','shelf_locator','shf_lct'],
		'exec':lambda self=self:Locator(engine=engine),
		
		'desc':"find shelf location using barcode to shelf tag code",
			},
			'10':{
		'cmds':['lm2','10','list_mode2'],
		'exec':lambda self=self:ListMode2(engine=engine,parent=self),
		
		'desc':"list mode using only one code input!",
			},
		'11':{
		'cmds':['codeLocator_nf','locator_nf','geo_nf','loc_nf','cl_nf','lbl2shlf_nf','lbl2tg_nf'],
		'exec':lambda:pc.run(),
		
		'desc':"find shelf code from scanned code without searching for Location Field!",
			},
        '12':{
		'cmds':['tasks','t','job'],
        'exec':lambda self=self:TasksMode(engine=engine,parent=self),
		
		'desc':"job related tasks!",
			}

		}
		#
		self.modeString=''.join([f"{Fore.cyan}{self.modes[i]['cmds']} - {self.modes[i]['desc']}{Style.reset}\n" for i in self.modes])
		while True:
			self.currentMode=input(f"which mode do you want to use \n{self.modeString}: ").lower()
			for k in self.modes:
				if self.currentMode in self.modes[k]['cmds']:
					self.modes[k]['exec']()

	def Unified(self,line):
		try:
			return self.unified(line)
		except Exception as e:
			print(e)
			return False



	upc_other_cmds=False
	code_other_cmds=False
	def startCollectItemMode(self):
		code=''
		barcode=''
		options=['q - quit - 1','2 - b - back','skip','?']
		while True:
			self.upc_other_cmds=False
			self.code_other_cmds=False
			while True:
				fail=False
				upce=''
				barcode=input(f"{Fore.green_yellow}Barcode{Style.reset}{options}{Style.bold}\n: ")
				print(f"{Style.reset}")
				if barcode.lower() in ['q','quit','1']:
					exit('user quit!')
				elif barcode in ['2','b','back']:
					return
				elif barcode.lower() in ['skip','sk','skp']:
					#barcode='1'*11
					break
				elif barcode.lower() in ['?']:
					self.help()
					self.upc_other_cmds=True
				elif self.Unified(barcode):
					self.upc_other_cmds=True
				elif barcode == '':
					#barcode='0'*11
					break
				else:	
					if len(barcode) == 8:
						try:
							upce=upcean.convert.convert_barcode(intype="upce",outtype="upca",upc=barcode)
						except Exception as e:
							print(e)				
					for num,test in enumerate([UPCA,EAN8,EAN13]):
						try:
							if test == UPCA:
								if len(barcode) >= 11:
									t=test(barcode)	
								elif len(barcode) == 8:
									t=test(upce)
							else:
								t=test(barcode)
								print(t)
							break
						except Exception as e:
							print(e)
							if num >= 3:
								fail=True
				#print("break",fail)
				if fail:
					barcode='0'*11
					break
				else:
					break

			while True:
				fail=False
				code=input(f"{Style.reset}{Fore.green}Code{Style.reset}{options}{Style.bold}\n: ")
				print(f"{Style.reset}")
				if code.lower() in ['q','quit','1']:
					exit('user quit!')
				elif code in ['2','b','back']:
					return
				elif code.lower() in ['skip','sk','skp']:
					#code='1'*8
					break
				elif code.lower() in ['?']:
					self.help()
					self.code_other_cmds=True
				elif self.Unified(code):
					self.code_other_cmds=True
				elif code == '':
					#code='0'*8
					break
				elif code == 'tlm':
					self.listMode=not self.listMode
					print(f"ListMode is now: {Fore.red}{self.listMode}{Style.reset}")
					break
				elif code == 'slm':
					print(f"ListMode is: {Fore.red}{self.listMode}{Style.reset}")
					break
				else:
					fail=False
					for num,test in enumerate([Code39,]):
						try:
							t=test(code,add_checksum=False)
							break
						except Exception as e:
							print(e)
							if num >= 1:
								fail=True
				if fail:
					code='0'*8
					break
				else:
					break
			
			if self.code_other_cmds == False and self.upc_other_cmds == False:
				with Session(self.engine) as session:
					if len(barcode) == 8:
						if code == '#skip':
							try:
								query=session.query(self.tables['Entry']).filter(self.tables['Entry'].barcode.icontains(barcode))
							except Exception as e:
								query=session.query(self.tables['Entry']).filter(self.tables['Entry'].barcode.icontains(upce))
						elif barcode == '#skip':
							query=session.query(self.tables['Entry']).filter(self.tables['Entry'].Code.icontains(upce))
						else:	
							query=session.query(self.tables['Entry']).filter(or_(self.tables['Entry'].Barcode.icontains(barcode),self.tables['Entry'].Code.icontains(code)))

					else:
						print(code,barcode)
						if code in ['#skip','']:
							query=session.query(self.tables['Entry']).filter(self.tables['Entry'].Barcode.icontains(barcode))
						elif barcode == ['#skip','']:
							query=session.query(self.tables['Entry']).filter(self.tables['Entry'].Code.icontains(code))

						else:
							query=session.query(self.tables['Entry']).filter(or_(self.tables['Entry'].Barcode.icontains(barcode),self.tables['Entry'].Code.icontains(code)))
					results=query.all()
					if len(results) < 1:
						print(code)
						print(barcode)
						if (code != '0'*8 and barcode != '0'*11):
							if upce != '':
								entry=self.tables['Entry'](Barcode=upce,Code=barcode,upce2upca=barcode,InList=True)
							else:
								entry=self.tables['Entry'](Barcode=barcode,Code=code,InList=True)
							session.add(entry)
							session.commit()
							session.flush()
							session.refresh(entry)
							print(entry)
					else:
						for num,e in enumerate(results):
							print(f"{Fore.light_red}{num}{Style.reset}->{e}")
						while True:
							msg=input(f"Do you want to edit one? if so enter its {Fore.light_red}entry number{Style.reset}(or {Fore.yellow}-1|q|quit{Style.reset} to {Fore.yellow}quit{Style.reset},{Fore.cyan}-2|b|back{Style.reset} to {Fore.cyan}go back{Style.reset}{Fore.green}[or Hit <Enter>]{Style.reset}): ")
							try:								
								if msg == '':
									if self.listMode and len(results) >=1:
										qty=input("How Much to add? ")
										if qty == '':
											qty=1
										qty=float(qty)
										setattr(results[0],'InList',True)
										setattr(results[0],'ListQty',getattr(results[0],'ListQty')+qty)
										session.commit()
										session.flush()
										session.refresh(results[0])
									break
								if msg.lower() in ['-1','q','quit']:
									exit("user quit!")
								elif msg.lower() in ['-2','b','back']:
									break
								else:
									num=int(msg)
									if num < 0:
										raise Exception("Invalid Id:Hidden CMD!")
									else:
										if self.listMode:
											while True:
												qty=input("How Much to add? ")
												print(qty)
												if qty == '':
													qty=1
												qty=float(qty)
												setattr(results[num],'InList',True)
												setattr(results[num],'ListQty',getattr(results[num],'ListQty')+qty)
												session.commit()
												session.flush()
												session.refresh(results[num])
												break
										else:
											print(results[num])
											self.editEntry(session,results[num])
										break
							except Exception as e:
								print(e)
							#use first result as found as entry and display it while incrementing it
							

	listMode=False
	def editEntry(self,session,item):
		print(session,item)
		for column in item.__table__.columns:
			while True:
				try:
					if column.name not in ['Timestamp','EntryId','Image']:
						new_value=input(f"{column.name}->{getattr(item,column.name)}('n','s','d','q'): ")
						if new_value in ['s','n','']:
							break
						elif new_value in ['#clear_field']:
							if isinstance(column.type,Float):
								new_value=float(0)
							elif isinstance(column.type,Integer):
								new_value=int(0)
							elif str(column.type) == "VARCHAR":
								new_value=''
							elif isinstance(column.type,Boolean):
								setattr(item,column.name,0)
						elif new_value in ['d']:
							session.query(self.tables['Entry']).filter(self.tables['Entry'].EntryId==item.EntryId).delete()
							print(item,"Was Deleted!")
							return
						elif new_value in ['b']:
							return	
						elif new_value in ['q']:
							exit("user quit!")

						if isinstance(column.type,Float):
							new_value=float(new_value)
						elif isinstance(column.type,Integer):
							new_value=int(new_value)
						elif str(column.type) == "VARCHAR":
							pass
						elif isinstance(column.type,Boolean):
							if new_value.lower() in ['true','yes','1','y',]:
								setattr(item,column.name,1)
							else:
								setattr(item,column.name,0)
						if str(column.type) not in ['BOOLEAN',]:
							#exit(str((column.name,column.type,isinstance(column.type,Boolean))))
							setattr(item,column.name,new_value)
							
						session.commit()
					break
				except Exception as e:
					print(e)




	def startListMode(self):
		print(f"{Fore.yellow}List Mode{Style.reset}")
		self.listMode=True
		self.startCollectItemMode()

	def help(self):
		with open(Path(__file__).parent/Path("helpMsg.txt"),"r") as msgr:
			msg=f"""{msgr.read().format(Style=Style,Fore=Fore,Back=Back)}"""
			print(msg)
			return msg

def quikRn():
	Main(engine=ENGINE,tables=tables,error_log=Path("error_log.log"))

if __name__ == "__main__":
	Main(engine=ENGINE,tables=tables,error_log=Path("error_log.log"))
