import sys
import re
import fio
import xml.etree.ElementTree as ET

import phraseClusteringKmedoid
import SennaParser
import CourseMirror_Survey
import global_params
import os
import fio

def WriteDocsent(phrasedir, datadir, cid, sheets, types):
    for sheet in sheets:
        for type in types:
            responses_filename = os.path.join(phrasedir, str(sheet), '%s.sentence.dict'%(type))
            
            if not fio.IsExist(responses_filename):
                print '%s not exist'%responses_filename
                continue
            
            responses_dict = fio.LoadDict(responses_filename, int)
            
            DID = str(sheet) + '_' + type
            
            path = os.path.join(datadir, str(sheet), type, 'docsent/')
            fio.NewPath(path)
            filename = os.path.join(path, DID + '.docsent')
            
            #create a XML file
            root = ET.Element(tag='DOCSENT', attrib = {'DID':DID, 'LANG':"ENG"})
            root.tail = '\n'
            tree = ET.ElementTree(root)
            
            par = 1
            sno_id = 1
            for sentence, count in responses_dict.items():
                
                RSNT = 1
                for c in range(count):
                    node = ET.Element(tag='S', attrib={'PAR':str(par), 'RSNT':str(RSNT), 'SNO':str(sno_id)})
                    node.text = sentence
                    node.tail = '\n'
                    root.append(node)
                    sno_id = sno_id + 1
                    par += 1
            
            tree.write(filename)
            
def WriteCluster(phrasedir, datadir, cid, sheets, types):
    for type in types:
        for sheet in sheets:
            
            student_summaryList = CourseMirror_Survey.getStudentResponseList(excelfile, course, week, type, withSource=True)
            if len(student_summaryList) == 0: continue
            
            path = os.path.join(datadir, str(sheet), type)
            fio.NewPath(path)
            filename = os.path.join(path, type + '.cluster')
            
            #create a XML file
            root = ET.Element(tag='CLUSTER', attrib = {'LANG':"ENG"})
            root.tail = '\n'
            tree = ET.ElementTree(root)
        
            DID = str(sheet) + '_' + type
            
            node = ET.Element(tag='D', attrib={'DID':str(DID)})
            node.tail = '\n'
            root.append(node)
        
            tree.write(filename)
            
def Write2Mead(phrasedir, datadir, cid, sheets, types):
    #assume one week is a one document
    WriteDocsent(phrasedir, datadir, cid, sheets, types)
    WriteCluster(phrasedir, datadir, cid, sheets, types)
                
if __name__ == '__main__':
    
    from config import ConfigFile
    
    cid = sys.argv[1]
    config = ConfigFile(config_file_name='config_%s.txt'%cid)
    
    phrasedir = "../../data/"+cid+"/MC/"
    
    datadir = "../data/"+cid+ '/MEAD/'
    fio.DeleteFolder(datadir)
    
    sheets = global_params.lectures[cid]
    types=config.get_types()
    
    Write2Mead(phrasedir, datadir, cid, sheets, types)
            
    #Step5: get PhraseMead output
    
    print "done"