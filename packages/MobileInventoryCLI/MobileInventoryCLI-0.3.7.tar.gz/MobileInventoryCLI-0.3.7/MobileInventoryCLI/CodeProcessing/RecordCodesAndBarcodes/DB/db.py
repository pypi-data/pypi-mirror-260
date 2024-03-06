import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from datetime import datetime,timedelta
from colored import Fore,Style,Back
from datetime import datetime,timedelta
from pathlib import Path
import pandas as pd
import tarfile,zipfile
import base64
import pint
import qrcode
import barcode
from barcode import UPCA,EAN13,Code39
from qrcode import QRCode
from barcode.writer import ImageWriter
import csv,string,random
import shutil,upcean
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.renderText2Png import *

filename="codesAndBarcodes.db"
DEVMOD=False
if DEVMOD:
    if Path(filename).exists():
        Path(filename).unlink()
dbfile="sqlite:///"+str(filename)
img_dir=Path("Images")
if not img_dir.exists():
    img_dir.mkdir()
print(dbfile)
#import sqlite3
#z=sqlite3.connect(filename)
#print(z)
ENGINE=create_engine(dbfile)
BASE=dbase()
#BASE.prepare(autoload_with=ENGINE)

def reInit(f=None,dbf=None):
    filename="codesAndBarcodes.db"
    dbfile="sqlite:///"+str(filename)
    if f:
        filename=f
    if dbf:
        dbfile=dbf
    if Path(filename).exists():
        Path(filename).unlink()
    ENGINE=create_engine(dbfile)
    Entry.metadata.create_all(ENGINE)
    DayLog.metadata.create_all(ENGINE)
    try:
        img_dir=Path("Images")
        if not img_dir.exists():
            img_dir.mkdir()
        else:
            shutil.rmtree(img_dir)
            img_dir.mkdir()
    except Exception as e:
        print(e)

    exit(f"A {Style.bold}{Style.underline}{Fore.yellow}Factory Reset{Style.reset} was performed. A {Style.bold}{Style.underline}{Fore.yellow}Restart{Style.reset} is {Style.bold}{Style.underline}{Fore.yellow}Required{Style.reset}.")


def removeImage(image_dir,img_name):
    try:
        if img_name != '':
            im=Path(image_dir)/Path(img_name)
            if im.exists():
                im.unlink()
                print(f"{im} removed from FS!")
    except Exception as e:
        print(e)

def importImage(image_dir,src_path,nname=None,ow=False):
    try:
        if not Path(image_dir).exists():
            Path(image_dir).mkdir()
        if not nname:
            dest=Path(image_dir)/Path(Path(src_path).name)
        else:
            dest=Path(image_dir)/Path(nname)
        if not ow and dest.exists():
            raise Exception(f'exists {dest}')
        if not Path(src_path).exists():
            raise Exception (f'src {src_path} does not exist!')
        size=Path(src_path). stat().st_size
        with dest.open('wb') as out, Path(src_path).open('rb') as ifile:
            while True:
                d=ifile.read(1024*1024)
                print(f'writing {len(d)} - {ifile.tell()}/{size}')
                if not d:
                    break
                out.write(d)
        return str(dest)
    except Exception as e:
        print(e)
        return ''

def save_results(query):
    while True:
        save_results=input(f"Save Results {Fore.cyan}y{Style.reset}|{Fore.yellow}N{Style.reset}] : ")
        if save_results.lower() in ['n','no']:
            return
        elif save_results.lower() in ['y','yes']:
            df = pd.read_sql(query.statement, query.session.bind,dtype=str)
            while True:
                saveTo=input("save to: ")
                print(f"Saving to '{Path(saveTo)}'!")
                if Path(saveTo).parent.exists():
                    df.to_csv(saveTo,index=False)
                    return
                print(Path(saveTo))
        else:
            print("Invalid Entry!")
