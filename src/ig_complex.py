#################################################################
# Created on 2 March 2020
# author: Matia Vanonni
# Python 3.7.4
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# IG Complexity Extension (i.e., extract_grammer_complexity)
# Created on 25 April 2024
# Last Updated: 31 May 2024
# author: Graham Ambrose
#################################################################

#############
### SET UP
#############

#pip install pip setuptools wheel
#pip install spacy
#python -m spacy download en
#pip install svglib
#pip install pandas
#pip install fuzzywuzzy
#pip install python-Levenshtein

import spacy
import pandas as pd
from spacy.lang.en import English
from IPython.core.display import display, HTML
nlp = spacy.load("en_core_web_sm")
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.lang.en.stop_words import STOP_WORDS
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from pathlib import Path
import os
import pandas as pd
from glob import glob
from collections import defaultdict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn import metrics
import numpy as np

#######################################################################################################################
### Vanonni CODE
#################

### recurse ############################################################################################################

def recurse(*tokens):
    children = []
    def add(tok):
        sub = tok.children
        for item in sub:
            children.append(item)
            add(item)
    for token in tokens:
       add(token)

    return children

### get_branch ##########################################################################################################

def get_branch(t,sent,include_self=True):
    branch = recurse(t)
    if include_self:
        branch += [t]
    branch = [w for w in sent if w in branch]# and w.dep_ in include]

    #print(branch)

    lemmas = []
    tags = []
    deps = []

    for token in branch:
        lemma = token.lemma_.lower()
        lemmas.append(lemma)
        tags.append(token.tag_)
        deps.append(token.dep_)

    return lemmas, tags, deps
	
### parse_by_subject ##############################################################################################################

def parse_by_subject(sent):

    subjects = [t for t in sent if t.dep_ in subdeps]
    #print(subjects)
    objects = [t for t in sent if t.dep_ in objdeps]
    #print(objects)

    datalist = []
  #  for obnum, object in enumerate(objects):
	#    object = object.lemma_
	#	data['Object'] = object
	#	datalist.append(data)

    for obnum, subject in enumerate(subjects):
        subdep = subject.dep_
        mlem = None
        verb = subject.head
        if not verb.tag_.startswith('V'):
            continue

        vlem = verb.lemma_
        vdep = verb.dep_


        tokenlists = defaultdict(list)


        neg = ''
        for t in verb.children:
            if t.tag_ == 'MD':
                mlem = t.orth_.lower()
                continue
            dep = t.dep_
            if dep in ['punct','det', 'meta', 'intj', 'dep']: #'cc',
                continue
            if dep == 'neg':
                neg = 'not'

            elif t.dep_ == 'prt':
                vlem = vlem + '_' + t.orth_.lower()

            else:

                tokenlists[dep].append(t)

        slem = subject.lemma_

        data = {
                'Attribute': slem,
       #         'Object':object,
				'Deontic':mlem,
                'neg': neg,
                'aIm': vlem,
                'aIm_d': vdep}

        if subdep == 'nsubjpass':
            data['passive'] = 1

        object_branches = []
        object_tags = []
        object_deps = []

        for dep, tokens in tokenlists.items():
            if dep in nonobjdeps:
                continue
            for t in tokens:
                tbranch, ttags, tdep = get_branch(t,sent)
                object_tags.append(ttags)
                object_branches.append(tbranch)
                object_deps.append(tdep)
        data['Object_properties'] = object_branches
        data['Object_tags'] = object_tags
        data['Object_deps'] = object_deps


        #datalist.append(data)


        subphrase, subtags, subdep = get_branch(subject,sent)

        data['Attribute_properties'] = subphrase
        data['Attribute_tags'] = subtags
        data['Attribute_deps'] = subdep

        cond_branches = []
        cond_tags = []
        cond_deps = []


        for dep, tokens in tokenlists.items():
            if dep in noncondeps:
                continue
            for t in tokens:
                tbranch, ttags, tdep = get_branch(t,sent)
                cond_tags.append(ttags)
                cond_branches.append(tbranch)
                cond_deps.append(tdep)
        data['Condition_tags'] = cond_tags
        data['Condition'] = cond_branches
        data['Condition_deps'] = cond_deps


        datalist.append(data)

    return datalist

### Dependancies #####################################################################################################

subdeps = ['nsubj','nsubjpass', 'expl', 'csubj']
objdeps = ['dobj','dative', 'iobj']
condeps = ['advmod', 'advcl', 'prep', 'prepc', 'xcomp']

