from GooBa import Parent, Element

Card = Parent("div", className="card")

# {
#   "userId": 1,
#   "id": 1,
#   "title": "delectus aut autem",
#   "completed": false
# }

title,user_id  = Element("h3")

Card.appendChild(title, user_id)