class PairCollection(BASE):
    __tablename__="PairCollection"
    Barcode=Column(String)
    Code=Column(String)
    PairCollectionId=Column(Integer,primary_key=True)
    Name=Column(String)

    def __init__(self,Barcode,Code,Name='',PairCollectionId=None):
        if PairCollectionId:
            self.PairCollectionId=PairCollectionId
        self.Name=Name
        self.Barcode=Barcode
        self.Code=Code

    def __repr__(self):
        msg=f'''PairCollection(
            Barcode='{self.Barcode}',
            Code='{self.Code}',
            Name='{self.Name}',
            PairCollectionId={self.PairCollectionId},
        )'''
        return msg

    def __str__(self):
        msg=f'''PairCollection(
            {Fore.green}Barcode='{self.Barcode}',{Style.reset}
            {Fore.green_yellow}Code='{self.Code}',{Style.reset}
            {Fore.dark_goldenrod}Name='{self.Name}',{Style.reset}
            {Fore.yellow}PairCollectionId={self.PairCollectionId},{Style.reset}
        )'''
        return msg
    LCL=Path("LCL_IMG")
    LCL_ANDROID=Path("/storage/emulated/0/DCIM/Screenshots")

    def save_code(self):
        filename=Path(f"{self.PairCollectionId}_code.png")
        if self.LCL_ANDROID.exists():
            filename=str(self.LCL_ANDROID/filename)
        else:
            filename=str(self.LCL/filename)
        print(filename)
        try:
            codes=[Code39,QRCode]
            for code in codes:
                try:
                    if code == QRCode:
                        qrcode.make(self.Code).save(filename)
                        break
                    else:
                        code(self.Code,add_checksum=False,writer=ImageWriter()).write(filename)
                        break
                    pass
                except Exception as e:
                    print(e)


            return filename
        except Exception as e:
            print(e)
        return False

    def save_barcode(self):
        filename=Path(f"{self.PairCollectionId}_barcode.png")
        if self.LCL_ANDROID.exists():
            filename=str(self.LCL_ANDROID/filename)
        else:
            filename=str(self.LCL/filename)
        print(filename)
        try:
            codes=[UPCA,EAN13,QRCode]
            for code in codes:
                try:
                    if code == QRCode:
                        qrcode.make(self.Barcode).save(filename)
                        break
                    else:
                        if len(self.Barcode) <= 8 and code == UPCA:
                            upca=upcean.convert.convert_barcode_from_upce_to_upca(self.Barcode)
                            if upca != False:
                                code(upca,writer=ImageWriter()).write(filename)
                            else:
                                continue
                        elif len(self.Barcode) > 12:
                            if code == EAN13:
                                code(self.Barcode,writer=ImageWriter()).write(filename)
                            else:
                                continue
                        else:
                            code(self.Barcode,writer=ImageWriter()).write(filename)
                        break
                except Exception as e:
                    print(e)
            return filename


        except Exception as e:
            print(e)
        return False

    def saveItemData(self,num=None):
        if self.LCL_ANDROID.exists():
            self.LCL=self.LCL_ANDROID
        text=[]
        for column in self.__table__.columns:
            text.append('='.join([column.name,str(self.__dict__[column.name])]))
        data='\n'.join(text)
        #LCL=Path("LCL_IMG")
        if not self.LCL.exists():
            self.LCL.mkdir()
        fname=str(self.LCL/Path(str(self.PairCollectionId)))
        n=self.save_barcode()
        c=self.save_code()
        print(n,c)
        renderImageFromText(fname,data,barcode_file=n,code_file=c)

    def listdisplay(self,num=None):
        name=self.Name
        ma=32
        n=self.split_by_len(name,ma)
        #print(n)
        new=[]
        for i in n:
            if n.index(i) > 0:
                new.append(i)
            else:
                new.append(i)
        name='\n'.join(new)
        name="\n"+name
        if num == None:
            num=''
        msg=f'''{Fore.magenta}{Fore.dark_goldenrod}{num}->({Style.reset} NAME={Fore.cyan}{name}{Style.reset} | UPC={Fore.green}{self.Barcode}{Style.reset} | CODE={Fore.yellow}{self.Code}{Style.reset} |{self.PairCollectionId}{Style.reset}{Fore.magenta} )-<{Fore.dark_goldenrod}{num}{Style.reset}'''
        print(msg)
    def split_by_len(self,string, length):
        result = []
        for i in range(0, len(string), length):
            result.append(string[i:i + length])
        return result

