# -*- coding: utf-8 -*-

import unohelper
from uno import fileUrlToSystemPath

class Einstellungen():
    
    def __init__(self,mb,pdk):
        if mb.debug: log(inspect.stack)
        
        self.mb = mb
        
        global pd
        pd = pdk
        
        
    def start(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            pass
                
            self.erzeuge_einstellungsfenster()
                
        except Exception as e:
            self.mb.nachricht('Export.export '+ str(e),"warningbox")
            log(inspect.stack,tb())


    def erzeuge_einstellungsfenster(self): 
        if self.mb.debug: log(inspect.stack)
        try:
            breite = 650
            hoehe = 280
            breite_listbox = 120
            
            
            sett = self.mb.settings_exp
            
            posSize_main = self.mb.desktop.ActiveFrame.ContainerWindow.PosSize
            X = posSize_main.X +20
            Y = posSize_main.Y +20            

            # Listener erzeugen 
            listener = {}           
            listener.update( {'auswahl_listener': Auswahl_Item_Listener(self.mb)} )
            
            controls = self.dialog_einstellungen(listener, breite_listbox,breite,hoehe)
            ctrls,pos_y = self.mb.erzeuge_fensterinhalt(controls)                
            
            # Hauptfenster erzeugen
            posSize = X,Y,breite,pos_y + 40
            fenster,fenster_cont = self.mb.erzeuge_Dialog_Container(posSize)
            fenster_cont.Model.Text = LANG.EXPORT
            
            #fenster_cont.addEventListener(listenerDis)
            self.haupt_fenster = fenster
            
            # Controls in Hauptfenster eintragen
            for c in ctrls:
                fenster_cont.addControl(c,ctrls[c])
            
            listener['auswahl_listener'].container = ctrls['control_Container']
            
        except:
            log(inspect.stack,tb())
                
       
    
    def dialog_einstellungen(self,listener,breite_listbox,breite,hoehe):
        if self.mb.debug: log(inspect.stack)
        
        lb_items = LANG.TRENNER,LANG.MAUSRAD,LANG.LOG

        controls = (
            10,
            ('controlE_calc',"FixedText",        
                                    20,0,50,20,    
                                    ('Label','FontWeight'),
                                    (LANG.EINSTELLUNGEN ,150),                  
                                    {} 
                                    ), 
            20,                                                  
            ('control_Liste',"ListBox",      
                                    20,0,breite_listbox,hoehe,    
                                    ('Border',),
                                    ( 2,),       
                                    {'addItems':lb_items,'addItemListener':(listener['auswahl_listener'])} 
                                    ),  
            0,
            ('control_Container',"Container",      
                                    breite_listbox + 40,0,breite-60-breite_listbox ,hoehe ,    
                                    ('BackgroundColor','Border'),
                                    (KONST.MENU_DIALOG_FARBE,1),              
                                    {} 
                                    ),  
            hoehe - 20,
            )
        return controls

        

from com.sun.star.awt import XItemListener   
class Auswahl_Item_Listener(unohelper.Base, XItemListener):
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        self.mb = mb
        self.container = None
        
    # XItemListener    
    def itemStateChanged(self, ev):  
        if self.mb.debug: log(inspect.stack)
        
        try:     
            sel = ev.value.Source.Items[ev.value.Selected] 
            
            for c in self.container.getControls():
                c.dispose()
            
            if sel == LANG.LOG:
                self.dialog_logging()
                    
            elif sel == LANG.MAUSRAD:
                self.dialog_mausrad()
                                        
            elif sel == LANG.TRENNER:
                self.dialog_trenner()

        except:
            log(inspect.stack,tb())
            
    def disposing(self,ev):
        return False
  
        
    def dialog_logging(self):

        try:
            ctx = self.mb.ctx
            mb = self.mb
            breite = 650
            hoehe = 190
            
            tab = 20
            tab1 = 40
            
            
            posSize_main = self.mb.desktop.ActiveFrame.ContainerWindow.PosSize
            X = posSize_main.X +20
            Y = posSize_main.Y +20
            Width = breite
            Height = hoehe
            
            posSize = X,Y,Width,Height
            fenster_cont = self.container
            
            y = 10
            
            prop_names = ('Label','FontWeight',)
            prop_values = (LANG.EINSTELLUNGEN_LOGDATEI,200,)
            control, model = mb.createControl(ctx, "FixedText", tab, y, 200, 20, prop_names, prop_values)
            fenster_cont.addControl('Titel', control) 

            y += 30
            
            prop_names = ('Label','State')
            prop_values = (LANG.KONSOLENAUSGABE,self.mb.class_Log.output_console)
            controlCB, model = mb.createControl(ctx, "CheckBox", tab, y, 200, 20, prop_names, prop_values)
            controlCB.setActionCommand('Konsole')
             
            y += 20
            
            prop_names = ('Label','State',)
            prop_values = (LANG.ARGUMENTE_LOGGEN,self.mb.class_Log.log_args,)
            control_arg, model = mb.createControl(ctx, "CheckBox", tab1, y, 200, 20, prop_names, prop_values)
            control_arg.setActionCommand('Argumente')
            control_arg.Enable = (self.mb.class_Log.output_console == 1)
            
            y += 30
            
            prop_names = ('Label','State',)
            prop_values = (LANG.LOGDATEI_ERZEUGEN,self.mb.class_Log.write_debug_file,)
            control_log, model = mb.createControl(ctx, "CheckBox", tab1, y, 200, 20, prop_names, prop_values)
            control_log.setActionCommand('Logdatei')
            control_log.Enable = (self.mb.class_Log.output_console == 1)
            
            y += 20
            
            prop_names = ('Label',)
            prop_values = (LANG.SPEICHERORT,)
            control_filepath, model = mb.createControl(ctx, "FixedText", tab1, y, 200, 20, prop_names, prop_values)
            fenster_cont.addControl('Titel', control_filepath) 
            
            y += 20
            
            prop_names = ('Label',)
            prop_values = (mb.class_Log.location_debug_file,)
            control_path, model = mb.createControl(ctx, "FixedText", tab1, y, 600, 20, prop_names, prop_values)
            fenster_cont.addControl('Titel', control_path)
            
            # Breite des Log-Fensters setzen
            prefSize = control_path.getPreferredSize()
            Hoehe = prefSize.Height 
            Breite = prefSize.Width
            control_path.setPosSize(0,0,Breite+10,0,4)
            #fenster.setPosSize(0,0,Breite+10+tab1,0,4)
            
            y += 20
            
            prop_names = ('Label',)
            prop_values = (LANG.AUSWAHL,)
            control_but, model = mb.createControl(ctx, "Button", tab1, y, 80, 20, prop_names, prop_values)
            control_but.setActionCommand('File')
            fenster_cont.addControl('Titel', control)
            
            
            # Listener setzen
            log_listener = Listener_Logging_Einstellungen(self.mb,control_log,control_arg,control_path)
            
            controlCB.addActionListener(log_listener)
            fenster_cont.addControl('Konsole', controlCB)
            
            control_log.addActionListener(log_listener)
            fenster_cont.addControl('Log', control_log) 
            
            control_but.addActionListener(log_listener)
            fenster_cont.addControl('but', control_but)
            
            control_arg.addActionListener(log_listener)
            fenster_cont.addControl('arg', control_arg)
            
        except:
            log(inspect.stack,tb())
            
    
    
            
    def dialog_mausrad_elemente(self,listener,nutze_mausrad):
        if self.mb.debug: log(inspect.stack)
        
        lb_items = 'Trenner','Logging','Mausrad'

        controls = (
            10,
            ('controlE_calc',"FixedText",        
                                    20,0,50,20,    
                                    ('Label','FontWeight'),
                                    (LANG.NUTZE_MAUSRAD ,150),                  
                                    {} 
                                    ), 
            20,                                                  
            ('control_CB_calc',"CheckBox",      
                                    20,0,200,220,    
                                    ('Label','State'),
                                    (LANG.NUTZE_MAUSRAD,nutze_mausrad),       
                                    {'addActionListener':(listener,)} 
                                    ),  
            30,
            ('control_Container_calc',"FixedText",      
                                    20,0,200,200,    
                                    ('MultiLine','Label'),
                                    (True,LANG.MAUSRAD_HINWEIS),              
                                    {} 
                                    ),  
            200,
            )
        return controls
    
    
    def dialog_mausrad(self): 
        if self.mb.debug: log(inspect.stack)
        
        try:

            sett = self.mb.settings_proj
            
            try:
                if sett['nutze_mausrad']:
                    nutze_mausrad = 1
                else:
                    nutze_mausrad = 0
            except:
                self.mb.settings_proj['nutze_mausrad'] = False
                nutze_mausrad = 0
            
            posSize_main = self.mb.desktop.ActiveFrame.ContainerWindow.PosSize
            X = posSize_main.X +20
            Y = posSize_main.Y +20            

            # Listener erzeugen 
            listener = Listener_Mausrad_Einstellungen(self.mb)         
            
            controls = self.dialog_mausrad_elemente(listener,nutze_mausrad)
            ctrls,pos_y = self.mb.erzeuge_fensterinhalt(controls)                
             
            # Controls in Hauptfenster eintragen
            for c in ctrls:
                self.container.addControl(c,ctrls[c])
                         
        except:
            log(inspect.stack,tb())
            
            
    
    def dialog_trenner_elemente(self,trenner_dict,listener_CB,listener_URL):
        if self.mb.debug: log(inspect.stack)
        
        controls = (
            10,
            ('control',"FixedText",         
                                    'tab0',0,250,20,  
                                    ('Label','FontWeight'),
                                    (LANG.TRENNER_FORMATIERUNG ,150),                                             
                                    {} 
                                    ),
            30,
            ('control1',"CheckBox",         
                                    'tab0',0,200,20,   
                                    ('Label','State'),
                                    (LANG.LINIE,trenner_dict['strich']),                                                  
                                    {'addItemListener':(listener_CB)} 
                                    ) ,
            0,
            ('control11',"CheckBox",        
                                    'tab4x',0,150,20,   
                                    ('Label','State'),
                                    (LANG.KEIN_TRENNER,trenner_dict['keiner']),                                           
                                    {'addItemListener':(listener_CB)} 
                                    ),
            30,
            ('control2',"CheckBox",         
                                    'tab0',0,360,20,   
                                    ('Label','State'),
                                    (LANG.FARBE,trenner_dict['farbe']),                                                   
                                    {'addItemListener':(listener_CB)} 
                                    ), 
            20,
            ('control3',"FixedText",        
                                    'tab1',0,32,16,  
                                    ('BackgroundColor','Label','Border'),
                                    (self.mb.settings_proj['trenner_farbe_schrift'],'    ',1),       
                                    {'addMouseListener':(listener_CB)} 
                                    ),  
            0,
            ('control4',"FixedText",        
                                    'tab2',0,120,20,  
                                    ('Label',),
                                    (LANG.FARBE_SCHRIFT,),                                                                    
                                    {} 
                                    ),  
            20,
            ('control5',"FixedText",        
                                    'tab1',0,32,16,  
                                    ('BackgroundColor','Label','Border'),
                                    (self.mb.settings_proj['trenner_farbe_hintergrund'],'    ',1),   
                                    {'addMouseListener':(listener_CB)} 
                                    ),  
            0,
            ('control6',"FixedText",        
                                    'tab2',0,120,20,  
                                    ('Label',),
                                    (LANG.FARBE_HINTERGRUND,),                                                                
                                    {} 
                                    ),  
            30,
            ('control7',"CheckBox",         
                                    'tab0',0,80,20,   
                                    ('Label','State'),
                                    (LANG.BENUTZER,trenner_dict['user']),                                                  
                                    {'addItemListener':(listener_CB)} 
                                    ),              
            20,
            ('control8',"FixedText",        
                                    'tab1',0,20,20,   
                                    ('Label',),
                                    ('URL: ',),                                                                            
                                    {'Enable':trenner_dict['user']==1} 
                                    ), 
            0,
            ('control10',"Button",          
                                    'tab2',0,60,20,    
                                    ('Label',),
                                    (LANG.AUSWAHL,),                                                                         
                                    {'Enable':trenner_dict['user']==1,'addActionListener':(listener_URL,)} 
                                    ), 
            30,
            ('control9',"FixedText",        
                                    'tab1',-4,600,20,   
                                    ('Label',),
                                    (self.mb.settings_proj['trenner_user_url'],),                                            
                                    {'Enable':trenner_dict['user']==1} 
                                    ), 
            20,
            )
        
        # Tabs waren urspruenglich gesetzt, um sie in der Klasse Design richtig anzupassen.
        # Das fehlt. 'tab...' wird jetzt nur in Zahlen uebersetzt. Beim naechsten 
        # groesseren Fenster, das ich schreibe und das nachtraegliche Berechnungen benoetigt,
        # sollte der Code generalisiert werden. Vielleicht grundsaetzlich ein Modul fenster.py erstellen?
        tab0 = tab0x = 20
        tab1 = tab1x = 42
        tab2 = tab2x = 78
        tab3 = tab3x = 100
        tab4 = tab4x = 230
        
        tabs = ['tab0','tab1','tab2','tab3','tab4','tab0x','tab1x','tab2x','tab3x','tab4x']
        
        tabs_dict = {}
        for a in tabs:
            tabs_dict.update({a:locals()[a]  })

        controls2 = []
        
        for c in controls:
            if not isinstance(c, int):
                c2 = list(c)
                c2[2] = tabs_dict[c2[2]]
                controls2.append(c2)
            else:
                controls2.append(c)

        return controls2
            
    def dialog_trenner(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            
            listener_CB = Trenner_Format_Listener(self.mb)
            listener_URL = Trenner_URL_Listener(self.mb)
#             design = self.mb.class_Design
#             design.set_default(tabs)
            
            trenner = 'keiner', 'strich', 'farbe', 'user'
            trenner_dict = {}
            for t in trenner:
                if self.mb.settings_proj['trenner'] == t:
                    trenner_dict.update({t: 1})
                else:
                    trenner_dict.update({t: 0})
             

            controls = self.dialog_trenner_elemente(trenner_dict,listener_CB,listener_URL)
            ctrls,pos_y = self.mb.erzeuge_fensterinhalt(controls)


            # UEBERGABE AN LISTENER
            listener_CB.conts = {'controls':{'strich': ctrls['control1'],
                                             'farbe': ctrls['control2'],
                                             'user': ctrls['control7'],
                                             'keiner': ctrls['control11']
                                             },
                                 
                                 'farbe':{'schrift': ctrls['control3'],
                                          'hintergrund': ctrls['control5'],
                                          'text_schrift:': ctrls['control4'],
                                          'text_hinterg:': ctrls['control6'],
                                          },
                                 
                                 'user':{'url': ctrls['control8'],
                                         'auswahl': ctrls['control10']
                                         },
                                 'keiner':{},
                                 'strich':{}
                                 }
            
            listener_URL.url_textfeld = ctrls['control9']
            
            # Controls in Hauptfenster eintragen
            for c in ctrls:
                self.container.addControl(c,ctrls[c])
            
        except:
            log(inspect.stack,tb())
            
            

from com.sun.star.awt import XActionListener
class Listener_Logging_Einstellungen(unohelper.Base, XActionListener):
    def __init__(self,mb,control_log,control_arg,control_filepath):
        self.mb = mb
        self.control_log = control_log
        self.control_arg = control_arg
        self.control_filepath = control_filepath
                
    def actionPerformed(self,ev):
        if self.mb.debug: log(inspect.stack)

        try:
            if ev.ActionCommand == 'Konsole':
                
                self.control_log.Enable = (ev.Source.State == 1)
                self.control_arg.Enable = (ev.Source.State == 1)
                self.mb.class_Log.output_console = ev.Source.State
                self.mb.class_Log.write_debug_config_file()
                self.mb.debug = ev.Source.State
                
            elif ev.ActionCommand == 'Logdatei':
                self.mb.class_Log.write_debug_file = ev.Source.State
                self.mb.class_Log.write_debug_config_file()
                
            elif ev.ActionCommand == 'Argumente':
                self.mb.class_Log.log_args = ev.Source.State
                self.mb.class_Log.write_debug_config_file()
                
            elif ev.ActionCommand == 'File':
                Folderpicker = self.mb.createUnoService("com.sun.star.ui.dialogs.FolderPicker")
                Folderpicker.execute()
                
                if Folderpicker.Directory == '':
                    return
                filepath = fileUrlToSystemPath(Folderpicker.getDirectory())
                
                self.mb.class_Log.location_debug_file = filepath
                self.control_filepath.Model.Label = filepath
                
                self.mb.class_Log.write_debug_config_file()
   
        except:
            log(inspect.stack,tb())
    
    def disposing(self,ev):
        return False     
    
    
class Listener_Mausrad_Einstellungen(unohelper.Base, XActionListener):
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        self.mb = mb
                
    def actionPerformed(self,ev):
        if self.mb.debug: log(inspect.stack)

        try:
            self.mb.settings_proj['nutze_mausrad'] = ev.Source.State == 1
            self.mb.nutze_mausrad = ev.Source.State == 1
            self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj) 
        except:
            log(inspect.stack,tb())
    
    def disposing(self,ev):
        return False    
    
    
from com.sun.star.awt import XMouseListener   
class Trenner_Format_Listener(unohelper.Base,XItemListener,XMouseListener):
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        
        self.mb = mb
        self.conts = {}
        
        
    def itemStateChanged(self, ev):  
        if self.mb.debug: log(inspect.stack)

        try:
            for name in self.conts['controls']:
                if ev.Source == self.conts['controls'][name]:
                    self.conts['controls'][name].State = 1
                    self.mb.settings_proj['trenner'] = name
                    self.aktiviere_controls(self.conts[name])
                else:
                    self.conts['controls'][name].State = 0
                    self.deaktiviere_controls(self.conts[name])
            
            self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj)  
        except:
            log(inspect.stack,tb())
      
        
    def aktiviere_controls(self,ctrls):
        if self.mb.debug: log(inspect.stack) 
        
        for c in ctrls:
            ctrls[c].Enable = True
            
    def deaktiviere_controls(self,ctrls):
        if self.mb.debug: log(inspect.stack) 
        
        for c in ctrls:
            ctrls[c].Enable = False
                
    def mousePressed(self, ev):   
        if self.mb.debug: log(inspect.stack) 

        try:
            if ev.Source == self.conts['farbe']['schrift']:
                self.erzeuge_farb_auswahl_fenster('schrift',ev)
            elif ev.Source == self.conts['farbe']['hintergrund']:
                self.erzeuge_farb_auswahl_fenster('hintergrund',ev)            
        except:
            log(inspect.stack,tb())    
    
    def erzeuge_farb_auswahl_fenster(self,auswahl,ev):
        if self.mb.debug: log(inspect.stack) 
        
        
        posSize = ev.Source.Context.PosSize
        x = ev.value.Source.AccessibleContext.LocationOnScreen.value.X 
        y = ev.value.Source.AccessibleContext.LocationOnScreen.value.Y + ev.value.Source.Size.value.Height
        w = posSize.Width
        h = posSize.Height
        
        win,cont = self.mb.erzeuge_Dialog_Container((x,y,w,h))
        
        y = 20
        
        control, model = self.mb.createControl(self.mb.ctx,"FixedText",20,y ,50,20,(),() )  
        control.Text = LANG.HEXA_EINGBEN
        cont.addControl('Titel', control)
        breite, hoehe = self.mb.kalkuliere_und_setze_Control(control,'w')
        
        y += 25
        
        listener = Farben_Key_Listener(self.mb,win,auswahl,ev.Source)
        control, model = self.mb.createControl(self.mb.ctx,"Edit",20,y ,100,20,(),() ) 
        control.addKeyListener(listener)
        cont.addControl('Hex', control)
        
        y += 25
        
        control, model = self.mb.createControl(self.mb.ctx,"Edit",20,y ,50,20,(),() )  
        control.Text = LANG.FARBWAEHLER
        model.ReadOnly = True
        model.BackgroundColor = KONST.MENU_DIALOG_FARBE
        model.Border = 0
        
        
        cont.addControl('Titel', control)
        breite2, hoehe2 = self.mb.kalkuliere_und_setze_Control(control,'w')
        
        if breite2 > breite:
            breite = breite2
            
        win.setPosSize(0,0,breite + 50,y+40,12)
        
    
            
    def mouseExited(self, ev):
        return False
    def mouseEntered(self,ev):
        return False
    def mouseReleased(self,ev):
        return False
    def disposing(self,ev):
        return False
    
