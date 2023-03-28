from pymongo import MongoClient
from face_attendence import rectangle_detect
client  = MongoClient('mongodb+srv://root:1234@cluster0.ytoesmw.mongodb.net/?retryWrites=true&w=majority')
db = client.information

# post = {"name":"김태경", " idnumber":"940203-1054321"}
# db.ID.insert_one(post)


# file_name = rectangle_detect('./image/id_4.jpg')

# with open(f'{file_name}.txt', 'r', encoding='UTF-8') as f:
#     text = f.read()
#     doc = {
#         "filename":f'{file_name}.txt',
#         "id_info":text
#     }
#     db.ID.insert_one(doc)
# print(file_name)

# all_users = list(db.ID.find({},{'_id':False}))		# 밖에 list() 씌워줘야함!!
# print(all_users[0])

user = db.ID.find_one({"name":"김태경"},{'_id':False})
print(user)