class Entry(BASE):
    __tablename__="Entry"
    Code=Column(String)
    Barcode=Column(String)
    #not found in prompt requested by
    '''
    #name {Entryid}
    #name {Entryid} {new_value}
    
    #price {Entryid}
    #price {Entryid} {new_value}

    #note {Entryid}
    #note {Entryid} {new_value}
    
    #size {Entryid} 
    #size {Entryid} {new_value}
    '''
    Name=Column(String)
    Price=Column(Float)
    Note=Column(String)
    Size=Column(String)
    
    CaseCount=Column(Integer)

    Shelf=Column(Integer)
    BackRoom=Column(Integer)
    Display_1=Column(Integer)
    Display_2=Column(Integer)
    Display_3=Column(Integer)
    Display_4=Column(Integer)
    Display_5=Column(Integer)
    Display_6=Column(Integer)
    InList=Column(Boolean)
    Stock_Total=Column(Integer)
    Location=Column(String)
    ListQty=Column(Float)
    upce2upca=Column(String)
    Image=Column(String)
    EntryId=Column(Integer,primary_key=True)
    Timestamp=Column(Float)

    ALT_Barcode=Column(String)
    DUP_Barcode=Column(String)
    CaseID_BR=Column(String)
    CaseID_LD=Column(String)
    CaseID_6W=Column(String)
    Tags=Column(String)
    Facings=Column(Integer)
    SBX_WTR_DSPLY=Column(Integer)
    SBX_CHP_DSPLY=Column(Integer)
    SBX_WTR_KLR=Column(Integer)
    FLRL_CHP_DSPLY=Column(Integer)
    FLRL_WTR_DSPLY=Column(Integer)
    WD_DSPLY=WD_DSPLY=Column(Integer)
    CHKSTND_SPLY=CHKSTND_SPLY=Column(Integer)
    def csv_headers(self):
        headers=[]
        for i in self.__table__.columns:
            headers.append(i.name)
        headers.append("DateFromTimeStamp")
        return headers

    def csv_values(self):
        values=[]
        for i in self.__table__.columns:
            value=self.__dict__.get(i.name)
            values.append(value)
        values.append(datetime.fromtimestamp(self.Timestamp).ctime())
        return values
    def synthetic_field_str(self):
        f=string.ascii_uppercase+string.digits
        part=[]
        for num in range(4):
            part.append(f[random.randint(0,len(f)-1)])
        part.append("-")
        for num in range(4):
            part.append(f[random.randint(0,len(f)-1)])
        return ''.join(part)



    def __init__(self,Barcode,Code,upce2upca='',Name='',InList=False,Price=0.0,Note='',Size='',CaseCount=0,Shelf=0,BackRoom=0,Display_1=0,Display_2=0,Display_3=0,Display_4=0,Display_5=0,Display_6=0,Stock_Total=0,Timestamp=datetime.now().timestamp(),EntryId=None,Location='///',ListQty=0.0,Image='',CHKSTND_SPLY=0,WD_DSPLY=0,FLRL_CHP_DSPLY=0,FLRL_WTR_DSPLY=0,SBX_WTR_KLR=0,SBX_CHP_DSPLY=0,SBX_WTR_DSPLY=0,Facings=0,Tags='',CaseID_6W='',CaseID_BR='',CaseID_LD='',ALT_Barcode='',DUP_Barcode=''):
        if EntryId:
            self.EntryId=EntryId
        self.Barcode=Barcode
        self.Code=Code
        self.Name=Name
        self.Price=Price
        self.Note=Note
        self.Size=Size
        self.Shelf=Shelf
        self.CaseCount=CaseCount
        self.BackRoom=BackRoom
        self.Display_1=Display_1
        self.Display_2=Display_2
        self.Display_3=Display_3
        self.Display_4=Display_4
        self.Display_5=Display_5
        self.Display_6=Display_6
        self.Stock_Total=Stock_Total
        self.Location=Location
        self.Timestamp=Timestamp
        self.InList=InList
        self.ListQty=ListQty
        self.upce2upca=upce2upca
        self.Image=Image

        self.ALT_Barcode=ALT_Barcode
        self.DUP_Barcode=DUP_Barcode
        self.CaseID_BR=CaseID_BR
        self.CaseID_LD=CaseID_LD
        self.CaseID_6W=CaseID_6W

        self.Tags=Tags
        self.Facings=Facings
        
        self.SBX_WTR_DSPLY=SBX_WTR_DSPLY
        self.SBX_CHP_DSPLY=SBX_CHP_DSPLY
        self.SBX_WTR_KLR=SBX_WTR_KLR

        self.FLRL_CHP_DSPLY=FLRL_CHP_DSPLY
        self.FLRL_WTR_DSPLY=FLRL_WTR_DSPLY

        self.WD_DSPLY=WD_DSPLY
        self.CHKSTND_SPLY=CHKSTND_SPLY
        #CHKSTND_SPLY=0,WD_DSPLY=0,FLRL_CHP_DSPLY=0,FLRL_WTR_DSPLY=0,SBX_WTR_KLR=0,SBX_CHP_DSPLY=0,SBX_WTR_DSPLY=0,Facings=0,Tags='',CaseID_6W='',CaseID_BR='',CaseID_LD='',ALT_Barcode='',DUP_Barcode=''

        '''
        ALT_Barcode=Column(String)
        DUP_Barcode=Column(String)
        CaseID_BR=Column(String)
        CaseID_LD=Column(String)
        CaseID_6W=Column(String)
        Tags=Column(String)
        Facings=Column(Integger)
        SBX_WTR_DSPLY=Column(Integer)
        SBX_CHP_DSPLY=Column(Integer)
        SBX_WTR_KLR=Column(Integer)
        FLRL_CHP_DSPLY=Column(Integer)
        FLRL_WTR_DSPLY=Column(Integer)
        WD_DSPLY=WD_DSPLY=Column(Integer)
        CHKSTND_SPLY=CHKSTND_SPLY=Column(Integer)
        '''


        #proposed fields
        #[done]smle,s|search|? - calls a prompt to search for InList==True with CODE|BARCODE instead of direct search waits for b for back, q for quit, for next CODE|BARCODE
        #optional fields
        #self.alt_barcode
        #self.duplicate_code
        #self.case_id_backroom - in case specific case is needed to be logged
        #csidbm,$EntryId,generate - create a synthetic id for case and save item to and save qrcode png of $case_id
        #csidbm,$EntryId,$case_id - set case id for item
        #csidbm,$EntryId - display item case id
        #csidbm,s|search,$case_id - display items associated with $case_id
        #csidbm,$EntryId,clr_csid - set $case_id to ''
        #the above applies to the below self.case_id_load as well
        #self.case_id_load - in case specific is found in load wanted in data

        #self.Tags
        #cmd syntax
        #tag,$EntryID,+|-|=,$tag_text
        #tag,s|search,$tag_text -> search for items with tag txt (multiple tags separated with a bar '|'')
        #tag,$EntryId|$code|$barcode -> display tags for item with $entryId, $code (returns multiple values), $barcode (returns multiple values)
        #- removes tag from field with tags
        #+ adds a tag to field with tags
        #= set field to $tag_text
        #self.Tags is a string separated by json string containing a list of tags
        #json.dumps(['a','b','c'])
        #json.loads('["a", "b", "c"]')

        #self.Facings
        #additional inventory fields
        #self.checkstandsupplies
        #self.sbx_dsply
        #self.flrl_dsply
        #self.wd_dsply

        try:
            if not self.LCL_ANDROID.exists():
                self.LCL_ANDROID.mkdir(parents=True)
        except Exception as e:
            print(e,"android directory!")
    LCL=Path("LCL_IMG")
    LCL_ANDROID=Path("/storage/emulated/0/DCIM/Screenshots")

    def save_code(self):
        filename=Path(f"{self.EntryId}_code.png")
        if self.LCL_ANDROID.exists():
            filename=str(self.LCL_ANDROID/filename)
        else:
            filename=str(self.LCL/filename)
        print(filename)
        try:
            codes=[Code39,QRCode]
            for code in codes:
                try:
                    if code == QRCode:
                        qrcode.make(self.Barcode).save(filename)
                        break
                    else:
                        code(self.Code,add_checksum=False,writer=ImageWriter()).write(filename)
                        break
                    pass
                except Exception as e:
                    print(e)


            return filename
        except Exception as e:
            print(e)
        return False

    def save_barcode(self):
        filename=Path(f"{self.EntryId}_barcode.png")
        if self.LCL_ANDROID.exists():
            filename=str(self.LCL_ANDROID/filename)
        else:
            filename=str(self.LCL/filename)
        print(filename)
        try:
            codes=[UPCA,EAN13,QRCode]
            for code in codes:
                try:
                    if code == QRCode:
                        qrcode.make(self.Barcode).save(filename)
                        break
                    else:
                        if len(self.Barcode) <= 8 and code == UPCA:
                            upca=upcean.convert.convert_barcode_from_upce_to_upca(self.Barcode)
                            if upca != False:
                                code(upca,writer=ImageWriter()).write(filename)
                            else:
                                continue
                        elif len(self.Barcode) > 12:
                            if code == EAN13:
                                code(self.Barcode,writer=ImageWriter()).write(filename)
                            else:
                                continue
                        else:
                            code(self.Barcode,writer=ImageWriter()).write(filename)
                        break
                except Exception as e:
                    print(e)
            return filename


        except Exception as e:
            print(e)
        return False

    def saveItemData(self,num=None):
        if self.LCL_ANDROID.exists():
            self.LCL=self.LCL_ANDROID
        text=[]
        for column in self.__table__.columns:
            text.append('='.join([column.name,str(self.__dict__[column.name])]))
        data='\n'.join(text)
        #LCL=Path("LCL_IMG")
        if not self.LCL.exists():
            self.LCL.mkdir()
        fname=str(self.LCL/Path(str(self.EntryId)))
        n=self.save_barcode()
        c=self.save_code()
        renderImageFromText(fname,data,barcode_file=n,img_file=self.Image,code_file=c)

    def listdisplay(self,num=None):
        name=self.Name
        ma=32
        n=self.split_by_len(name,ma)
        #print(n)
        new=[]
        for i in n:
            if n.index(i) > 0:
                new.append(i)
            else:
                new.append(i)
        name='\n'.join(new)
        name="\n"+name
        if num == None:
            num=''
        msg=f'''{Fore.magenta}{Fore.dark_goldenrod}{num}->({Style.reset} NAME={Fore.cyan}{name}{Style.reset} | UPC={Fore.green}{self.Barcode}{Style.reset} | SHELF={Fore.yellow}{self.Code}{Style.reset} | QTY={Fore.violet}{self.ListQty}{Style.reset} | EID={Fore.sky_blue_2}{self.EntryId}{Style.reset}{Fore.magenta} )-<{Fore.dark_goldenrod}{num}{Style.reset}'''
        print(msg)
    def split_by_len(self,string, length):
        result = []
        for i in range(0, len(string), length):
            result.append(string[i:i + length])
        return result

    def saveListExtended(self,num):
        if self.LCL_ANDROID.exists():
            self.LCL=self.LCL_ANDROID
        total=self.Display_1+self.Display_2+self.Display_3+self.Display_4+self.Display_5+self.Display_6+self.Shelf+self.BackRoom
        total+=self.WD_DSPLY+self.SBX_WTR_KLR+self.SBX_CHP_DSPLY+self.SBX_WTR_DSPLY+self.FLRL_CHP_DSPLY+self.FLRL_WTR_DSPLY+self.CHKSTND_SPLY
        name=self.Name
        ma=32
        if len(name) > ma:
            n=self.split_by_len(name,ma)
            #print(n)
            new=[]
            for i in n:
                if n.index(i) > 0:
                    new.append(str(' '*7)+i)
                else:
                    new.append(i)
            name='\n'.join(new)
        if num == None:
            num=''
        msg=f"""
============={num}============
Barcode = {self.Barcode}
Code/Shelf/Label = {self.Code}
Name = {name}
Shelf = {self.Shelf}
BackRoom/Wall = {self.BackRoom}

Display_1 = {self.Display_1}
Display_2 = {self.Display_2}
Display_3 = {self.Display_3}
Display_4 = {self.Display_4}
Display_5 = {self.Display_5}
Display_6 = {self.Display_6}

SBX_WTR_DSPLY={self.SBX_WTR_DSPLY}
SBX_CHP_DSPLY={self.SBX_CHP_DSPLY}
SBX_WTR_KLR={self.SBX_WTR_KLR}

FLRL_CHP_DSPLY={self.FLRL_CHP_DSPLY}
FLRL_WTR_DSPLY={self.FLRL_WTR_DSPLY}

WD_DSPLY={self.WD_DSPLY}

CHKSTND_SPLY={self.CHKSTND_SPLY}

Total = {total}
Total - Backroom = {total-self.BackRoom}
-------------{num}-------------
"""
        
        if not self.LCL.exists():
            self.LCL.mkdir()
        fname=str(self.LCL/Path(str(self.EntryId)))
        renderImageFromText(fname,msg)
        '''
ALT_Barcode={self.ALT_Barcode}
DUP_Barcode={self.DUP_Barcode}
CaseID_BR={self.CaseID_BR}
CaseID_LD={self.CaseID_LD}
CaseID_6W={self.CaseID_6W}
Tags={self.Tags}
Facings={self.Facings}

        '''

    def listdisplay_extended(self,num):
        #print(self.csv_headers())
        #print(self.csv_values())
        total=self.Display_1+self.Display_2+self.Display_3+self.Display_4+self.Display_5+self.Display_6+self.Shelf+self.BackRoom
        total+=self.SBX_WTR_DSPLY
        total+=self.SBX_CHP_DSPLY
        total+=self.SBX_WTR_KLR
        total+=self.FLRL_CHP_DSPLY
        total+=self.FLRL_WTR_DSPLY
        total+=self.WD_DSPLY
        total+=self.CHKSTND_SPLY

        name=self.Name
        ma=32
        if len(name) > ma:
            n=self.split_by_len(name,ma)
            #print(n)
            new=[]
            for i in n:
                if n.index(i) > 0:
                    new.append(str(' '*7)+i)
                else:
                    new.append(i)
            name='\n'.join(new)
        if num == None:
            num=''
        msg=f"""
============={Fore.green}{num}{Style.reset}============
{Fore.red}EntryId{Style.bold}={Fore.green_yellow}{self.EntryId}{Style.reset}
{Fore.blue}Barcode{Style.reset} = {Fore.aquamarine_3}{self.Barcode}{Style.reset}
{Fore.dark_goldenrod}Code/Shelf/Label{Style.reset} = {Fore.yellow}{self.Code}{Style.reset}
{Fore.green_yellow}Name{Style.reset} = {Fore.cyan}{name}{Style.reset}
{Fore.violet}Shelf{Style.reset} = {Fore.magenta}{self.Shelf}{Style.reset}
{Fore.yellow_4b}BackRoom/Wall{Style.reset} = {Fore.orange_4b}{self.BackRoom}{Style.reset}
{Fore.slate_blue_1}Display_1{Style.reset} = {Fore.medium_purple_3b}{self.Display_1}{Style.reset}
{Fore.medium_violet_red}Display_2{Style.reset} = {Fore.magenta_3a}{self.Display_2}{Style.reset}
{Fore.deep_pink_1a}Display_3 = {Style.reset}{Fore.purple_1a}{self.Display_3}{Style.reset}
{Fore.orange_red_1}Display_4 = {Style.reset}{Fore.plum_4}{self.Display_4}{Style.reset}
{Fore.light_salmon_1}Display_5 = {Style.reset}{Fore.pale_green_1a}{self.Display_5}{Style.reset}
{Fore.pink_1}Display_6 = {Style.reset}{Fore.gold_3a}{self.Display_6}{Style.reset}

{Fore.cyan}SBX_WTR_DSPLY{Style.reset}={Fore.pale_green_1b}{self.SBX_WTR_DSPLY}{Style.reset}
{Fore.cyan}SBX_CHP_DSPLY{Style.reset}={Fore.pale_green_1b}{self.SBX_CHP_DSPLY}{Style.reset}
{Fore.cyan}SBX_WTR_KLR{Style.reset}={Fore.pale_green_1b}{self.SBX_WTR_KLR}{Style.reset}
{Fore.violet}FLRL_CHP_DSPLY{Style.reset}={Fore.green_yellow}{self.FLRL_CHP_DSPLY}{Style.reset}
{Fore.violet}FLRL_WTR_DSPLY{Style.reset}={Fore.green_yellow}{self.FLRL_WTR_DSPLY}{Style.reset}
{Fore.grey_50}WD_DSPLY{Style.reset}={self.WD_DSPLY}{Style.reset}
{Fore.grey_50}CHKSTND_SPLY{Style.reset}={self.CHKSTND_SPLY}{Style.reset}

{Fore.pale_green_1b}{Style.underline}If Backroom is needed as part of total use value Below...{Style.reset}
{Fore.spring_green_3a}Total{Style.reset} = {Fore.light_yellow}{total}{Style.reset}
{Fore.yellow_4b}{Style.underline}If Backroom is not needed as part of total use value Below...{Style.reset}
{Fore.hot_pink_2}Total - Backroom{Style.reset} = {Fore.light_yellow}{total-self.BackRoom}{Style.reset}
-------------{Fore.red}{num}{Style.reset}-------------
"""
        print(msg)
        return msg

    def imageExists(self):
        try:
            return Path(self.Image).exists() and Path(self.Image).is_file()
        except Exception as e:
            return False

    def __repr__(self):
        m= f"""
        {Style.bold}{Style.underline}{Fore.pale_green_1b}Entry{Style.reset}(
        {Fore.hot_pink_2}{Style.bold}{Style.underline}EntryId{Style.reset}={self.EntryId}
        {Fore.violet}{Style.underline}Code{Style.reset}='{self.Code}',
        {Fore.orange_3}{Style.bold}Barcode{Style.reset}='{self.Barcode}',
        {Fore.orange_3}{Style.underline}UPCE from UPCA[if any]{Style.reset}='{self.upce2upca}',
        {Fore.green}{Style.bold}Price{Style.reset}=${self.Price},
        {Fore.red}Name{Style.reset}='{self.Name}',
        {Fore.tan}Note{Style.reset}='{self.Note}',

        {Fore.grey_50}ALT_Barcode{Style.reset}={Fore.grey_70}{self.ALT_Barcode}{Style.reset}
        {Fore.grey_50}DUP_Barcode{Style.reset}={Fore.grey_70}{self.DUP_Barcode}{Style.reset}
        {Fore.grey_50}CaseID_BR{Style.reset}={Fore.grey_70}{self.CaseID_BR}{Style.reset}
        {Fore.grey_50}CaseID_LD{Style.reset}={Fore.grey_70}{self.CaseID_LD}{Style.reset}
        {Fore.grey_50}CaseID_6W{Style.reset}={Fore.grey_70}{self.CaseID_6W}{Style.reset}
        {Fore.grey_50}Tags{Style.reset}={Fore.grey_70}{self.Tags}{Style.reset}
        {Fore.grey_50}Facings{Style.reset}={Fore.grey_70}{self.Facings}{Style.reset}

        {Fore.pale_green_1b}Timestamp{Style.reset}='{datetime.fromtimestamp(self.Timestamp).strftime('%D@%H:%M:%S')}',
        {Fore.deep_pink_3b}Shelf{Style.reset}={self.Shelf},
        {Fore.light_steel_blue}BackRoom{Style.reset}={self.BackRoom},
        {Fore.cyan}Display_1{Style.reset}={self.Display_1},
        {Fore.cyan}Display_2{Style.reset}={self.Display_2},
        {Fore.cyan}Display_3{Style.reset}={self.Display_3},
        {Fore.cyan}Display_4{Style.reset}={self.Display_4},
        {Fore.cyan}Display_5{Style.reset}={self.Display_5},
        {Fore.cyan}Display_6{Style.reset}={self.Display_6},

        {Fore.cyan}SBX_WTR_DSPLY{Style.reset}={Fore.pale_green_1b}{self.SBX_WTR_DSPLY}{Style.reset}
        {Fore.cyan}SBX_CHP_DSPLY{Style.reset}={Fore.pale_green_1b}{self.SBX_CHP_DSPLY}{Style.reset}
        {Fore.cyan}SBX_WTR_KLR{Style.reset}={Fore.pale_green_1b}{self.SBX_WTR_KLR}{Style.reset}
        {Fore.violet}FLRL_CHP_DSPLY{Style.reset}={Fore.green_yellow}{self.FLRL_CHP_DSPLY}{Style.reset}
        {Fore.violet}FLRL_WTR_DSPLY{Style.reset}={Fore.green_yellow}{self.FLRL_WTR_DSPLY}{Style.reset}
        {Fore.grey_50}WD_DSPLY{Style.reset}={self.WD_DSPLY}{Style.reset}
        {Fore.grey_50}CHKSTND_SPLY{Style.reset}={self.CHKSTND_SPLY}{Style.reset}

        {Fore.light_salmon_3a}Stock_Total{Style.reset}={self.Stock_Total},
        {Fore.magenta_3c}InList{Style.reset}={self.InList}
        {Fore.indian_red_1b}{Style.bold}{Style.underline}{Style.blink}ListQty{Style.reset}={self.ListQty}
        {Fore.misty_rose_3}Location{Style.reset}={self.Location}
        {Fore.sky_blue_2}CaseCount{Style.reset}={self.CaseCount}
        {Fore.sky_blue_2}Size{Style.reset}={self.Size}
        {Fore.tan}Image[{Fore.dark_goldenrod}Exists:{Fore.deep_pink_3b}{self.imageExists()}{Style.reset}{Fore.tan}]{Style.reset}={self.Image}"""

        if self.imageExists():
            m+=f"""
        {Fore.green}Image {Fore.orange_3}{Style.bold}{Style.underline}ABSOLUTE{Style.reset}{Style.reset}={Path(self.Image).absolute()}"""

        m+="""
        )
        """
        if self.Barcode and len(self.Barcode) >= 13:
            print(f"{Fore.hot_pink_1b}Detected Code is 13 digits long; please verify the 'EAN13 Stripped $var_x=$var_z' data first before using the UPC Codes!{Style.reset}")
        pc.PossibleCodes(scanned=self.Barcode)
        pc.PossibleCodesEAN13(scanned=self.Barcode)
        return m