from com.sun.star.awt import XKeyListener
class Farben_Key_Listener(unohelper.Base, XKeyListener):
    
    def __init__(self,mb,win,auswahl,source):
        if mb.debug: log(inspect.stack)
        
        self.mb = mb
        self.win = win
        self.auswahl = auswahl
        self.source = source
    
    def keyPressed(self,ev):
        return False
        
    def keyReleased(self,ev):
        
        if ev.KeyCode != 1280:
            return
        
        if self.mb.debug: log(inspect.stack)
        
        if self.auswahl == 'schrift':
            wahl = 'trenner_farbe_schrift'
        else:
            wahl = 'trenner_farbe_hintergrund'
        
        try:
            farbe = int('0x'+ev.Source.Text,0)
        
        except:
            self.mb.nachricht(LANG.UNGUELTIGE_FARBE,"warningbox")
            self.win.dispose()
            return
        
        self.mb.settings_proj[wahl] = farbe
        self.win.dispose()
        self.source.Model.BackgroundColor = farbe
        
        self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj)  

    def disposing(self,ev):pass   
    
    
    
class Trenner_URL_Listener(unohelper.Base, XActionListener):
    def __init__(self,mb):
        self.mb = mb
        self.url_textfeld = None
                
    def actionPerformed(self,ev):
        if self.mb.debug: log(inspect.stack)
        
        Filepicker = self.mb.createUnoService("com.sun.star.ui.dialogs.FilePicker")
        Filepicker.appendFilter('Image','*.jpg;*.JPG;*.png;*.PNG;*.gif;*.GIF')
        Filepicker.execute()
         
        if Filepicker.Files == '':
            return
    
        filepath =  uno.fileUrlToSystemPath(Filepicker.Files[0])
        
        self.url_textfeld.Model.Label = filepath
        
        self.mb.settings_proj['trenner_user_url'] = Filepicker.Files[0]
        self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj)     
                
                
                
                
                
                
                
                