maindeps = ['nsubj','nsubjpass',
              'expl', # existential there as subject
              'advmod',
              'dobj',
              'prep',
              'xcomp',
              'dative', # indirect object
              'advcl',
              'agent',
              'ccomp',
              'acomp',
              'attr',
			  'csubj',
			  'iobj',
			  'prep',
			  'prepc']

noncondeps = ['nsubj','nsubjpass',
              'expl', # existential there as subject
              'dobj',
              'dative', # indirect object
              'agent',
			  'ccomp',
              'attr',
			  'xcomp',
              'acomp']

nonobjdeps = ['nsubj','nsubjpass',
              'expl', # existential there as subject
              'advmod',
              'prep',
              'xcomp',
              'advcl',
              'agent',
              'ccomp',
              'acomp']

### extract_grammar #######################################################################################################################

voldata = []

outfile="validation_data.pkl"

#sentence_num = 0

def extract_grammar(txt):
    doc = nlp(txt)
    statements = []
    for sent in doc.sents:
        statements = parse_by_subject(sent)
        for statement in statements:
            data = statement.copy()
            data['sentence_num'] = sentence_num
            data['full_sentence'] = str(sent)
            voldata.append(data)
            sentence_num += 1 # end loop over sentences
        return statements
pd.to_pickle(voldata,outfile)

#############################################################################################################################
### Ambrose CODE
################

### extract_grammer_complexity ##############################################################################################

