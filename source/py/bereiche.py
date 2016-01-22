# -*- coding: utf-8 -*-

from com.sun.star.style.BreakType import NONE as BREAKTYPE_NONE

class Bereiche():
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)

        self.mb = mb
        self.doc = mb.doc       
        
        self.oOO = None
    
    
    def starte_oOO(self,URL=None):
        if self.mb.debug: log(inspect.stack)
         
        prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop.Name = 'Hidden'
        prop.Value = True
        
        prop2 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop2.Name = 'AsTemplate'
        prop2.Value = True
                
        if URL == None:
            URL="private:factory/swriter"
            if self.mb.settings_proj['use_template'][0] == True:
                if self.mb.settings_proj['use_template'][1] != '':
                    URL = uno.systemPathToFileUrl(self.mb.settings_proj['use_template'][1])
                
        self.oOO = self.mb.doc.CurrentController.Frame.loadComponentFromURL(URL,'_blank',0,(prop,prop2))
        
        
    def schliesse_oOO(self):
        if self.mb.debug: log(inspect.stack)
        self.oOO.close(False)
        
    
    def erzeuge_neue_Datei(self,i,inhalt):
        if self.mb.debug: log(inspect.stack)
        
        nr = str(i) 

        text = self.oOO.Text
        
        inhalt = 'nr. ' + nr + '\t' + inhalt
        
        cursor = text.createTextCursor()
        cursor.gotoStart(False)
        cursor.gotoEnd(True)
        text.insertString( cursor, '', True )

        
        newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
        newSection.setName('OrgInnerSec'+nr)
        text.insertTextContent(cursor, newSection, False)
        cursor.goLeft(1,True)
        
        text.insertString( cursor, inhalt, True )
                
        Path1 = os.path.join(self.mb.pfade['odts'] , 'nr{}.odt'.format(nr) )
        Path2 = uno.systemPathToFileUrl(Path1)      
          
        self.oOO.storeToURL(Path2,())
        self.plain_txt_speichern(inhalt, 'nr{}'.format(nr))
        
        newSection.dispose()
        
        return Path1
    
    
    def erzeuge_neue_Datei2(self,i,inhalt):
        if self.mb.debug: log(inspect.stack)
        
        try:
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True
            
            URL="private:factory/swriter"
    
            if self.mb.settings_proj['use_template'][0] == True:
                URL = uno.systemPathToFileUrl(self.mb.settings_proj['use_template'][1])
            self.oOO = self.mb.desktop.loadComponentFromURL(URL,'_blank',8+32,(prop,))
            
            nr = str(i) 
            
            text = self.oOO.Text
            
            cursor = text.createTextCursor()
            cursor.gotoStart(False)
            cursor.gotoEnd(True)

            newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
            newSection.setName('OrgInnerSec'+nr)
            text.insertTextContent(cursor, newSection, False)
            
            cursor.goLeft(2,True)
            cursor.collapseToStart()
            
            if not self.mb.debug:
                inhalt = ' '
                
            text.insertString( cursor, inhalt, True )
            
            cursor.collapseToEnd()
            cursor.goRight(2,True)
            cursor.setString('')
            
            Path1 = os.path.join(self.mb.pfade['odts'] , 'nr%s.odt' %nr )
            Path2 = uno.systemPathToFileUrl(Path1)    
    
            self.oOO.storeToURL(Path2,())
            self.plain_txt_speichern(inhalt, 'nr{}'.format(nr))
            
            self.oOO.close(False)

        except:
            log(inspect.stack,tb())
    
    
    def erzeuge_leere_datei(self):
        if self.mb.debug: log(inspect.stack)
         
        prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop.Name = 'Hidden'
        prop.Value = True
        
        URL="private:factory/swriter"
        
        dokument = self.mb.doc.CurrentController.Frame.loadComponentFromURL(URL,'_blank',0,(prop,))
        
        text = dokument.Text
        cur = text.createTextCursor()
        cur.gotoStart(False)
        
        from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
        for i in range(100):
            text.insertControlCharacter( cur, PARAGRAPH_BREAK, 0 )
            text.insertControlCharacter( cur, PARAGRAPH_BREAK, 0 )

        url = os.path.join(self.mb.pfade['odts'], 'empty_file.odt')
        dokument.storeToURL(uno.systemPathToFileUrl(url),())
        dokument.close(False)
        
        
    def leere_Dokument(self):
        if self.mb.debug: log(inspect.stack)
        
        try:
            all_sections_Namen = self.doc.TextSections.ElementNames
            if self.doc.TextSections.Count != 0:
                for name in all_sections_Namen:
                    sec = self.doc.TextSections.getByName(name)
                    sec.dispose()
            
            cursor = self.mb.viewcursor
            cursor.gotoStart(False)
            cursor.gotoEnd(True)
            cursor.setString('')
        except:
            log(inspect.stack,tb())
            
    
    def erzeuge_bereich_papierkorb(self,i,path):
        if self.mb.debug: log(inspect.stack)
        
        nr = str(i) 
        
        text = self.mb.doc.Text
        sections = self.mb.doc.TextSections  
        
        newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
        
        SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
        SFLink.FileURL = path
        SFLink.FilterName = 'writer8'
        newSection.setPropertyValue('FileLink',SFLink)
            
        newSection.setName('OrganonSec'+nr)
        
        sectionN = sections.getByIndex(sections.Count-1)
        textSectionCursor = text.createTextCursorByRange(sectionN.Anchor)
        textSectionCursor.gotoEnd(False)
        
        text.insertTextContent(textSectionCursor, newSection, False)
    
                     
    def erzeuge_bereich(self,i,path,sicht):
        if self.mb.debug: log(inspect.stack)
        
        nr = str(i) 
        
        text = self.mb.doc.Text
        sections = self.mb.doc.TextSections  
        
        newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
            
        newSection.setName('OrganonSec'+nr)
        
        if sicht == 'nein':
            newSection.IsVisible = False
            
        if sections.Count == 0:
            # bei leerem Projekt
            textSectionCursor = text.createTextCursor()
        else:
            sectionN = sections.getByIndex(sections.Count-1)
            textSectionCursor = text.createTextCursorByRange(sectionN.Anchor)
            textSectionCursor.gotoEnd(False)
        
        text.insertTextContent(textSectionCursor, newSection, False)
        
    
    def erzeuge_bereich2(self,i,sicht):
        if self.mb.debug: log(inspect.stack)
        
        nr = str(i) 

        text = self.mb.doc.Text
        sections = self.mb.doc.TextSections  
        
        alle_hotzenploetze = []
        for sec_name in sections.ElementNames:
            if 'OrganonSec' in sec_name:
                alle_hotzenploetze.append(sec_name)
        anzahl_hotzenploetze = len(alle_hotzenploetze)
        
        path = os.path.join(self.mb.pfade['odts'] , 'nr%s.odt' %nr) 
        path = uno.systemPathToFileUrl(path)
                 
        SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
        SFLink.FileURL = path#_to_Papierkorb
        SFLink.FilterName = 'writer8'

        newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
        newSection.setPropertyValue('FileLink',SFLink)
        newSection.setName('OrganonSec'+str(anzahl_hotzenploetze))

        if sicht == 'nein':
            newSection.IsVisible = False

        textSectionCursor = text.createTextCursor()
        textSectionCursor.gotoEnd(False)

        text.insertTextContent(textSectionCursor, newSection, False)

        # Der richtige Link fuer den letzten Bereich wird erst hier gesetzt, da die sec ansonsten
        # falsch eingefuegt wird (weiss der Henker, warum)
        path_to_empty = uno.systemPathToFileUrl(os.path.join(self.mb.pfade['odts'],'empty_file.odt'))
        SFLink.FileURL = path_to_empty
        newSection.setPropertyValue('FileLink',SFLink)
        
        newSection.Anchor.BreakType = BREAKTYPE_NONE


    def loesche_leeren_Textbereich_am_Ende(self):
        if self.mb.debug: log(inspect.stack)
        
        text = self.doc.Text
        cur = text.createTextCursor()
        
        cur.gotoEnd(False)
        cur.goLeft(1,True)
        cur.setString('')
       
        
    def datei_nach_aenderung_speichern(self, zu_speicherndes_doc_path, bereichsname = None, speichern = False):

        if (len(self.mb.undo_mgr.AllUndoActionTitles) > 0 and bereichsname != None) or speichern:
            # Nur loggen, falls tatsaechlich gespeichert wurde
            if self.mb.debug: log(inspect.stack)

            try:
                # Damit das Handbuch nicht geaendert wird:
                if self.mb.anleitung_geladen:
                    return
                                
                self.verlinkte_Bilder_einbetten(self.mb.doc)
                projekt_path = self.mb.doc.URL
                
                prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
                prop.Name = 'Hidden'
                prop.Value = True
                
                newDoc =  self.mb.desktop.loadComponentFromURL("private:factory/swriter",'_blank',8+32,(prop,))
                cur = newDoc.Text.createTextCursor()
                cur.gotoStart(False)
                cur.gotoEnd(True)
    
                SFLink = uno.createUnoStruct("com.sun.star.text.SectionFileLink")
                SFLink.FileURL = projekt_path
    
                newSection = self.mb.doc.createInstance("com.sun.star.text.TextSection")
                newSection.setPropertyValues(("LinkRegion",'FileLink'),(bereichsname,SFLink))
                                    
                newDoc.Text.insertTextContent(cur, newSection, True)
                newDoc.Text.removeTextContent(newSection)
                newDoc.storeToURL(zu_speicherndes_doc_path,())
                
                if '.odthelfer' not in zu_speicherndes_doc_path:
                    # plain_txt speichern
                    plain_txt = newDoc.Text.String
                    dict_bereiche = self.mb.props[T.AB].dict_bereiche
                    
                    os_path = uno.fileUrlToSystemPath(zu_speicherndes_doc_path)
                    bereich = [ n for n,p in dict_bereiche['Bereichsname'].items() if p == os_path ][0]
                    ordinal = dict_bereiche['Bereichsname-ordinal'][bereich]
                    
                    self.plain_txt_speichern(plain_txt, ordinal)

                newDoc.close(False)
    
                self.mb.loesche_undo_Aktionen()
            except:
                log(inspect.stack,tb())
                self.mb.nachricht(LANG.DATEI_NICHT_GESPEICHERT,'warningbox')
                try:
                    newDoc.close(False)
                except:
                    pass
        
    
    def plain_txt_speichern(self,plain_txt,ordinal):
        if self.mb.debug: log(inspect.stack)
        
        try:
            pfad_plain_txt = os.path.join(self.mb.pfade['plain_txt'], ordinal + '.txt')
    
            with codecs_open(pfad_plain_txt , "w","utf-8") as f:
                f.write(plain_txt)
        except:
            log(inspect.stack,tb())
            
    
    def plain_txt_loeschen(self,ordinal):
        if self.mb.debug: log(inspect.stack)
        
        try:
            pfad_plain_txt = os.path.join(self.mb.pfade['plain_txt'], ordinal + '.txt')
            os.remove(pfad_plain_txt)
        except:
            log(inspect.stack,tb())
        

    def verlinkte_Bilder_einbetten(self,doc):
        if self.mb.debug: log(inspect.stack)
        
        self.mb.selbstruf = True
        
        try:
            bilder = self.mb.doc.GraphicObjects
            bitmap = self.mb.doc.createInstance( "com.sun.star.drawing.BitmapTable" )
            
            for i in range(bilder.Count):
                bild = bilder.getByIndex(i)
                if 'vnd.sun.star.GraphicObject' not in bild.GraphicURL:
                    # Wenn die Grafik nicht gespeichert werden kann,
                    # (weil noch nicht geladen oder User hat zu frueh weitergeklickt)
                    # muesste sie eigentlich bei der naechsten Aenderung
                    # im Bereich gespeichert werden
                    try:
                        bitmap.insertByName( "TempI"+str(i), bild.GraphicURL )
                        #if self.mb.debug: print(bild.GraphicURL)
                        try:
                            internalUrl = bitmap.getByName( "TempI"+str(i) ) 
                            bild.GraphicURL = internalUrl 
                        except:
                            pass
                        bitmap.removeByName( "TempI"+str(i) ) 
                    except:
                        log(inspect.stack,tb())
        except:
            log(inspect.stack,tb())
        self.mb.selbstruf = False   
        
        
    def speicher_odt(self,pfad):
        if self.mb.debug: log(inspect.stack)
        
        try:
            prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop.Name = 'Hidden'
            prop.Value = True        
        
            prop2 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop2.Name = 'FilterName'
            prop2.Value = "HTML (StarWriter)"
    
            pfad = uno.systemPathToFileUrl(os.path.join(self.speicherordner,self.titel+'.html'))
            doc = self.doc.CurrentController.Frame.loadComponentFromURL(pfad,'_blank',0,(prop,prop2))

            prop1 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            prop1.Name = 'Overwrite'
            prop1.Value = True
            
            pfad = uno.systemPathToFileUrl(os.path.join(self.speicherordner,self.titel+'.odt'))
            doc.storeToURL(pfad,(prop1,))
            doc.close(False)
            
        except:
            log(inspect.stack,tb())


    def speicher_pdf(self):
        if self.mb.debug: log(inspect.stack)
        
        prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop.Name = 'Hidden'
        prop.Value = True        
    
        prop2 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop2.Name = 'FilterName'
        prop2.Value = "HTML (StarWriter)"

        pfad = uno.systemPathToFileUrl(os.path.join(self.speicherordner,self.titel+'.html'))
        doc = self.doc.CurrentController.Frame.loadComponentFromURL(pfad,'_blank',0,(prop,prop2))

        prop1 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop1.Name = 'Overwrite'
        prop1.Value = True
        
        
        prop3 = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop3.Name = 'FilterName'
        prop3.Value = 'writer_pdf_Export'
        
        
        pfad = uno.systemPathToFileUrl(os.path.join(self.speicherordner,self.titel+'.pdf'))
        doc.storeToURL(pfad,(prop1,prop3))
        doc.close(False)