Entry.metadata.create_all(ENGINE)
PairCollection.metadata.create_all(ENGINE)
tables={
    'Entry':Entry,
    'PairCollection':PairCollection,
}

class DayLog(BASE):
    __tablename__="DayLog"
    DayLogId=Column(Integer,primary_key=True)
    EntryId=Column(Integer)
    ScannedCode=Column(String)
    Qty=Column(Float)
    ListNote=Column(String)
    ListName=Column(String)
    date=Column(Date)

    def __init__(self,EntryId,ScannedCode,date,Qty=1,ListName=f'Entry for {datetime.now().month}/{datetime.now().day}/{datetime.now().year}',ListNote=f'Entry for {datetime.now().ctime()}',DayLogId=None):
        self.ScannedCode=ScannedCode
        self.Qty=Qty
        if date:
            self.date=date
        else:
            self.date=datetime.now()

        self.ListName=ListName
        self.ListNote=ListNote
        self.EntryId=EntryId
        if DayLogId:
            self.DayLogId=DayLogId

    def addQty(self,amount):
        self.Qty+=amount
    def minusQty(self,amount):
        self.Qty-=amount
    def clearQty():
        self.Qty=0
    def setQty(self,qty):
        self.Qty=qty

    def __repr__(self):
        return f"""{Fore.cyan}{Style.bold}DayLog{Style.reset}(
    {Fore.red}DayLogId={self.DayLogId}{Style.reset},
    {Fore.green}ScannedCode={self.ScannedCode},{Style.reset}
    {Fore.yellow}EntryId={self.EntryId},{Style.reset},
    {Fore.magenta}Qty={self.Qty},{Style.reset}
    {Fore.GREY_50}ListName={self.ListName},{Style.reset}
    {Fore.tan}ListNote={self.ListNote},{Style.reset}
    {Fore.violet}date={self.date},{Style.reset}
    )"""
DayLog.metadata.create_all(ENGINE)
