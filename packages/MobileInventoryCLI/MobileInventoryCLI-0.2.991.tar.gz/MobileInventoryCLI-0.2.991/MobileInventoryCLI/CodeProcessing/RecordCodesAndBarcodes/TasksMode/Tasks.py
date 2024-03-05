from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified

import random
from colored import Style,Fore
class TasksMode:
    def getTotalwithBreakDownForScan(self):
        while True:
            color1=Fore.red
            color2=Fore.yellow
            color3=Fore.cyan
            color4=Fore.green_yellow

            scanned=input("barcode|code: ")
            if scanned in self.options['1']['cmds']:
                self.options['1']['exec']()
            elif scanned in self.options['2']['cmds']:
                return
            else:
                with Session(self.engine) as session:
                    result=session.query(Entry).filter(or_(Entry.Barcode==scanned,Entry.Code==scanned)).first()
                    if result:
                        total=0
                        for f in self.valid_fields:
                            if getattr(result,f) != None:
                                total+=float(getattr(result,f))
                        print(result)
                        print(f"{color1}Amount Needed Total is {Style.reset}{color2}{Style.bold}{total}{Style.reset}!")
                        
                    else:
                        print(f"{Fore.red}{Style.bold}No such Barcode|Code:{scanned}{Style.reset}")

            

    def display_field(self,fieldname):
        color1=Fore.red
        color2=Fore.yellow
        color3=Fore.cyan
        color4=Fore.green_yellow
        m=f"Item Num |Name|Barcode|Code|{fieldname}"
        hr='-'*len(m)
        print(f"{m}\n{hr}")
        if fieldname in self.valid_fields:
            with Session(self.engine) as session:
                results=session.query(Entry).filter(Entry.InList==True).all()
                if len(results) < 1:
                    print(f"{Fore.red}{Style.bold}Nothing is in List!{Style.reset}")
                for num,result in enumerate(results):
                    print(f"{Fore.red}{num}{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")
        print(f"{m}\n{hr}")

    def setFieldInList(self,fieldname):
        while True:
            m=f"Item Num |Name|Barcode|Code|{fieldname}"
            hr='-'*len(m)
            print(f"{m}\n{hr}")
            if fieldname in self.valid_fields:
                with Session(self.engine) as session:
                    code=''
                    while True:
                        code=input("barcode|code: ")
                        if code in self.options['1']['cmds']:
                            self.options['1']['exec']()
                        elif code in self.options['2']['cmds']:
                            return
                        else:
                            break
                    value=0
                    while True:
                        value=input("amount|+amount|-amount: ")
                        if value in self.options['1']['cmds']:
                            self.options['1']['exec']()
                        elif value in self.options['2']['cmds']:
                            return
                        else:
                            try:
                                color1=Fore.red
                                color2=Fore.yellow
                                color3=Fore.cyan
                                color4=Fore.green_yellow 
                                if value.startswith("-") or value.startswith("+"):
                                    value=float(eval(value))
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                                    if result:
                                        setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                        result.InList=True
                                        session.commit()
                                        session.flush()
                                        session.refresh(result)
                                        print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")
                                        print(f"{m}\n{hr}")

                                    else:
                                        n=Entry(Barcode=code,Code='',Name=code,InList=True,Note="New Item")
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        result=n
                                        print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")

                                        print(f"{m}\n{hr}")
                                else:
                                    value=float(eval(value))
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                                    if result:
                                        setattr(result,fieldname,value)
                                        result.InList=True
                                        session.commit()
                                        session.flush()
                                        session.refresh(result)
                                        print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")

                                        print(f"{m}\n{hr}")

                                    else:
                                        n=Entry(Barcode=code,Code='',Name=code,InList=True,Note="New Item")
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        result=n
                                        print(f"{Fore.red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")

                                        print(f"{m}\n{hr}")

                                        #raise Exception(result)
                                break
                            except Exception as e:
                                print(e)
    def setName(self):
        with Session(self.engine) as session:
            code=''
            while True:
                code=input("barcode|code: ")
                if code in self.options['1']['cmds']:
                    self.options['1']['exec']()
                elif code in self.options['2']['cmds']:
                    return
                else:
                    break
            value=0
            while True:
                value=input("Name: ")
                if value in self.options['1']['cmds']:
                    self.options['1']['exec']()
                elif value in self.options['2']['cmds']:
                    return
                else:
                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                    if result:
                        result.Name=value
                        session.commit()
                        session.flush()
                        session.refresh(result)
                        print(result)
                    else:
                        print(f"{Fore.red}{Style.bold}No Such Item Identified by '{code}'{Style.reset}")
                    break
                            

    def __init__(self,engine,parent):
        self.engine=engine
        self.parent=parent
        self.valid_fields=['Shelf',
        'BackRoom',
        'Display_1',
        'Display_2',
        'Display_3',
        'Display_4',
        'Display_5',
        'Display_6',]
        #self.display_field("Shelf")
        self.options={
                '1':{
                    'cmds':['q','quit','#1'],
                    'desc':"quit program",
                    'exec':lambda: exit("user quit!"),
                    },
                '2':{
                    'cmds':['b','back','#2'],
                    'desc':'go back menu if any',
                    'exec':None
                    },
                }
        #autogenerate duplicate functionality for all valid fields for display
        count=3
        for entry in self.valid_fields:
            self.options[entry]={
                    'cmds':["#"+str(count),f"ls {entry}"],
                    'desc':f'list needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.display_field(f"{entry}"),
                    }
            count+=1
        #setoptions
        #self.setFieldInList("Shelf")
        for entry in self.valid_fields:
            self.options[entry+"_set"]={
                    'cmds':["#"+str(count),f"set {entry}"],
                    'desc':f'set needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.setFieldInList(f"{entry}"),
                    }
            count+=1
        self.options["lu"]={
                    'cmds':["#"+str(count),f"lookup","lu","check","ck"],
                    'desc':f'get total for valid fields',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(),
                    }
        count+=1
        self.options["setName"]={
                    'cmds':["#"+str(count),f"setName","sn"],
                    'desc':f'set name for item by barcode!',
                    'exec':lambda self=self,entry=entry: self.setName(),
                    }
        count+=1


        while True:
            command=input(f"{Style.bold}{Fore.green}do what[??/?]:{Style.reset} ")
            if self.parent != None and self.parent.Unified(command):
                print("ran an external command!")
            elif command == "??":
                for num,option in enumerate(self.options):
                    color=Fore.dark_goldenrod
                    color1=Fore.cyan
                    if (num%2)==0:
                        color=Fore.green_yellow
                        color1=Fore.magenta
                    print(f"{color}{self.options[option]['cmds']}{Style.reset} - {color1}{self.options[option]['desc']}{Style.reset}")
            else:
                for option in self.options:
                    if self.options[option]['exec'] != None and command.lower() in self.options[option]['cmds']:
                        self.options[option]['exec']()
                    elif self.options[option]['exec'] == None and command.lower() in self.options[option]['cmds']:
                        return
               



if __name__ == "__main__":
    TasksMode(parent=None,engine=ENGINE)
