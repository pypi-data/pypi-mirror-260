import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
import xml.etree.ElementTree as ET
from .customresponse import CustomResponse
from datetime import datetime, timezone
from .commonfunctions import rfplogger
import time
import json

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

##### Prepare the GraphQL MUTATIONS

queryPublicationID='''
    {
      publications(first: 5) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    '''

mutationstagedUploadsCreate = '''
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
    stagedUploadsCreate(input: $input) {
        stagedTargets {
        url
        resourceUrl
        parameters {
            name
            value
        }
        }
        userErrors {
        field
        message
        }
    }
    }
    '''

mutationbulkOperationRunMutation = '''
    mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!) {
    bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
        bulkOperation {
            id
            status
        }
            userErrors {
                field
                message
        }
    }
    }
    '''

######################### GRAPHQL FUNCTIONS

def Shopify_get_metaobject_gid(shop="", access_token="", api_version="2024-01", metaobject_type="", handle=""):

    # print(f"Access token: {access_token}")

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # print(f"headers: {headers}")

    query = """
    query GetMetaobjectByHandle($type: String!, $handle: String!) {
      metaobjectByHandle(handle: {
            type: $type,
            handle: $handle
        }) {
            id
            type
            handle
        }
    }
    """
    
    variables = {
        "type": metaobject_type,
        "handle": handle
    }
    
    payload = {
        'query': query,
        'variables': variables
    }

    # print(f"payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    # response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        result_id = response_json['data']['metaobjectByHandle']['id']
        return result_id
    else:
        print(f"Error: {response.status_code}")
        return None

def Shopify_update_metaobject(shop="", access_token="", api_version="2024-01", metaobject_gid="", banner_url="", mobile_banner_url="", product_url="", metaobject_banner_number=1):
    # Push to shopify banner object for vinzo
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Generate field names based on metaobject_banner_number
    field_names = [f"product_link_{metaobject_banner_number}",
                   f"banner_url_{metaobject_banner_number}",
                   f"mobile_banner_url_{metaobject_banner_number}"
    ]

    print(field_names)

    mutation = """
    mutation UpdateMetaobject($id: ID!, $metaobject: MetaobjectUpdateInput!) {
    metaobjectUpdate(id: $id, metaobject: $metaobject) {
        metaobject {
        handle
        """
    
    # Add dynamic field names to the mutation
    for field_name in field_names:
        mutation += f"{field_name}: field(key: \"{field_name}\") {{ value }}\n"

    mutation += """
        }
        userErrors {
        field
        message
        code
        }
    }
    }
    """

    variables = { 
        "id": metaobject_gid,
        "metaobject": {
            "fields": [
                {"key": field_name, "value": value}
                for field_name, value in zip(field_names, [product_url, banner_url, mobile_banner_url])
            ]
        } 
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error loading to shopify: {response.status_code}")
        return (f"Error loading to shopify: {response.status_code}")

def Shopify_get_products(shop="", access_token="", api_version="2024-01", number_products=0):

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/products.json?limit=250"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    all_products = []
    i = 0
    while url:
        if number_products != 0 and i*250 > number_products: break
        i+=1
        print(i)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            message=f"Failed to retrieve products: {response.text}"
            print(message)
            return CustomResponse(data=message, status_code=response.status_code)
        
        products=response.json()['products']
        all_products.extend(products)
        links = response.headers.get('Link', None)
        next_url = None
        if links:
            for link in links.split(','):
                if 'rel="next"' in link:
                    next_url = link.split(';')[0].strip('<>')
                    next_url = next_url.strip('<> ')
                    break
            url = next_url if next_url else None
        else:
            break
        
    return CustomResponse(data=all_products, status_code=200)
    
def Shopify_get_collections(shop="", access_token="", api_version="2024-01"):

    url_custom = f"https://{shop}.myshopify.com/admin/api/{api_version}/custom_collections.json"
    url_smart = f"https://{shop}.myshopify.com/admin/api/{api_version}/smart_collections.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url_smart, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve smart collections: {response.status_code}")
        print(f"response {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    smart_collections = response.json()['smart_collections']
    
    response = requests.get(url_custom, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve custom collections: {response.status_code}")
        print(f"response {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    custom_collections = response.json()['custom_collections']
    
    all_collections = smart_collections + custom_collections

    return CustomResponse(data=all_collections, status_code=200)

def Shopify_get_collection_metadata(shop="", access_token="", api_version="2024-01", collection_id=""):
    '''Returns metafields and metadata'''
    metadata_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}.json"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(metadata_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve metadata for collection ID {collection_id}. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return CustomResponse(data=response.text, status_code=400)
    
    collection_metadata = response.json()['collection']
    
    # Retrieve metafields for the collection
    metafields_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}/metafields.json"
    response = requests.get(metafields_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve metafields for collection ID {collection_id}. Status code: {response.status_code}")
        print(f"Metafields response: {response.text}")
        return CustomResponse(data=response.text, status_code=400)
    metafields_data = response.json()['metafields']

    # Join metadata and metafield 
    collection_metadata['metafields'] = metafields_data

    # print(f"collection_metadata: {collection_metadata}")

    return CustomResponse(data=collection_metadata, status_code=200)

def Shopify_get_collection_url(shop="", access_token="", api_version="2024-01", collection_id=""):    
    collection_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}"
    response = requests.get(collection_url)    
    if response.status_code == 200:
        return CustomResponse(data=collection_url, status_code=200)
    else:
        # Handle the case where the URL does not exist
        return CustomResponse(data="Collection URL does not exist", status_code=404)

def Shopify_get_products_in_collection(shop="", access_token="", api_version="2024-01", collection_id=""):

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}/products.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    all_products = []

    while url:

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            products=response.json()['products']
            all_products.extend(products)
            links = response.headers.get('Link', None)

            next_url = None
            if links:
                for link in links.split(','):
                    if 'rel="next"' in link:
                        next_url = link.split(';')[0].strip('<>')
                        next_url = next_url.strip('<> ')
                        break
                url = next_url if next_url else None
            else:
                break


        else:
            print(f"Failed to retrieve products in collection {collection_id}: {response.status_code}")
            return CustomResponse(data=response.text, status_code=400)

    return CustomResponse(data=all_products, status_code=200)

