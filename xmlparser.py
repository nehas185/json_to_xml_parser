import json
import os
from xml.etree import ElementTree as ET
from lxml import objectify


def update_system_filter(xml_file_path,tmp_path):
    #read system filter xml file
    tree=ET.parse(xml_file_path)
    #get the root tag of the xml file
    root=tree.getroot()

    #create list of jsons file from tmp path
    json_list = []
    for r, d, f in os.walk(tmp_path):
        for file in f:
            if ".json" in file:
                p = os.path.join(r, file)
                json_list.append(p)
    print "json_list : ",json_list

    #start parsing the json files
    for conf_path in json_list:
        print("conf_path: ", conf_path)
        #read conf file
        conf_dict = {}     
        with open(conf_path, 'r') as f:
	        conf_dict = json.load(f)
		#print(conf_dict)

        k=[]      
        if conf_dict.has_key('actions'):
            actions=conf_dict['actions']
            #print "action_path: ",actions 
            for action in actions:                      
                if action.has_key('rules'):                    
                    rules = action['rules']                    
                    if not rules.has_key('id'):
                        #print "action_path: "
                        continue
                    evid=rules['id']                    
                    if not rules.has_key('rname_r2'):                        
                        continue
                    rname=rules['rname_r2']
                    if not rules.has_key('rulec_'):                        
                        continue
                    rcondn=rules['rulec_']                    
                    for event_block in root:
                            new_rule=0
	                    event_tag=event_block.tag                           
	                    event_id=event_tag.split('_')[1]                                                  
	                    if (event_id==evid):
                                   # import pdb
                                   # pdb.set_trace()                                    
				    for rule in event_block :
			                    if(rule[1].text==rcondn):
                                                    new_rule =1
				                    print('Rule already exists!')
				                    break
                                    if(new_rule==0):        
			               new=ET.SubElement(event_block,'rule')
			               n1=ET.SubElement(new,'rname')
			               n1.text=rname
			               n2=ET.SubElement(new,'rulec_')
			               n2.text=rcondn
			               ET.dump(new)
			               tree.write('system.xml')
               #     print("Removing the json file from :",conf_path)
               #     os.remove(conf_path)



#update_system_filter(xml file path,json file path)
update_system_filter("system.xml","./tmp")