from re import I
def extract_grammer_complexity(txt):

    n_txt = txt

    ####################
    # Identify Entities
    ####################

    t_nlp = nlp(n_txt)
    for ent in t_nlp.ents:
        #print(ent.text, ent.label_)
        e = nlp(ent.text)
        for token in e:
          if token.tag_ == "NNP":
            replace = str(token)
            #print(replace)
            n_txt = n_txt.replace(ent.text, replace)
            break



    ############################################################################
    # identify and count aIms
    ############################################################################
    # the extractor functions much better with only one aIm, so the extra aims
    # are identified, cataloged, and removed to allow for better extraction below
    ############################################################################

    t_nlp = nlp(n_txt)
    sentence_num = 0

    for sent in t_nlp.sents:
        statements = parse_by_subject(sent)
        Statem = str(sent)
        #print(Statem)

        # make sure we are pointed at the correct parse, i.e., it needs a deontic AND it needs to be the ROOT verb
        for statement in statements:
          if  statement['aIm_d'] == "ROOT":
            #print(statement['aIm_d'])
            #print(statement)
            sentence_num += 1 # end loop over sentences

            # Aims
            Aim = [statement['aIm']]

            # Counting Aims

            Aim_Count = 1
            Aim_Conj = 'N/A'
            x = -1
            for Aim_states in statement['Object_tags']:
              x += 1
              i = -1
              for Aim_state in Aim_states:
                i += 1
                if Aim_state in ['VB', 'VBP'] and statement['Object_deps'][x][i] not in ['auxpass','acl', 'relcl', 'advcl']:
                  Aim_Count += 1
                  Aim.append(statement['Object_properties'][x][i]) # Full tasks
                  n_txt = n_txt.replace(str(statement['Object_properties'][x][i]), "")

                  # Aims Conjunction                # Only count conj. if additional aims are detected
                  x = -1
                  for ele in range(len(statement['Object_tags'])):
                    x += 1
                    Aim_state = statement['Object_tags'][x]
                    try:
                      i = Aim_state.index("CC")
                      Aim_Conj = statement['Object_properties'][x][i]
                      #txt = txt.replace(str(statement['Object_properties'][x][i]), "")
                    except ValueError:
                      skip = 1

            #print(Aim)



    ###################################################
    # Extraction with modified entities and single aIms
    ###################################################

    doc = nlp(n_txt)
    sentence_num = 0
    clean_data = pd.DataFrame(columns = ['ID', 'Statement', "Main Attribute", "Attributes Count", "Attributes Conjunction", "Coord. Actor", "Coord. Actor Count", "Deontic", "Negative", "Task", "Task Count", "Task Conjunction","Condition", "Condition Count", "Condition Conjunction"]) #, "Institutional State Complexity", "Institutional Regimentation"])

    for sent in doc.sents:
        statements = parse_by_subject(sent)
        #Statem = str(sent)
        #print(txt)

        # make sure we are pointed at the correct parse, i.e., it needs a deontic AND it needs to be the ROOT verb
        for statement in statements:
          if  statement['aIm_d'] == "ROOT":
            #print(statement['aIm_d'])
            #print(statement)
            sentence_num += 1 # end loop over sentences



            #############
            # Attributes
            #############

            Att = [statement['Attribute'].lower()]
            Att_Count = 1

            # Counting Attributes
            #print(statements[0]['Attribute_tags'])
            i = -1
            for Att_state in statement['Attribute_tags']:
              i += 1
              if Att_state in ['NN', 'NNP', 'PRP']:
                if statement['Attribute_deps'][i] not in ['compound', 'amod', 'dobj','advcl']:
                  if statement['Attribute_properties'][i] not in Att:
                    Att.append(statement['Attribute_properties'][i]) # if first actor in Attribute_properties is not already IDed as the Main Attribute
                    Att_Count += 1

            # Attribute Conjunction
            Att_state = statement['Attribute_tags']
            try:
              i = Att_state.index("CC")
              Att_Conj = statement['Attribute_properties'][i]
            except ValueError:
              Att_Conj = 'N/A'

            #print(Att)



            ###############
            # Total Actors
            ###############

            Actors = Att.copy()

            # Counting Actors
            #print(statements[0]['Attribute_tags'])
            dub_counted_list = []

            # In Conditions
            Actor_Count = Att_Count
            x = -1
            for Actor_states in statement['Condition_tags']:
              #print(Actor_states)

              x += 1
              i = -1
              for Actor_state in Actor_states:
                i += 1
                dub_counted_list.append(statement['Condition'][x])
                #if statement['Condition_deps'][x][i] in ['prep'] and statement['Condition_tags'][x][i] in ['IN']:
                  #print(statement['Condition'][x][i:])
                  #print(statement['Condition_tags'][x][i:])
                  #print(statement['Condition_deps'][x][i:])
                  #print('')

                #if Actor_state in ['NN', 'NNP', 'PRP']:
                #  if statement['Condition_deps'][x][i] in ['pobj','conj']:  # not in ['npadvmod', 'acl']: # noun is not a 'noun phrase as adverbial modifier' or 'clausal modifier of noun
                #    Actor_Count += 1
                #    print(statement['Condition_tags'][x][i])
                #    print(statement['Condition_deps'][x][i])
                #    print(statement['Condition'][x][i])
                #    Actors.append(statement['Condition'][x][i]) # Full actors

            # In Object Properties
            x = -1
            for Object_states in statement['Object_tags']:
              #print(Actor_states)
              x += 1
              i = -1
              if statement['Object_properties'][x] not in dub_counted_list:
                for Object_state in Object_states:
                  i += 1
                  dub_counted_list.append(Object_state)
                  if statement['Object_deps'][x][i] in ['prep'] and statement['Object_tags'][x][i] in ['IN']:
                    print(statement['Object_properties'][x][i:])
                    #print(statement['Object_tags'][x][i:])
                    #print(statement['Object_deps'][x][i:])
                    #print('')

            #      if Object_state in ['NN', 'NNP', 'PRP']:
            #        if statement['Object_deps'][x][i] in ['pobj','conj']:  # not in ['npadvmod', 'acl']: # noun is not a 'noun phrase as adverbial modifier' or 'clausal modifier of noun
            #          Actor_Count += 1
            #          #print(statement['Object_tags'][x][i])
            #          #print(statement['Object_deps'][x][i])
            #          #print(statement['Object_properties'][x][i])
            #          Actors.append(statement['Object_properties'][x][i]) # Full actors

            #print(Actors)



            ##########
            # Deontic
            ##########

            Deon = statement['Deontic']
            if statement['neg'] != '':
              Neg = statement['neg']
            else:
              Neg = 'N/A'



            #####################
            # Counting Conditions
            #####################

            #print(statements[0]['Condition'])
            Con_Conj = ['N/A']
            Con = []
            Con_Count = 0
            list_num = -1
            for Cond_state in statement['Condition']:
              list_num += 1

              if len(statement['Condition'][list_num]) < 3: # don't count miss-splitting of conjunctions
                  continue
              else:
                  Con_Count += 1
                  if statement['Condition'][list_num] not in Con:
                    Con.append(statement['Condition'][list_num])

              for word in Cond_state:
                  if word in ['or', 'and']:
                      Con_Count += 1

                      if Con_Conj[0] == 'N/A':  # add conjunction to first position if the first position is 'n/a'
                        Con_Conj[0] = str(word)
                      else:
                        Con_Conj.append(str(word))  # appemd conjunction to the list otherwise


                      for word in Cond_state:
                        if word in [',']:
                          Con_Count += 1



            #################################
            # Institutional State Complexity
            #################################

            #if Con_Count == 0:
            #  ISC = Con_Count
            #elif Con_Conj == "and":     # Should an
            #  ISC = Con_Count
            #else:
            #  ISC = 1



            ##############################
            # Institutional Regimentation
            ##############################

            #if Aim_Conj == "and":
            #  IReg = Aim_Count/1
            #elif Aim_Conj == "or":     # Should an
            #  IReg = Aim_Count/((2**Aim_Count)-1)
            #else:
            #  IReg = 1



            ####################################
            # append rows to an empty DataFrame
            ####################################

            clean_data = clean_data._append({'ID':sentence_num, 'Statement':txt, "Main Attribute":Att, "Attributes Count":Att_Count, "Attributes Conjunction":Att_Conj, "Coord. Actor":Actors, "Coord. Actor Count":Actor_Count, "Deontic":Deon, "Negative":Neg, "Task":Aim, "Task Count":Aim_Count, "Task Conjunction":Aim_Conj, "Condition": Con, "Condition Count":Con_Count, "Condition Conjunction":Con_Conj}, ignore_index=True) #, "Institutional State Complexity":ISC, "Institutional Regimentation":IReg}, ignore_index=True)
            #print('ID:', sentence_num, 'Statem:', sent, "Attributes Count:", Att_Count, "Attributes Conjunction:", Att_Conj, "Deontic:", Deon, "Negative:", Neg,, "Aim Count:", Aim_Count, "Aim Conjunction:", Aim_Conj, "Condition Count:", Con_Count, "Condition Conjunction:", Con_Conj)
            #print(" ")

    return clean_data

