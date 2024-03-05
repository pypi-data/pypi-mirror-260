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

print("fores")
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExportList.ExportListCurrent import *


import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc

class Unified:
	
	def unified(self,line):
		args=line.split(",")
		#print(args)
		if len(args) > 1:
			if args[0].lower() in ["remove","rm",'del','delete']:
				try:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).delete()
						print(result)
						session.commit()
						session.flush()
				except Exeption as e:
					print(e)
				return True
			elif args[0].lower() in ['smle']:
				if len(args) >= 2:
					if args[1].lower() in ['?','s','search','lu']:
						while True:
							code=input("code|barcode|q/quit|b/back: ")
							if code.lower() in ['q','quit']:
								exit("user quit!")
							elif code.lower() in ['b','back']:
								break
								return True
							else:
								with Session(self.engine) as session:
									result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code),Entry.InList==True).first()
									if result:
										result.listdisplay_extended(num=0)	
									else:
										print(f"{Fore.red}No Such Item by {Style.underline}{code}{Style.reset}")
					else:
						with Session(self.engine) as session:
							result=session.query(Entry).filter(or_(Entry.Barcode==args[1],Entry.Code==args[1]),Entry.InList==True).first()
							if result:
								result.listdisplay_extended(num=0)
							else:
								print(f"{Fore.red}No Such Item by {Style.underline}{args[1]}{Style.reset}")				
				return True
			elif args[0].lower() in ['code_len']:
				while True:
					#scanned=input("code|barcode[q/b]: ")
					if len(args) >= 2:
						scanned=args[1]
						if scanned in ['q','quit']:
							exit("user quit!")
						elif scanned in ['b','back']:
							return True
						else:
							print(f"{Fore.cyan}{scanned}{Style.reset} is {Fore.green}'{len(scanned)}'{Style.reset} characters long!")
						break
				return True
			elif args[0].lower() in ["search","s",'sch']:
				print("Search Mod")
				with Session(self.engine) as session:
					#session.query(Entries).filter
					for field in Entry.__table__.columns:
						if field.name.lower() == args[1].lower():
							print(field)
							if str(field.type) in ['FLOAT','INTEGER']:
								term=0
								if str(field.type) == 'FLOAT':
									term=float(args[2])
								elif str(field.type) == 'INTEGER':
									term=int(args[2])
								operators=['==','!=','<','<=','>','>=','q','b']
								print(f"""
{Fore.yellow}=={Style.reset} -> equal to
{Fore.yellow}=!{Style.reset} -> not equal to
{Fore.yellow}<{Style.reset} -> less than
{Fore.yellow}<={Style.reset} -> less than, or equal to
{Fore.yellow}>{Style.reset} -> greater than
{Fore.yellow}>={Style.reset} -> greater than, or equal to
{Fore.red}q{Style.reset} -> quit
{Fore.red}b{Style.reset} -> back
									""")
								while True:
									operator=input(f"operator {operators}:").lower()
									if operator not in operators:
										continue
									if operator == 'q':
										exit('user quit')
									elif operator == 'b':
										break
									elif operator == '==':
										query=session.query(Entry).filter(field==term)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '!=':
										query=session.query(Entry).filter(field!=term)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '<':
										query=session.query(Entry).filter(field<term)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '<=':
										query=session.query(Entry).filter(field<=term)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '>':
										query=session.query(Entry).filter(field>term)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '>=':
										query=session.query(Entry).filter(field>=term)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
								break
							elif str(field.type) == 'VARCHAR':
								operators=['=','%','q','b','!%','!=']
								print(f"""
 {Fore.yellow}={Style.reset} -> entry in Field is exactly
 {Fore.yellow}!={Style.reset} -> entry is not equal to
 {Fore.yellow}%{Style.reset} -> entry is contained within field but is NOT exact to the total of the field
 {Fore.yellow}!%{Style.reset} -> entry is not contained within field but is NOT exact to the total of the field
 {Fore.red}q{Style.reset} -> quit
 {Fore.red}b{Style.reset} -> back
									""")
								while True:
									operator=input(f"operator {operators}:").lower()
									if operator not in operators:
										continue
									if operator == 'q':
										exit('user quit')
									elif operator == 'b':
										break
									elif operator == '=':
										query=session.query(Entry).filter(field==args[2])
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '!=':
										query=session.query(Entry).filter(field!=args[2])
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '%':
										query=session.query(Entry).filter(field.icontains(args[2]))
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break
									elif operator == '!%':
										query=session.query(Entry).filter(field.icontains(args[2])==False)
										save_results(query)
										results=query.all()
										for num,e in enumerate(results):
											print(f"{Fore.red}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
										print(f"Number of Results: {len(results)}")
										break

								break
							else:
								print(field.type)

				'''args[1] == fieldname'''
				'''args[2] == value to search for'''
				return True
			elif args[0].lower() in ['name','nm']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Name)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")	
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Name',str(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Name)
				return True
			elif args[0].lower() in ['code','cd']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Code)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Code',str(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Code)
				return True
			elif args[0].lower() in ['barcode','bcd','bd']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Barcode)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Barcode',str(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Barcode)
				return True
			elif args[0].lower() in ['note','nt']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Note)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Note',str(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Note)
				return True
			elif args[0].lower() in ['price','pc','prc']:
				if len(args) == 2:

					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Price)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Price',float(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Price)
				return True
			elif args[0].lower() in ['img','im','Image']:
				if len(args) == 2:

					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Image)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						try:
							imtext=str(args[2])
							f=importImage(image_dir=img_dir,src_path=imtext,nname=f'{result.EntryId}.png',ow=True)
							setattr(result,'Image',f)
							
							session.commit()
							session.flush()
							session.refresh(result)
							print(result.Image)
						except Exception as e:
							print("No Such EntryId!")
				return True
			elif args[0].lower() in ['rm_img','rm_im','del_img']:
				try:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						try:
							imtext=result.Image
							removeImage(image_dir=img_dir,img_name=imtext)
							setattr(result,'Image','')
							
							session.commit()
							session.flush()
							session.refresh(result)
							print(result.Image)
						except Exception as e:
							print(e)
							print("No Such EntryId!")
				except Exception as e:
					print(e)
				return True
			elif args[0].lower() in ['size','sz','sze']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Size)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Size',str(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Size)
				return True
			elif args[0].lower() in ['shelf','slf','shf','shlf']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Shelf)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Shelf',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Shelf)
				return True
			elif args[0].lower() in ['backroom','bkrm','br']:
				print("Backroom")
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.BackRoom)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'BackRoom',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.BackRoom)		
				return True
			elif args[0].lower() in ['inlist','il']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.InList)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'InList',bool(int(args[2])))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.InList)		
				return True
			elif args[0].lower() in ['display_1','d1']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_1)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_1',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_1)		
				return True
			elif args[0].lower() in ['display_2','d2']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_2)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_2',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_2)		
				return True
			elif args[0].lower() in ['display_3','d3']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_3)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_3',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_3)	
				return True
			elif args[0].lower() in ['display_4','d4']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_4)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_4',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_4)		
				return True
			elif args[0].lower() in ['display_5','d5']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_5)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_5',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_5)		
				return True
			elif args[0].lower() in ['display_6','d6']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_6)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_6',int(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_6)			
				return True
			elif args[0].lower() in ['inlist','il']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.InList)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'InList',bool(int(args[2])))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.InList)	
				return True
			elif args[0].lower() in ['qty','listQty','lq','lstqty']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.ListQty)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'ListQty',float(args[2]))
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.ListQty)
				return True
				#newbuild	
			elif args[0].lower() in ['location','geo','lctn','ln','l']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(or_(Entry.EntryId==int(args[1]),Entry.Barcode==args[1],Entry.Code==args[1])).first()
							if result:
								print(result.Location)
								if len(result.Barcode) >= 13:
									print(f"{Fore.hot_pink_1b}Detected Code is 13 digits long; please verify the {Style.underline}'EAN13 Stripped $var_x:$var_z'{Style.res_underline} data first before using the UPC Codes!{Style.reset}")
								pc.PossibleCodes(scanned=result.Barcode)
								pc.PossibleCodesEAN13(scanned=result.Barcode)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId/Code/Barcode; below are possible shelf codes for the unkown!{Style.reset}")
								if len(args[1]) >= 13:
									print(f"{Fore.hot_pink_1b}Detected Code is 13 digits long; please verify the 'EAN13 Stripped $var_x=$var_z' data first before using the UPC Codes!{Style.reset}")
								pc.PossibleCodes(scanned=args[1])
								pc.PossibleCodesEAN13(scanned=args[1])

				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Location',args[2])
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Location)
				return True
			elif args[0].lower() in ['upce2upca','u2u','e2a']:
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.upce2upca)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				elif len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'upce2upca',args[2])
						
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.upce2upca)		
				return True
			elif args[0].lower() in ['+','-','=']:
				if len(args) == 3:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(or_(Entry.Barcode==args[2],Entry.Code==args[2])).first()
						if result:
							if args[0] == '-':
								result.ListQty=result.ListQty-float(args[1])
							elif args[0] == '+':
								result.ListQty=result.ListQty+float(args[1])
							elif args[0] == '=':
								result.ListQty=float(args[1])
							result.InList=True
							session.commit()
							session.flush()
							session.refresh(result)
							print(result)		
						else:
							print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					print(f"{Fore.red}[+,-,=]{Style.reset},{Fore.yellow}QTY{Style.reset},{Fore.green}Code/Barcode{Style.reset}")
				return True
			elif args[0].lower() in ["stock_total","st"]:
				with Session(self.engine) as session:
					item=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
					keys=[f'Display_{i}' for i in range(1,7)]
					keys.append('Shelf')
					keys.append('BackRoom')
					print(keys)
					t=0
					for k in keys:
						curr=getattr(item,k)
						if curr:
							t+=curr
						else:
							setattr(item,k,0)
					setattr(item,'Stock_Total',t)
					
					session.commit()
					session.flush()
					session.refresh(item)
					print(item.Stock_Total)
				return True	
			elif args[0].lower() == "show":
				with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).all()
						for num,e in enumerate(result):
							print(num,e)
				return True
		elif args[0].lower() in ["list_all","la"]:
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).all()
					for num,e in enumerate(result):
						print(num,e)
			print("-"*10)
			return True
		elif args[0].lower() in ["show_list","sl",]:
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).filter(Entry.InList==True).all()
					for num,e in enumerate(result):
						print(num,e)
			print("-"*10)
			return True
		elif args[0].lower() in ["clear_list","cl","clrl"]:
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).filter(Entry.InList==True).update({'InList':False,'ListQty':0})
					session.commit()
					session.flush()
					print(result)
			print("-"*10)
			return True
		elif args[0].lower() in ["clear_all","ca","clrall"]:
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).update(
						{'InList':False,
						'ListQty':0,
						'Shelf':0,
						'Note':'',
						'BackRoom':0
						,'Display_1':0,
						'Display_2':0,
						'Display_3':0,
						'Display_4':0,
						'Display_5':0,
						'Display_6':0,
						'Stock_Total':0,
						})
					session.commit()
					session.flush()
					print(result)
			print("-"*10)
			return True
		elif args[0].lower() in ["clear_all_img","cam","clrallimg"]:
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).all()
					for num,item in enumerate(result):
						print(f"{Fore.red}{num} - clearing img field -> {item}")
						if Path(item.Image).exists():
							try:
								if Path(item.Image).is_file():
									Path(item.Image).unlink()
									item.ImagePath=''
									session.commit()
									#session.flush()
									#session.refresh(item)
							except Exception as e:
								item.Image=''
								session.commit()
								#session.flush()
								#session.refresh(item)
						else:
							item.Image=''
							session.commit()
							#session.flush()
							#session.refresh(item)
					session.commit()
					session.flush()
					print(result)
			print("-"*10)
			return True
		elif args[0].lower() in ["save_csv","save","sv"]:
			df=pd.read_sql_table('Entry',self.engine)
			while True:
				try:
					sfile=input(f"{Style.bold}Save Where:{Style.reset} ")
					if sfile == "":
						sfile="./db.csv"
						print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
					if sfile.lower() == 'q':
						exit("user quit!")
					elif sfile.lower() == 'b':
						break
					else:
						df.to_csv(sfile,index=False)
					break
				except Exception as e:
					print(e)
					
			return True
		elif args[0].lower() in ["save_bar","sb","svbr"]:
			df=pd.read_sql_table('Entry',self.engine)
			while True:
				try:
					sfile=input(f"{Style.bold}Save Where:{Style.reset} ")
					if sfile == "":
						sfile="./barcode.csv"
						print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
					if sfile.lower() == 'q':
						exit("user quit!")
					elif sfile.lower() == 'b':
						break
					else:
						df=df['Barcode']
						df.to_csv(sfile,index=False)
					break
				except Exception as e:
					print(e)
					
			return True
		elif args[0].lower() in ["save_bar_cd","sbc","svbrcd"]:
			df=pd.read_sql_table('Entry',self.engine)
			while True:
				try:
					sfile=input(f"{Style.bold}Save Where:{Style.reset} ")
					if sfile == "":
						sfile="./barcode.csv"
						print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
					if sfile.lower() == 'q':
						exit("user quit!")
					elif sfile.lower() == 'b':
						break
					else:
						df=df[['Barcode','Code']]
						df.to_csv(sfile,index=False)
					break
				except Exception as e:
					print(e)
					
			return True
		elif args[0].lower() in ["factory_reset"]:
			#just delete db file and re-generate much simpler
			reInit()
			'''with Session(self.engine) as session:
				done=session.query(Entry).delete()
				session.commit()
				session.flush()
				print(done)'''
			return True
		elif args[0].lower() in ["fields","f","flds"]:
			print("fields in table!")
			for column in Entry.__table__.columns:
				print(column.name)
			return True
		elif args[0].lower() in ['tlm']:
			self.listMode=not self.listMode
			print(f"ListMode is now: {Fore.red}{self.listMode}{Style.reset}")
			return True
		elif args[0].lower() in ['slm']:
			print(f"ListMode is: {Fore.red}{self.listMode}{Style.reset}")
			return True
		elif args[0].lower() in ['sum_list','smzl']:
			with Session(self.engine) as session:
				results=session.query(Entry).filter(Entry.InList==True).all()
				for num,result in enumerate(results):
					result.listdisplay(num=num)
			
			return True
		elif args[0].lower() in ['?','help']:
			self.help()
			return True
		elif args[0].lower() in ['smle']:
					with Session(self.engine) as session:
						results=session.query(Entry).filter(Entry.InList==True).all()
						if len(results) < 1:
							print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
						for num,result in enumerate(results):
							result.listdisplay_extended(num=num)
		elif args[0].lower() in ['smle-e']:
					with Session(self.engine) as session:
						results=session.query(Entry).filter(Entry.InList==True).all()
						if len(results) < 1:
							print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
						for num,result in enumerate(results):
							result.saveListExtended(num=num)
		elif args[0].lower() in ['le-img']:
					with Session(self.engine) as session:
						results=session.query(Entry).filter(Entry.InList==True).all()
						if len(results) < 1:
							print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
						for num,result in enumerate(results):
							result.saveItemData(num=num)
		elif args[0].lower() in ['le-img-bc']:
					with Session(self.engine) as session:
						results=session.query(Entry).filter(Entry.InList==True).all()
						if len(results) < 1:
							print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
						for num,result in enumerate(results):
							print(num)
							result.save_barcode()
		elif args[0].lower() in ['le-img-c']:
					with Session(self.engine) as session:
						results=session.query(Entry).filter(Entry.InList==True).all()
						if len(results) < 1:
							print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
						for num,result in enumerate(results):
							print(num)
							result.save_code()
		elif args[0].lower() in ['clear','reset','screen_reset','#<>?']:
					print(os.system("clear "))
					return True
		elif args[0].lower() in ['backup',]:
					print(f"Backing Files up")
					d=datetime.now().strftime("%m-%d-%Y")
					backup=Path(f"./codesAndBarcodes-{d}.tgz")
					if backup.exists():
						backup.unlink()
					with tarfile.open(backup,"w:gz") as gzf:
						#gzf.add("codesAndBarcodes.db")
						#gzf.add("Images")
						#gzf.add("LCL_IMG")
						dbf=Path("codesAndBarcodes.db")
						if dbf.exists():
							print(f"adding {dbf}")
							gzf.add(dbf)
						imd=Path("Images")
						if imd.exists():
							print(f"adding {imd}")
							gzf.add(imd)
						lclimg=Path("LCL_IMG")
						if lclimg.exists():
							print(f"adding {lclimg}")
							gzf.add(lclimg)
					print(backup)
					return True
		elif args[0].lower() in ['restore',]:
			backup=input("backup file: ")
			backup=Path(backup)
			if backup.exists():
				print("clearing old data...")
				dbf=Path("codesAndBarcodes.db")
				if dbf.exists():
					dbf.unlink()
				imd=Path("Images")
				if imd.exists():
					shutil.rmtree(str(imd))
				lclimg=Path("LCL_IMG")
				if lclimg.exists():
					shutil.rmtree(str(lclimg
						))
				
				with tarfile.open(backup,"r:gz") as gzf:
					gzf.extractall()
			return True
		elif args[0].lower() in ['export_list','el']:
			ExportListCSV(parent=self,engine=self.engine)
		elif args[0].lower() in ['code_len']:
				while True:
					scanned=input("code|barcode[q/b]: ")
					if scanned in ['q','quit']:
						exit("user quit!")
					elif scanned in ['b','back']:
						return True
					else:
						print(f"{Fore.cyan}{scanned}{Style.reset} is {Fore.green}'{len(scanned)}'{Style.reset} characters long!")
					break
				return True
		elif args[0].lower() in ['ni','new_item']:
			while True:
				try:
					data={}
					for column in Entry.__table__.columns:
						value=None
						if column.type in ['FLOAT','INTEGER']:
							if column.type == 'FLOAT':
								value=input("f{column.name}({column.type})[q/b/value/enter to skip]: ")
								if value == '':
									continue
								elif value.lower() in ['b','back']:
									return
								elif value.lower() in ['q','quit']:
									exit("user quit!")
								value=float(value)
							elif column.type == 'INTEGER':
								value=input("f{column.name}({column.type})[q/b/value/enter to skip]: ")
								if value == '':
									continue
								elif value.lower() in ['b','back']:
									return
								elif value.lower() in ['q','quit']:
									exit("user quit!")
								value=int(value)
						else:
							value=input(f"{column.name}({column.type})[q/b/value/enter to skip]: ")
							if value == '':
								continue
							elif value.lower() in ['b','back']:
								return
							elif value.lower() in ['q','quit']:
								exit("user quit!")
						data[column.name]=value
						data['InList']=True
					newEntry=Entry(**data)
					with Session(self.engine) as session:
						session.add(newEntry)
						session.commit()
						session.flush()
						session.refresh(newEntry)
						print(newEntry)
					break
				except Exception as e:
					print(e)
		return False