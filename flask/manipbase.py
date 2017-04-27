from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from scv2func import *
import string
from datetime import date

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')

metadata = MetaData(scv2_engine)

tables = importContext(scv2_engine,metadata)

#OK BOYS ! GO SESSION, MAPPING, INFINITE POOOOWERRR !!! 

Session = sessionmaker(bind=scv2_engine) # Session class

session = Session() # object constructor

mapAll(tables)

#has this worked ?

print ('=====================================================')
print ('|	      Trying out the session !	  	    |')
print ('=====================================================')


alfredo = User()
alfredo.firstname='alfredo'
alfredo.lastname='freccino'
alfredo.username='freccifredo'
alfredo.birthdate = date(1978,11,24)
alfredo.mail = 'fredoIlPomodoro@italia.it'
alfredo.password = 'unamozzarella'

session.add(alfredo)
session.add(alfredo)
print(session.new,'\n')

session.flush()
session.commit()

for user in session.query(User):
	print(user.firstname,user.lastname)

print("\nIl y a peut-être des doublons ! Supprimons les ?\n")

for user in session.query(User).filter(User.firstname.like('alfredo')).all():
	count = session.query(User).filter(User.firstname.like('alfredo')).count()
	print(count)
	if(count > 1):
		session.delete(user)



session.flush()
session.commit()

for user in session.query(User):
	print(user.firstname,user.lastname)

print('\n\nAllons itérer en recherche alphabétique par queries ! :D\n')

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
	for itemtype in session.query(Itemtype.type_name):
		for item in alphaSearch(session,Item,Itemtype,letter,itemtype[0]):
			print("Un(e)",itemtype[0]," commençant par la lettre",letter,"est:", item.title)
			print("\nCeux qui y ont participé:\n")
			for participant,participation in queryAllParticipantsInfo(session,Item,Participant,Participation,item.title):
				print(participant.firstname,participant.lastname,"| leur role:",participation.role)

			print('\n')



# REQUETES AVEC SELECT TOUJOURS DISPONIBLES ! 

# print ("<><><><><><><> Requêtes et companie ;) <><><><><><><>\n")

# item_type = tables['item_type']
# item = tables['item']
# item_type = tables['item_type']
# notation = tables['notation']
# interest = tables['interest']
# participant = tables['participant']
# participation = tables['participation']
# vote = tables['vote']
# distinction = tables['distinction']
# event = tables['event']

# conn = scv2_engine.connect()

# for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':

#     WOW = alphaItemSearch(tables,conn,letter,'Film')

#     for wows in WOW:
#         print("Films de la base de donnée commençant par ",letter," : ",wows)



# s = select([item.c.title])

# for titles in conn.execute(s):
#     print('------------------')
#     print(titles[0])
#     print('------------------')
#     for data in getAllParticipants(tables,conn,titles[0]):
#         print(data)


# conn.close()
