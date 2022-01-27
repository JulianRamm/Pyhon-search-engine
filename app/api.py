from flask import Blueprint, Response, request
import json

ping = Blueprint("ping", __name__)
product_list = Blueprint("articles", __name__)

query_params = {
    "category": "Categoría",
    "product": "Producto",
    "brand": "Marca",
    "price": "Precio",
    "freeShipping": "Envío Gratis",
    "prestige": "Prestigio"
}

@ping.route("/ping")
def pong():
    return "pong"

@product_list.route("/articles", methods=['GET'])
def get_product_list():
    try:
        with open('./products.json') as file:
            articles = json.load(file)
            valid = True
            if len(request.args) == 1 and "category" in request.args:
                category =  request.args.get("category")  
                articles = [x for x in articles if x.get("Categoría") == category] 
            elif len(request.args) in (2,3):
                args = request.args.items()
                key1, value1 = next(args)
                key2, value2 = next(args)
        
                if key1 in query_params and key2 in query_params:
                    key1 = query_params[key1]
                    key2 = query_params[key2]
                    if key1 == "Prestigio":
                        value1 = int(value1) * "*"
                    elif key2 == "Prestigio":
                        value2 = int(value2) * "*"
                    articles = [x for x in articles if x.get(key1) == value1 and x.get(key2) == value2]                
                else:
                    valid = False
                if len(request.args) == 3:
                    key3, value3 = next(args)
                    if key3 == "order" and value3 in ("0", "1", "2", "3"):
                        if value3 == "0":
                             articles.sort(key=lambda x: x.get("Producto"))
                        if value3 == "1":
                            articles.sort(key=lambda x: x.get("Producto"), reverse=True)
                        if value3 == "2":
                            articles.sort(key=lambda x: int(x.get("Precio")[1:].replace(".", "")))
                        if value3 == "3":
                            articles.sort(key=lambda x: int(x.get("Precio")[1:].replace(".", "")), reverse=True)
                    else:
                        valid = False
            if len(request.args) > 3 or not valid:
                return Response(status=400)    
            if len(articles) == 0:
                return Response(status=404)
            return Response(status=200, response=json.dumps(articles))
    except Exception as e:
        print(e)