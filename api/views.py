from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["quickbite"]
collection = db["menus"]

class MenuList(APIView):
#get/api/menus
#get all+search+filter
    def get(self, request):
        query = {}

        restaurant = request.GET.get("restaurant")
        category = request.GET.get("category")
        available = request.GET.get("available")

        if restaurant:
            query["restaurant_name"] = restaurant

        if category:
            query["category"] = category

        if available:
            query["is_available"] = available.lower() == "true"

        menus = []
        for menu in collection.find(query):
            menu["_id"] = str(menu["_id"])
            menus.append(menu)

        return Response(menus)

#post/api/menus
#create menu
    def post(self, request):
        data = request.data

        required = [
            "restaurant_name",
            "menu_name",
            "category",
            "price",
            "spicy_level",
            "is_available",
            "description"
        ]

        for field in required:
            if field not in data:
                return Response({"error": f"{field} is required"}, status=400)

        data["created_at"] = datetime.utcnow()

        result = collection.insert_one(data)

        data["_id"] = str(result.inserted_id)

        return Response(data, status=201)



class MenuDetail(APIView):

#get/api/menus/id
    def get(self, request, id):
        menu = collection.find_one({"_id": ObjectId(id)})

        if not menu:
            return Response({"error": "Menu not found"}, status=404)

        menu["_id"] = str(menu["_id"])

        return Response(menu)


#put/api/menus/id
    def put(self, request, id):
        result = collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": request.data}
        )

        if result.matched_count == 0:
            return Response({"error": "Menu not found"}, status=404)

        menu = collection.find_one({"_id": ObjectId(id)})
        menu["_id"] = str(menu["_id"])

        return Response(menu)


#delete/api/menus/id
    def delete(self, request, id):
        result = collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            return Response({"error": "Menu not found"}, status=404)

        return Response({"message": "Menu deleted"})