### extract_grammer_complexity_dataset #############################################################################################

from re import I
def extract_grammer_complexity_dataset(dataset, id, s):

  clean_data = pd.DataFrame(columns = ['ID', 'Statement', "Main Attribute", "Attributes Count", "Attributes Conjunction", "Coord. Actor", "Coord. Actor Count", "Deontic", "Negative", "Task", "Task Count", "Task Conjunction","Condition" ,"Condition Count", "Condition Conjunction"]) #, "Institutional State Complexity", "Institutional Regimentation"])
  sentence_num = 0

  for x in range(len(dataset)):
      #print(dataset.iloc[x][s])
      txt = (dataset.iloc[x][s])
      ID = (dataset.iloc[x][id])


      ##############

      n_txt = txt

      ####################
      # Identify Entities
      ####################

      t_nlp = nlp(n_txt)
      for ent in t_nlp.ents:
          #print(ent.text, ent.label_)
          e = nlp(ent.text)
          for token in e:
            if token.tag_ == "NNP":
              replace = str(token)
              #print(replace)
              n_txt = n_txt.replace(ent.text, replace)
              break



      ############################################################################
      # identify and count aIms
      ############################################################################
      # the extractor functions much better with only one aIm, so the extra aims
      # are identified, cataloged, and removed to allow for better extraction below
      ############################################################################

      t_nlp = nlp(n_txt)


      for sent in t_nlp.sents:
          statements = parse_by_subject(sent)
          Statem = str(sent)
          #print(Statem)

          # make sure we are pointed at the correct parse, i.e., it needs a deontic AND it needs to be the ROOT verb
          for statement in statements:
            if  statement['aIm_d'] == "ROOT":
              sentence_num += 1
              #print(statement['aIm_d'])
              #print(statement)

              # Aims
              Aim = [statement['aIm']]

              # Counting Aims
              #print(statements[0]['Object_tags'])
              Aim_Count = 1
              Aim_Conj = 'N/A'
              x = -1
              for Aim_states in statement['Object_tags']:
                x += 1
                i = -1
                for Aim_state in Aim_states:
                  i += 1
                  if Aim_state in ['VB', 'VBP'] and statement['Object_deps'][x][i] not in ['auxpass','acl', 'relcl', 'advcl']:
                    Aim_Count += 1
                    Aim.append(statement['Object_properties'][x][i]) # Full tasks
                    n_txt = n_txt.replace(str(statement['Object_properties'][x][i]), "")

                    # Aims Conjunction                # Only count conj. if additional aims are detected
                    x = -1
                    for ele in range(len(statement['Object_tags'])):
                      x += 1
                      Aim_state = statement['Object_tags'][x]
                      try:
                        i = Aim_state.index("CC")
                        Aim_Conj = statement['Object_properties'][x][i]
                        #txt = txt.replace(str(statement['Object_properties'][x][i]), "")
                      except ValueError:
                        skip = 1

              #print(Aim)



      ###################################################
      # Extraction with modified entities and single aIms
      ###################################################

      doc = nlp(n_txt)


      for sent in doc.sents:
          statements = parse_by_subject(sent)
          #Statem = str(sent)
          #print(txt)

          # make sure we are pointed at the correct parse, i.e., it needs a deontic AND it needs to be the ROOT verb
          for statement in statements:
            if  statement['aIm_d'] == "ROOT":
              #print(statement['aIm_d'])
              #print(statement)


              #############
              # Attributes
              #############

              Att = [statement['Attribute'].lower()]
              Att_Count = 1

              # Counting Attributes
              #print(statements[0]['Attribute_tags'])
              i = -1
              for Att_state in statement['Attribute_tags']:
                i += 1
                if Att_state in ['NN', 'NNP', 'PRP']:
                  if statement['Attribute_deps'][i] not in ['compound', 'amod', 'dobj']:
                    if statement['Attribute_properties'][i] not in Att:
                      Att.append(statement['Attribute_properties'][i]) # if first actor in Attribute_properties is not already IDed as the Main Attribute
                      Att_Count += 1

              # Attribute Conjunction
              Att_state = statement['Attribute_tags']
              try:
                i = Att_state.index("CC")
                Att_Conj = statement['Attribute_properties'][i]
              except ValueError:
                Att_Conj = 'N/A'

              #print(Att)



              ###############
              # Total Actors
              ###############

              Actors = Att.copy()

              # Counting Actors
              #print(statements[0]['Attribute_tags'])
              dub_counted_list = []

              # In Conditions
              Actor_Count = Att_Count
              x = -1
              for Actor_states in statement['Condition_tags']:
                #print(Actor_states)

                x += 1
                i = -1
                for Actor_state in Actor_states:
                  i += 1
                  dub_counted_list.append(statement['Condition'][x])
                  #if statement['Condition_deps'][x][i] in ['prep'] and statement['Condition_tags'][x][i] in ['IN']:
                    #print(statement['Condition'][x][i:])
                    #print(statement['Condition_tags'][x][i:])
                    #print(statement['Condition_deps'][x][i:])
                    #print('')

                  #if Actor_state in ['NN', 'NNP', 'PRP']:
                  #  if statement['Condition_deps'][x][i] in ['pobj','conj']:  # not in ['npadvmod', 'acl']: # noun is not a 'noun phrase as adverbial modifier' or 'clausal modifier of noun
                  #    Actor_Count += 1
                  #    print(statement['Condition_tags'][x][i])
                  #    print(statement['Condition_deps'][x][i])
                  #    print(statement['Condition'][x][i])
                  #    Actors.append(statement['Condition'][x][i]) # Full actors

              # In Object Properties
              x = -1
              for Object_states in statement['Object_tags']:
                #print(Actor_states)
                x += 1
                i = -1
                if statement['Object_properties'][x] not in dub_counted_list:
                  for Object_state in Object_states:
                    i += 1
                    dub_counted_list.append(Object_state)
                    #if statement['Object_deps'][x][i] in ['prep'] and statement['Object_tags'][x][i] in ['IN']:
                      #print(statement['Object_properties'][x][i:])
                      #print(statement['Object_tags'][x][i:])
                      #print(statement['Object_deps'][x][i:])
                      #print('')

              #      if Object_state in ['NN', 'NNP', 'PRP']:
              #        if statement['Object_deps'][x][i] in ['pobj','conj']:  # not in ['npadvmod', 'acl']: # noun is not a 'noun phrase as adverbial modifier' or 'clausal modifier of noun
              #          Actor_Count += 1
              #          #print(statement['Object_tags'][x][i])
              #          #print(statement['Object_deps'][x][i])
              #          #print(statement['Object_properties'][x][i])
              #          Actors.append(statement['Object_properties'][x][i]) # Full actors

              #print(Actors)



              ##########
              # Deontic
              ##########

              Deon = statement['Deontic']
              if statement['neg'] != '':
                Neg = statement['neg']
              else:
                Neg = 'N/A'



              #####################
              # Counting Conditions
              #####################

              #print(statements[0]['Condition'])
              Con_Conj = ['N/A']
              Con = []
              Con_Count = 0
              list_num = -1
              for Cond_state in statement['Condition']:
                list_num += 1

                if len(statement['Condition'][list_num]) < 3: # don't count miss-splitting of conjunctions
                    continue
                else:
                    Con_Count += 1
                    if statement['Condition'][list_num] not in Con:
                      Con.append(statement['Condition'][list_num])

                for word in Cond_state:
                  if word in ['or', 'and']:
                      Con_Count += 1

                      if Con_Conj[0] == 'N/A':  # add conjunction to first position if the first position is 'n/a'
                        Con_Conj[0] = str(word)
                      else:
                        Con_Conj.append(str(word))  # appemd conjunction to the list otherwise


                      for word in Cond_state:
                        if word in [',']:
                          Con_Count += 1



              #################################
              # Institutional State Complexity
              #################################

              #if Con_Count == 0:
              #  ISC = Con_Count
              #elif Con_Conj == "and":     # Should an
              #  ISC = Con_Count
              #else:
              #  ISC = 1



              ##############################
              # Institutional Regimentation
              ##############################

              #if Aim_Conj == "and":
              #  IReg = Aim_Count/1
              #elif Aim_Conj == "or":     # Should an
              #  IReg = Aim_Count/((2**Aim_Count)-1)
              #else:
              #  IReg = 1



              ####################################
              # append rows to an empty DataFrame
              ####################################

              clean_data = clean_data._append({'ID':ID, 'Statement':txt, "Main Attribute":Att, "Attributes Count":Att_Count, "Attributes Conjunction":Att_Conj, "Coord. Actor":Actors, "Coord. Actor Count":Actor_Count, "Deontic":Deon, "Negative":Neg, "Task":Aim, "Task Count":Aim_Count, "Task Conjunction":Aim_Conj, "Condition":Con , "Condition Count":Con_Count, "Condition Conjunction":Con_Conj}, ignore_index=True) #, "Institutional State Complexity":ISC, "Institutional Regimentation":IReg}, ignore_index=True)
              #print('ID:', sentence_num, 'Statem:', sent, "Attributes Count:", Att_Count, "Attributes Conjunction:", Att_Conj, "Deontic:", Deon, "Negative:", Neg,, "Aim Count:", Aim_Count, "Aim Conjunction:", Aim_Conj, "Condition Count:", Con_Count, "Condition Conjunction:", Con_Conj)
              #print(" ")

  return clean_data