def Shopify_get_product_variants(shop="", access_token="", api_version="2024-01", product_id=""):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/products/{product_id}/variants.json"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        variants=response.json()['variants']
        return CustomResponse(data=variants, status_code=200)
    else:
        print(f"Failed to retrieve product variants for product {product_id}: {response.status_code}")
        return CustomResponse(data=response.text, status_code=400)

def Shopify_get_customers(shop="", access_token="", api_version="2024-01"):
    # Endpoint URL for fetching customers
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/customers.json"
    
    # Headers for the request, including the required access token for authentication
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Making the GET request to the API
    response = requests.get(url, headers=headers)
    
    # Check the response status code
    if response.status_code != 200:
        # If the request was not successful, print an error message and return a custom response
        print(f"Failed to retrieve customers: {response.status_code}")
        print(f"response: {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    
    # If the request was successful, parse the JSON response to get the customers
    customers = response.json()['customers']
    
    # Return a custom response containing the customers and a successful status code
    return CustomResponse(data=customers, status_code=200)

def Shopify_get_products_with_metafields(shop="", access_token="", api_version="2024-01", metafield_key="custom.unpublish_after", filterdate="23/02/2024"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Initialize variables for pagination
    cursor = None
    filtered_products = []
    
    i = 0
    while True:
        print(f"Getting products... {i}", end='\r', flush=True)
        i += 1
        # Construct GraphQL query with pagination
        query = '''
        query ($cursor: String) {
            products(first: 250, after: $cursor) {
                edges {
                    node {
                        id
                        title
                        metafield(key: "%s") {
                            value
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        ''' % (metafield_key)

        # Send request to Shopify GraphQL API
        response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
        
        if response.status_code != 200:
            error_message = f"Failed to retrieve products with metafields: {response.status_code}"
            print(error_message)
            return CustomResponse(data=error_message, status_code=400)
        
        products = response.json()['data']['products']['edges']
        page_info = response.json()['data']['products']['pageInfo']
        cursor = page_info['endCursor'] if page_info['hasNextPage'] else None
              
        for product in products:
            # Attempt to retrieve the 'metafield' if it exists, otherwise use an empty dictionary
            metafield = product['node'].get('metafield') or {}
            metafield_value = metafield.get('value', '')
            
            if metafield_value:
                try:
                    # Convert the metafield value string to a datetime object
                    metafield_date = datetime.strptime(metafield_value, '%Y-%m-%dT%H:%M:%S%z')
                    # Convert the filter string to a datetime object
                    filter_date = datetime.strptime(filterdate, '%d/%m/%Y').replace(tzinfo=timezone.utc)
                    
                    if metafield_date < filter_date:
                        filtered_products.append({
                            'id': product['node']['id'],
                            'title': product['node']['title'],
                            'unpublish_metafield': metafield_value
                        })
            
                except ValueError as e:
                    print(f"Error parsing date for product {product['node']['id']}: {e}")

        if not page_info['hasNextPage']:
            break

    return CustomResponse(data=filtered_products, status_code=200)

def Shopify_get_products_and_inventoryid_with_metafields(shop="", access_token="", api_version="2024-01", metafield_key="custom.unpublish_after", filterdate="23/02/2024"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Initialize variables for pagination
    cursor = None
    filtered_products = []
    
    i = 0
    while True:
        print(f"Getting products and inventory id... {i}", end='\r', flush=True)
        i += 1
        # Construct GraphQL query with pagination and include variant inventory_item_id
        query = '''
        query ($cursor: String) {
            products(first: 250, after: $cursor) {
                edges {
                    node {
                        id
                        title
                        descriptionHtml
                        productType
                        status
                        tracksInventory
                        bodyHtml
                        productCategory {
                            productTaxonomyNode
                            {
                                id
                                name
                                fullName
                            }
                        }
                        metafield(key: "%s") {
                            value
                        }
                        variants(first: 250) {
                            edges {
                                node {
                                    id
                                    inventoryItem {
                                        id
                                    }
                                }
                            }
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        ''' % (metafield_key)

        # Send request to Shopify GraphQL API
        response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
        
        if response.status_code != 200:
            error_message = f"Failed to retrieve products with metafields: {response.status_code}"
            print(error_message)
            return CustomResponse(data=error_message, status_code=400)
        
        #rfplogger(i)
        #rfplogger(response.json())
        
        products = response.json()['data']['products']['edges']
        page_info = response.json()['data']['products']['pageInfo']
        cursor = page_info['endCursor'] if page_info['hasNextPage'] else None

        for product in products:
            # Attempt to retrieve the 'metafield' if it exists, otherwise use an empty dictionary
            metafield = product['node'].get('metafield') or {}
            metafield_value = metafield.get('value', '')
            
            variant_inventory_ids = [variant['node']['inventoryItem']['id'] for variant in product['node']['variants']['edges']]
            
            if metafield_value:
                try:
                    # Convert the metafield value string to a datetime object
                    metafield_date = datetime.strptime(metafield_value, '%Y-%m-%dT%H:%M:%S%z')
                    # Convert the filter string to a datetime object
                    filter_date = datetime.strptime(filterdate, '%d/%m/%Y').replace(tzinfo=timezone.utc)
                    
                    if metafield_date < filter_date:
                        filtered_products.append({
                            'id': product['node']['id'],
                            'title': product['node']['title'],
                            'unpublish_metafield': metafield_value,
                            'variant_inventory_item_ids': variant_inventory_ids
                        })
            
                except ValueError as e:
                    print(f"Error parsing date for product {product['node']['id']}: {e}")

        if not page_info['hasNextPage']:
            break
        
        #print("Wait 3 seconds...")
        time.sleep(3) # Query takes 288 tokens, wait 3 seconds so never deplete

    return CustomResponse(data=filtered_products, status_code=200)

def Shopify_unpublish_products_channel(shop="", access_token="", api_version="2024-01", products=[], channel_id=""):
    
    '''
    Upublishes products for a channel id by removing from channel id
    '''

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Prepare the GraphQL mutation for unpublishing products
    mutation = '''
    mutation publishableUnpublish($id: ID!, $input: [PublicationInput!]!) {
      publishableUnpublish(id: $id, input: $input) {
        userErrors {
          field
          message
        }
      }
    }
    '''
    allpublished = True
    for product in products:
        variables = {
            # "id": f"gid://shopify/Product/{product['id']}",
            "id": product['admin_graphql_api_id'],
            "input": [{
                "publicationId": channel_id
            }]
        }
        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            errors = response.json().get('errors', [])  
            if errors:
                allpublished=False
                continue

            # data = response.json().get('data', {})
            # print(f"Product {product['id']} unpublished successfully.")
        else:
            allpublished=False
            print(f"Failed to unpublish product {product['id']}: {response.status_code}")

    message = "All products were unpublished correctly"
    if allpublished != True:
        message = "Not all products were unpublished correctly"

    return CustomResponse(data=message, status_code=200)

def Shopify_get_online_store_channel_id(shop="", access_token="", api_version="2024-01"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"

    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token,
    }
    query = '''
    {
      publications(first: 250) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    '''
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        publications = data['data']['publications']['edges']
        for publication in publications:
            if publication['node']['name'] == 'Online Store':
                return publication['node']['id']
    return None

def BORRAR_Shopify_bulk_set_inventory_to_zero(shop="", access_token="", api_version="2024-01", inventory_item_ids="", location_id=""):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # GraphQL mutation to set inventory quantities to zero
    mutation = '''
    mutation inventoryBulkAdjustQuantityAtLocation($inventoryItemAdjustments: [InventoryAdjustItemInput!]!, $locationId: ID!) {
      inventoryBulkAdjustQuantityAtLocation(inventoryItemAdjustments: $inventoryItemAdjustments, locationId: $locationId) {
        inventoryLevels {
          id
          available
        }
        userErrors {
          field
          message
        }
      }
    }
    '''

    # Preparing the adjustments input for the GraphQL mutation
    adjustments = [{"inventoryItemId": item_id, "availableDelta": -9999} for item_id in inventory_item_ids]

    variables = {
        "inventoryItemAdjustments": adjustments,
        "locationId": location_id
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        print("Inventory set to zero successfully.")
    else:
        print(f"Failed to set inventory to zero: {response.status_code}")

def Shopify_reduce_inventory_by_9999(shop="", access_token="", api_version="2024-01", inventory_item_ids="", location_id=""):
    # inventory_item_ids = ["inventory-item-id-1", "inventory-item-id-2"]  # List of inventory item IDs

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # GraphQL mutation to set inventory quantities to zero
    mutation = '''
    mutation inventoryBulkAdjustQuantityAtLocation($inventoryItemAdjustments: [InventoryAdjustItemInput!]!, $locationId: ID!) {
      inventoryBulkAdjustQuantityAtLocation(inventoryItemAdjustments: $inventoryItemAdjustments, locationId: $locationId) {
        inventoryLevels {
          id
          available
        }
        userErrors {
          field
          message
        }
      }
    }
    '''
    # Preparing the adjustments input for the GraphQL mutation
    adjustments = [{"inventoryItemId": item_id, "availableDelta": -9999} for item_id in inventory_item_ids]
    print(adjustments)
    variables = {
        "inventoryItemAdjustments": adjustments,
        "locationId": location_id
        
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    rfplogger(response.json())
    if response.status_code == 200:
        message="Inventory set to zero successfully."
        print(message)
        return CustomResponse(data=message, status_code=200)
        
    else:
        message=f"Failed to set inventory to zero: {response.status_code}"
        print(message)
        return CustomResponse(data=message, status_code=400)

def Shopify_set_inventory_to_zero(shop="", access_token="", api_version="2024-01", inventory_item_ids="", location_id="", reason="correction", reference_document_uri=""):
    
    # Loop through each chunk and make the API call
    for chunk in chunker(inventory_item_ids, 250):

        url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': access_token
        }

        # GraphQL mutation to set inventory quantities to zero
        mutation = '''
        mutation inventorySetOnHandQuantities($input: InventorySetOnHandQuantitiesInput!) {
        inventorySetOnHandQuantities(input: $input) {
            inventoryAdjustmentGroup {
            id
            }
            userErrors {
            field
            message
            }
        }
        }
        '''
        # Build the setQuantities input dynamically
        #set_quantities = [{"inventoryItemId": item_id, "locationId": location_id, "quantity": 0} for item_id in inventory_item_ids]
        set_quantities = [{"inventoryItemId": item_id, "locationId": location_id, "quantity": 0} for item_id in chunk]

        variables = {
            "input": {
                "reason": reason,
                #"referenceDocumentUri": reference_document_uri,
                "setQuantities": set_quantities
            }
        }

        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
        
        if response.status_code != 200:
            message = f"Failed to set inventory to zero for chunk: {response.status_code}"
            print(message)
            return CustomResponse(data=message, status_code=400)

        print("Waiting...")
        rfplogger(response.json())
        time.sleep(2)

    message="Inventory set to zero successfully for all items."
    print(message)
    rfplogger(response.json())
    return CustomResponse(data=message, status_code=200)
    
def Shopify_get_locations(shop="", access_token="", api_version="2024-01"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/locations.json"
    headers = {"X-Shopify-Access-Token": access_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return CustomResponse(data=response.json()['locations'], status_code=200)  # Returns a list of locations
    else:
        print(f"Failed to retrieve locations: {response.status_code}")
        return CustomResponse(data="", status_code=400)
    
def Shopify_get_publication_id(shop="", access_token="", api_version="2024-01", name="Online Store"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }
    
    response = requests.post(url, json={'query': queryPublicationID}, headers=headers)
    publications = response.json().get('data', {}).get('publications', {}).get('edges', [])
    for pub in publications:
        # print(f"Publication ID: {pub['node']['id']}, Name: {pub['node']['name']}")
        # If looking for the default online store publication, you might compare by name
        if pub['node']['name'] == name:
            publication_id = pub['node']['id']
            # print(f"Found Online Store Publication ID: {publication_id}")
    return publication_id

def Shopify_get_publications(shop="", access_token="", api_version="2024-01"):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    
    query = '''
    {
      publications(first: 5) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    '''
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }
    response = requests.post(url, json={'query': query}, headers=headers)
    return response.json()

def Shopify_start_bulk_operation(shop, access_token, api_version, products):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token,
    }

    # Define your bulk operation query here
    # This is a simplified placeholder example
    bulk_operation_query = '''
    mutation {
        bulkOperationRunQuery(
            query: """
            {
                products {
                    edges {
                        node {
                            id
                            title
                            # Add fields to update here
                        }
                    }
                }
            }
            """
        ) {
            bulkOperation {
                id
                status
            }
            userErrors {
                field
                message
            }
        }
    }
    '''

    response = requests.post(url, json={'query': bulk_operation_query}, headers=headers)
    response_json = response.json()

    # Extract the operation ID and return it for polling
    operation_id = response_json['data']['bulkOperationRunQuery']['bulkOperation']['id']
    return operation_id

def Shopify_poll_bulk_operation_status(shop, access_token, api_version, operation_id):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token,
    }

    check_status_query = '''
    query {
        currentBulkOperation {
            id
            status
            errorCode
            completedAt
            objectCount
            fileSize
            url
            partialDataUrl
        }
    }
    '''

    while True:
        response = requests.post(url, json={'query': check_status_query}, headers=headers)
        response_json = response.json()
        current_operation_id = response_json['data']['currentBulkOperation']['id']
        operation_status = response_json['data']['currentBulkOperation']['status']

        # Check if the current operation ID matches the one we're interested in
        if current_operation_id != operation_id:
            print(f"Current operation ID ({current_operation_id}) does not match the expected operation ID ({operation_id}).")
            # Handle this situation, e.g., by breaking or continuing to poll
            break

        if operation_status == 'COMPLETED':
            results_url = response_json['data']['currentBulkOperation']['url']
            return results_url
        elif operation_status == 'FAILED':
            # Handle failure here
            print("Bulk operation failed.")
            break
        else:
            print("Bulk operation is still processing...")
            time.sleep(10)  # Poll every 10 seconds

def Shopify_bulk_unpublish_products(shop, access_token, api_version, product_ids, channel_id):
    """
    Bulk unpublish Shopify products.

    :param api_url: The Shopify GraphQL API URL, e.g., 'https://your-shop.myshopify.com/admin/api/2022-01/graphql.json'
    :param headers: Dictionary containing headers with API credentials, e.g., {'Content-Type': 'application/json', 'X-Shopify-Access-Token': 'your-access-token'}
    :param product_ids: List of product IDs to unpublish.
    """

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token,
    }

    # STEP 1: CREATE THE JSONL FILE
    # Create and write to the JSONL file
    file_path='unpublish_products.jsonl'
    with open(file_path, 'w') as file:
        for product_id in product_ids:
            # Construct the line as a dictionary
            line_dict = {
                "id": f"{product_id}",
                "input": {
                    "publicationId": channel_id
                }
            }
            # Convert the dictionary to a JSON string and write it to the file
            json_line = json.dumps(line_dict)
            file.write(f"{json_line}\n")

    print(f"JSONL file created and saved to {file_path}")

    # STEP 2: UPLOAD JSONL FILE TO SHOPIFY
    print(f"Uploading JSONL file")
    # GraphQL mutation for stagedUploadsCreate
    mutation = '''
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
    stagedUploadsCreate(input: $input) {
        stagedTargets {
        url
        resourceUrl
        parameters {
            name
            value
        }
        }
        userErrors {
        field
        message
        }
    }
    }
    '''

    # Define the input for the mutation
    variables = {
        "input": [
            {
                "filename": "unpublish_products.jsonl",
                "mimeType": "text/jsonl", #"text/jsonl" "application/jsonl"
                "httpMethod": "POST",
                "resource": "BULK_MUTATION_VARIABLES" #FILE  BULK_MUTATION_VARIABLES
            }
        ]
    }

    # Send the request to create a staged upload
    print(f"Creating staged upload...")
    response = requests.post(url, headers=headers, data=json.dumps({'query': mutation, 'variables': variables}))

    # Check response
    if response.status_code != 200:
        message="Failed to create staged upload."
        print(message)
        return CustomResponse(data=message, status_code=response.status_code)

    response_json=response.json()
    if 'errors' in response_json:
        error_message = response_json['errors'][0]['message']
        # Log the error message or handle it as needed
        message=f"Error received: {error_message}"
        print(message)
        return CustomResponse(data=message, status_code=400)

    print(f"Staged upload created.")

    upload_url = response_json['data']['stagedUploadsCreate']['stagedTargets'][0]['url']
    upload_parameters = response_json['data']['stagedUploadsCreate']['stagedTargets'][0]['parameters']
    resource_url = response_json['data']['stagedUploadsCreate']['stagedTargets'][0]['resourceUrl']

    #print(f"Upload url: {upload_url}")
    #print(f"Upload parameters: {upload_parameters}")
    #print(f"Resource url: {resource_url}")

    print(f"Uploading JSONL...")
    multipart_data = MultipartEncoder(
        fields={**{param['name']: param['value'] for param in upload_parameters}, 'file': ('unpublish_products.jsonl', open(file_path, 'rb'), 'text/jsonl')}
    )

    #print(f"Multipart data: {multipart_data}")

    response = requests.post(upload_url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    if response.status_code not in [200, 201]:
        message=f"Failed to upload file. Status Code: {response.status_code} Response: {response.text}"
        print(message)
        return CustomResponse(data=message, status_code=response.status_code)

    print("File uploaded successfully.")

    key_value = next((param['value'] for param in upload_parameters if param['name'] == 'key'), None)
    staged_upload_path=key_value

    # STEP 3: EXECUTE THE MUTATION

    mutation_string = """
        mutation publishableUnpublish($id: ID!, $input: [PublicationInput!]!) {
        publishableUnpublish(id: $id, input: $input) {
            userErrors {
            field
            message
            }
        }
        }
        """

    # The GraphQL mutation for running a bulk operation
    bulk_mutation = '''
    mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!) {
    bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
        bulkOperation {
            id
            status
        }
            userErrors {
                field
                message
        }
    }
    }
    '''  

    # Variables to be passed with the mutation
    variables = {
        "mutation": mutation_string,
        "stagedUploadPath": staged_upload_path
    }

    # Make the GraphQL POST request to start the bulk operation
    response = requests.post(url, headers=headers, json={'query': bulk_mutation, 'variables': variables})

    # Inspect the response
    if response.status_code != 200:
        message=f"Failed to initiate bulk operation. {response.text}. Status code: {response.status_code}"
        print(message)
        return CustomResponse(data=message, status_code=response.status_code)    

    print("Bulk operation initiated successfully.")
     
    ## STEP 4 WAIT UNTIL FINISHED
    query = '''
    {
    currentBulkOperation {
        id
        status
        errorCode
        completedAt
    }
    }
    '''

    while True:
        response = requests.post(url, headers=headers, json={'query': query})
        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['currentBulkOperation']:
                current_status = response_json['data']['currentBulkOperation']['status']
                if current_status == 'COMPLETED':
                    print("Bulk operation completed.")
                    break
                elif current_status == 'RUNNING':
                    print("Bulk operation is still running. Checking again in 10 seconds...")
                    time.sleep(5)
                else:
                    print(f"Bulk operation status: {current_status}")
                    break
            else:
                print("No current bulk operation found. It might have not started properly or already finished.")
                break
        else:
            print(f"Failed to query bulk operation status. Status code: {response.status_code}")
            break
    
    return CustomResponse(data="OK", status_code=200)


def Shopify_process_handle(input_string):
    '''
    Returns handle in allowed shopify format
    '''
    # Convert ASCII control codes 0 to 32 and specific symbols to spaces to later convert them to hyphens
    for i in range(33):
        input_string = input_string.replace(chr(i), ' ')
    input_string = re.sub(r'[!#$%&*+,./:;<=>?@\\^`{|}~]', ' ', input_string)
    
    # Remove disallowed characters
    input_string = re.sub(r'["\'()\[\]]', '', input_string)
    
    # Convert spaces and hyphens to a placeholder, and then convert that placeholder to hyphens
    input_string = re.sub(r'[\s-]+', '-', input_string)
    
    # Remove placeholder hyphens at the end of the string
    input_string = re.sub(r'-+$', '', input_string)
    
    # Convert uppercase letters to lowercase
    input_string = input_string.lower()
    
    return input_string

def Shopify_execute_bulk_mutation(shop="", access_token="", api_version="", mutation="", staged_upload_path=""):
    
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    variables = {
        "mutation": mutation,
        "stagedUploadPath": staged_upload_path
    }

    # Make the GraphQL POST request to start the bulk operation
    response = requests.post(url, headers=headers, json={'query': mutationbulkOperationRunMutation, 'variables': variables})

    # Inspect the response
    if response.status_code != 200:
        message=f"Failed to initiate bulk operation. {response.text}. Status code: {response.status_code}"
        print(message)
        return CustomResponse(data=message, status_code=response.status_code)    

    print("Bulk operation initiated successfully.")
    print(response.text)
    
    ## STEP 4 WAIT UNTIL FINISHED
    query = '''
    {
    currentBulkOperation(type: MUTATION) {
        id
        status
        errorCode
        completedAt
    }
    }
    '''

    while True:
        response = requests.post(url, headers=headers, json={'query': query})
        
        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['currentBulkOperation']:
                current_status = response_json['data']['currentBulkOperation']['status']
                if current_status == 'COMPLETED':
                    print("Bulk operation completed.")
                    break
                elif current_status == 'RUNNING':
                    print("Bulk operation is still running. Checking again in 10 seconds...")
                    time.sleep(10)
                else:
                    print(f"Bulk operation status: {current_status}")
                    break
            else:
                print("No current bulk operation found. It might have not started properly or already finished.")
                break
        else:
            print(f"Failed to query bulk operation status. Status code: {response.status_code}")
            break

    print(response.text)
    return CustomResponse(data=response.text, status_code=response.status_code)  

def Shopify_upload_jsonl(shop="", access_token="", api_version="", file_path=""):
    # GraphQL mutation for stagedUploadsCreate
    mutation=mutationstagedUploadsCreate

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Define the input for the mutation
    variables = {
        "input": [
            {
                "filename": file_path,
                "mimeType": "text/jsonl", 
                "httpMethod": "POST",
                "resource": "BULK_MUTATION_VARIABLES" 
            }
        ]
    }

    # Send the request to create a staged upload
    print(f"Creating staged upload...")
    response = requests.post(url, headers=headers, data=json.dumps({'query': mutation, 'variables': variables}))
    
    # Check response
    if response.status_code != 200:
        message="Failed to create staged upload."
        print(message)
        return CustomResponse(data=message, status_code=response.status_code)

    response_json=response.json()
    if 'errors' in response_json:
        error_message = response_json['errors'][0]['message']
        # Log the error message or handle it as needed
        message=f"Error received: {error_message}"
        print(message)
        return CustomResponse(data=message, status_code=400)

    print(f"Staged upload created.")

    upload_url = response_json['data']['stagedUploadsCreate']['stagedTargets'][0]['url']
    upload_parameters = response_json['data']['stagedUploadsCreate']['stagedTargets'][0]['parameters']
    resource_url = response_json['data']['stagedUploadsCreate']['stagedTargets'][0]['resourceUrl']

    print(f"Uploading JSONL...")
    multipart_data = MultipartEncoder(
        fields={**{param['name']: param['value'] for param in upload_parameters}, 'file': (file_path, open(file_path, 'rb'), 'text/jsonl')}
    )

    response = requests.post(upload_url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    if response.status_code not in [200, 201]:
        message=f"Failed to upload file. Status Code: {response.status_code} Response: {response.text}"
        print(message)
        return CustomResponse(data=message, status_code=response.status_code)

    print("File uploaded successfully.")

    key_value = next((param['value'] for param in upload_parameters if param['name'] == 'key'), None)
    staged_upload_path=key_value

    return CustomResponse(data=staged_upload_path, status_code=200)

def Shopify_bulk_update_products(shop="", access_token="", api_version="", file_path="", mutation=""):
    """
    Bulk update Shopify products

    """

    # UPLOAD JSONL FILE TO SHOPIFY
    print(f"Uploading JSONL file")
    custom_response=Shopify_upload_jsonl(shop=shop, access_token=access_token, api_version=api_version, file_path=file_path)
    if custom_response.status_code!=200:
        message=f"Error creating staged response: {custom_response.data}"
        print(message)
        return CustomResponse(data=message, status_code=400)
    staged_upload_path = custom_response.data
    print(f"Staged upload path: {staged_upload_path}")

    # EXECUTE THE MUTATION
    custom_response=Shopify_execute_bulk_mutation(shop=shop, access_token=access_token, api_version=api_version, mutation=mutation, staged_upload_path=staged_upload_path)
    
    return CustomResponse(data=custom_response.data, status_code=custom_response.status_code)


###################### SPECIFIC FUNCTIONS
    
def Shopify_get_marketing_customer_list(shop="", access_token="", api_version="2024-01"):
    ''' Returns a dictionary with 2 lists, customer who are subscribe to email marketing and cutomers subscribed to SMS marketing'''
    # Assume Shopify_get_customers is defined elsewhere and correctly returns customer data
    response = Shopify_get_customers(shop, access_token, api_version)
    
    # Initialize dictionaries to hold subscribers
    marketing_lists = {
        'newsletter_subscribers': [],
        'sms_marketing_subscribers': []
    }
    
    # Proceed only if the response was successful
    if response.status_code != 200:
        print("Failed to retrieve customers. Status Code:", response.status_code)
        return response

    # Iterate through the customer data
    for customer in response.data:
        email_marketing_consent = customer.get('email_marketing_consent')
        if email_marketing_consent and email_marketing_consent.get('state') == 'subscribed':
            marketing_lists['newsletter_subscribers'].append({
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'email': customer.get('email', '')
            })
        
        sms_marketing_consent = customer.get('sms_marketing_consent')
        # Adjusted to check if sms_marketing_consent is not None and then proceed
        if sms_marketing_consent and sms_marketing_consent.get('state') == 'subscribed':
            marketing_lists['sms_marketing_subscribers'].append({
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'email': customer.get('email', '')  # Assuming you want the email for SMS subscribers
            })
    
    return CustomResponse(data=marketing_lists, status_code=200)
    
def Shopify_set_stock_zero_metafield_unpublish(shop="", access_token="", api_version="2024-01", metafield_key="custom.unpublish_after", filter_date="", reason="correction", reference_document_uri=""):
    '''
    Set stock to zero for all products with custom.unpublish_after 
    less than the in the filter_date
    '''
    # GET PRODUCTS AND RELATED INVENTORY ID WITH METAFIELD VALUE. 
    # Has to get all products in store in batches of 250, takes 3 seconds per batch
    custom_response = Shopify_get_products_and_inventoryid_with_metafields(shop=shop, access_token=access_token, api_version="2024-01", metafield_key=metafield_key, filterdate=filter_date)
    if custom_response.status_code != 200:
        error_message = "Error getting product with metafield value"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)

    filtered_products = custom_response.data
    
    # GET INVENTORY ITEMS FOR ALL VARIANTS
    inventory_item_ids = [item_id for product in filtered_products for item_id in product['variant_inventory_item_ids']]
    # GET INVENTORY LOCATION
    custom_response = Shopify_get_locations(shop=shop, access_token=access_token, api_version="2024-01")
    if custom_response.status_code!=200:
        error_message = "Error getting locations"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    locations = custom_response.data
    if locations:
        # Take the first location from the list
        first_location = locations[0]  # Access the first item in the list
        location_id = first_location['id']
        location_id = f"gid://shopify/Location/{location_id}"
    else:
        error_message = "Error No locations found."
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    # SET STOCK TO ZERO. VERY FAST, JUST 1 MUTATION WITH ALL INVENTORY ITEMS
    reference_document_uri = ""
    custom_response=Shopify_set_inventory_to_zero(shop=shop, access_token=access_token, api_version="2024-01", inventory_item_ids=inventory_item_ids, location_id=location_id, reason=reason, reference_document_uri=reference_document_uri)
    if custom_response.status_code != 200:
        error_message = "Error setting inventory to zero"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    return CustomResponse(data="All OK", status_code=200)

    # GET PRODUCTS WITH METAFIELD VALUE. Has to get all products in store in batches of 250
    #custom_response = Shopify_get_products_with_metafields(shop=shop, access_token=access_token, api_version="2024-01", metafield_key=metafield_key, filterdate=filter_date)
    #if custom_response.status_code != 200:
    #    error_message = "Error getting product with metafield value"
    #    print(error_message)
    #    return CustomResponse(data=error_message, status_code=400)

    # Extracting just the numerical ID part from each product's 'id' field
    product_ids = [product['id'].split('/')[-1] for product in filtered_products]

    # GET INVENTORY ITEMS FOR EACH PRODUCT id. Loops for each product, takes a long time!
    inventory_item_ids = []
    for product_id in product_ids:
        custom_response = Shopify_get_product_variants(shop=shop, access_token=access_token, api_version="2024-01", product_id=product_id)
        
        # Check if variants were retrieved successfully
        if custom_response.status_code !=200:
                error_message = "Error getting variants"
                print(error_message)
                return CustomResponse(data=error_message, status_code=400)
        
        variants=custom_response.data

        for variant in variants:
            inventory_gid = f"gid://shopify/InventoryItem/{variant['inventory_item_id']}"
            inventory_item_ids.append(inventory_gid)
 
    # GET INVENTORY LOCATION
    custom_response = Shopify_get_locations(shop=shop, access_token=access_token, api_version="2024-01")
    if custom_response.status_code!=200:
        error_message = "Error getting locations"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    locations = custom_response.data
    if locations:
        # Take the first location from the list
        first_location = locations[0]  # Access the first item in the list
        location_id = first_location['id']
        location_id = f"gid://shopify/Location/{location_id}"
    else:
        error_message = "Error No locations found."
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    # SET STOCK TO ZERO. VERY FAST, JUST 1 MUTATION WITH ALL INVENTORY ITEMS
    reference_document_uri = ""
    custom_response=Shopify_set_inventory_to_zero(shop=shop, access_token=access_token, api_version="2024-01", inventory_item_ids=inventory_item_ids, location_id=location_id, reason=reason, reference_document_uri=reference_document_uri)
    if custom_response.status_code != 200:
        error_message = "Error setting inventory to zero"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    return CustomResponse(data="All OK", status_code=200)

def Shopify_collection_unpublish(shop="", access_token="", api_version="2024-01", collection_id=""):
    
    # GET PRODUCTS IN COLLECTION   
    print(f"Collection id: {collection_id}") 
    custom_response = Shopify_get_products_in_collection(shop=shop, access_token=access_token, collection_id=collection_id)
    if custom_response.status_code!= 200:
        error_message="Couldn't get products from collection"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    products = custom_response.data
    print(f"Total products in collection {len(products)}")
    
    # Filter products already unpublished to speed up
    # Filter wasn't working,
    # products = [product for product in products if product['published_at'] is not None]
    print(f"Total unpublished products in collection {len(products)}")

    channel_id = Shopify_get_online_store_channel_id(shop=shop, access_token=access_token, api_version=api_version) 
    
    # Bulk unpublish
    product_ids = [product['admin_graphql_api_id'] for product in products]
    custom_response=Shopify_bulk_unpublish_products(shop=shop, access_token=access_token, api_version=api_version, product_ids=product_ids, channel_id=channel_id)
    if custom_response!=200:
        return CustomResponse(data=custom_response.data, status_code=custom_response.status_code)
    
    message=f"Collection {collection_id}: {len(products)} products unpublished successfully."
    return CustomResponse(data=message, status_code=200)

    # UNPUBLISH PRODUCTS FROM COLLECTION BY CHANNEL ID
    
    custom_response = Shopify_unpublish_products_channel(shop=shop, access_token=access_token, api_version=api_version, products=products, channel_id=channel_id)
    if custom_response.status_code != 200:
        error_message="Couldn't unpublish products"
        print(error_message)
        return CustomResponse(data=error_message, status_code=400)
    
    message=f"Collection {collection_id}: {len(products)} products unpublished successfully."
    return CustomResponse(data=message, status_code=200)