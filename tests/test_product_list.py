from flask import url_for
from http import HTTPStatus
import json

def test_product_list__products_were_fetched_successfully__list_of_products_is_returned(client):
    response = client.get(url_for("articles.get_product_list"))
    assert HTTPStatus.OK == response.status_code

def test_product_list__a_problem_occurred_while_fetching_articles__response_500_is_returned(client, mocker):
    with mocker.patch('builtins.open', side_effect=FileNotFoundError):      
        response = client.get(url_for("articles.get_product_list")) 
        assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code

def test_product_list__an_unexistant_category_param_value_is_received__response_404_is_returned(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Any") 
    assert HTTPStatus.NOT_FOUND == response.status_code

def test_product_list__an_existant_category_param_is_received__responses_list_of_length_3(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes") 
    gotten_elements = json.loads(response.data)
    assert HTTPStatus.OK == response.status_code
    assert len(gotten_elements) == 5

""" def test_product_list__invalid_query_param_received__responses_bad_request_error(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"quantity=5") 
    assert HTTPStatus.BAD_REQUEST == response.status_code """

def test_product_list__3_query_params_received__responses_bad_request_error(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"product=Short"+"&brand=Lacoste") 
    assert HTTPStatus.BAD_REQUEST == response.status_code

def test_product_list__1_of_2_query_params_received_does_not_exists__responses_bad_request_error(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"none=5") 
    assert HTTPStatus.BAD_REQUEST == response.status_code

def test_product_list__query_params_received_are_valid__responses_ok_and_the_matching_list(client):
    response = client.get(url_for("articles.get_product_list")+"?product=Short&"+"brand=Lacoste") 
    assert HTTPStatus.OK == response.status_code

def test_product_list__param_order_equals_to_0__ascending_ordered_list_is_returned(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"brand=Adidas"+"&order=0")
    gotten_elements = json.loads(response.data) 
    for i in range(0, len(gotten_elements)-1):
        assert gotten_elements[i].get("Producto") < gotten_elements[i+1].get("Producto")

def test_product_list__param_order_equals_to_1__descending_ordered_list_is_returned(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"brand=Adidas"+"&order=1")
    gotten_elements = json.loads(response.data) 
    for i in range(0, len(gotten_elements)-1):
        assert gotten_elements[i].get("Producto") > gotten_elements[i+1].get("Producto")


def test_product_list__param_order_equals_to_2__ascending_order_list_by_price_is_returned(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"brand=Adidas"+"&order=2")
    gotten_elements = json.loads(response.data) 
    for i in range(0, len(gotten_elements)-1):
        assert int(gotten_elements[i].get("Precio")[1:].replace(".", "")) < int(gotten_elements[i+1].get("Precio")[1:].replace(".", ""))

def test_product_list__param_order_equals_to_3__descending_order_list_by_price_is_returned(client):
    response = client.get(url_for("articles.get_product_list")+"?category=Deportes&"+"brand=Adidas"+"&order=3")
    gotten_elements = json.loads(response.data)
    for i in range(0, len(gotten_elements)-1):
        assert int(gotten_elements[i].get("Precio")[1:].replace(".", "")) > int(gotten_elements[i+1].get("Precio")[1:].replace(".", ""))