######################################################################################################################
### CLEANING FUNCTIONS
######################

def construct_dataset(data,id,txt): # data to load, position of the ID column, position of the text column, new name

  data_text = pd.DataFrame({'Statement ID' : [],
                         'Statements' : []})

  data_text['Statement ID']=data.iloc[:, id].apply(int)
  data_text['Statements']=data.iloc[:, txt].apply(str)

  return data_text[['Statement ID','Statements']]

import re
from re import I


def clean_format(dataset, s):

  for x in range(len(dataset)):
    txt = (dataset.iloc[x][s])
    txt = re.sub("[\(].?[\)]", "", txt) # Remove '(?)'
    txt = re.sub("[\(].?.?[\)]", "", txt) # Remove '(??)'
    txt = re.sub("\[", "", txt) # Remove '['
    txt = re.sub("\]", "", txt) # Remove ']'
    txt = re.sub("\“", "", txt) # Remove '“'
    txt = re.sub("\”", "", txt) # Remove '”'

    dataset.iat[x,s] = txt


def clean_split_period(dataset):

    x = dataset.assign(Statements=dataset['Statements'].str.split('\. [A-Z][^A-Z]*')).explode('Statements') # Split on period-space-upper case
    return x


def clean_split_semicolon(dataset):

    x = dataset.assign(Statements=dataset['Statements'].str.split('\; ')).explode('Statements') # Split on period-space-upper case
    return x


def clean_split_X(dataset, split_term):

    x = dataset.assign(Statements=dataset['Statements'].str.split(split_term)).explode('Statements') # Split on a string/natural expression
    return x


def merge_statements(dataset):
  x = pd.DataFrame({'Statement ID': '1' ,
                    'Statements': [''.join(dataset['Statements'].str.strip('"').tolist())]})
  return x


def reset_index(dataset):
  dataset = dataset.reset_index(drop=True)
  return dataset
