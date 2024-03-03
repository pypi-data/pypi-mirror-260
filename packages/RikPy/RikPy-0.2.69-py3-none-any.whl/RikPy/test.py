from .commonheroku import heroku_environment, heroku_upload_file_from_url, heroku_list_files_in_folder, heroku_download_files_in_folder, heroku_delete_file
from .commonshopify import (Shopify_get_collection_url, Shopify_get_marketing_customer_list, 
    Shopify_get_customers, Shopify_get_collection_metadata, 
    Shopify_get_product_variants, Shopify_get_products_in_collection, 
    Shopify_get_metaobject_gid, Shopify_update_metaobject, 
    Shopify_get_collections, Shopify_get_products_with_metafields, Shopify_get_online_store_channel_id,
    Shopify_collection_unpublish, Shopify_set_inventory_to_zero, Shopify_get_locations, Shopify_set_inventory_to_zero,
    Shopify_set_stock_zero_metafield_unpublish)
from .commons3 import s3_download_files_in_folder, s3_list_files_in_folder, s3_environment, s3_upload_file_from_url, s3_upload_local_file, s3_delete_file
import json
import boto3
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import requests
from .commonfunctions import download_file_local, send_email, send_email_with_credentials, rfplogger
from .commonopenai import OpenAI_generate_image, OpenAI_generate_response
from .commonlogging import configure_logger

logger = configure_logger()

b_test_heroku = False
b_test_shopify = True
b_test_s3 = False
b_test_openai = False
b_test_email = False

if b_test_email:
    email_type="Info"
    email_message="Mensaje de prueba"
    email_subject="Subject"
    originator="RikPy"
    smtp_server="smtp.zoho.eu"
    smtp_port="587"
    smtp_user="hello@vinzo.uk"
    smtp_pass="T6P6rZa0ZxFN"
    email_recipient="rfornp@gmail.com"
    error_email_recipient="rfornp@gmail.com"
    #send_email(email_type=email_type, email_message=email_message, originator=originator)
    send_email_with_credentials(smtp_server=smtp_server, smtp_port=smtp_port, smtp_user=smtp_user, smtp_pass=smtp_pass, email_recipient=email_recipient, email_subject=email_subject, email_message=email_message, originator=originator)

if b_test_shopify:

    load_dotenv()  # This loads the environment variables from .env
    shop = os.getenv("SHOPIFY_ETW_SHOP")
    access_token = os.getenv("SHOPIFY_ETW_TOKEN")
    api_version = os.getenv("SHOPIFY_ETW_API_VERSION")


    collection_id='618927915343' # ETW unpublish collection
    location_id="gid://shopify/Location/89243976015"
    
    custom_response = Shopify_get_locations(shop=shop, access_token=access_token, api_version=api_version)
    print(custom_response.data)
    print(custom_response.status_code)

    exit()

    ######### Test unpublish collection 
    custom_response = Shopify_collection_unpublish(shop=shop,access_token=access_token, api_version="2024-01", collection_id=collection_id)
    if custom_response.status_code != 200:
        print("Error")
    rfplogger(custom_response.data)
    exit()

    ########## Test set stock zero metafield unpublish_after
    metafield_key = "custom.unpublish_after"
    filter_date = '31/1/2024'
   
    custom_response=Shopify_set_stock_zero_metafield_unpublish(shop=shop, access_token=access_token, api_version="2024-01", metafield_key=metafield_key, filter_date=filter_date)
    if custom_response.status_code != 200:
        print("Error")
        exit()

    ########## Test GET PRODUCTS VARIANTS (needs prodcut object from get prodcuts function)
    # load products using some function
    products = []
    variants_list=[]
    for product in products:
        first_product_id = products[0]['id']
        custom_response = Shopify_get_product_variants(shop=shop, access_token=access_token, product_id=first_product_id)
        if custom_response!=200:
            print("Shopify_get_product_variants Failed to retrieve variants for the first product")    
            break
        
        variants = custom_response.data
        # Extract the price of the first variant
        print(variants[0])
        first_variant_price = variants[0].get('price')
        first_variant_compare_price = variants[0].get('compare_at_price')
        
        # Print the price
        print("Price of the first variant:", first_variant_price)
        print(first_variant_compare_price)
        print(f"Shopify_get_product_variants: {custom_response.status_code}")
        variants_list.append([variants[0]])


    ######### Test unpublish a collection
    # CONFIGURE COLLECTION IN SHOPIFY AND .ENV
    collection_id='618927915343'
    custom_response= Shopify_collection_unpublish(shop=shop, access_token=access_token, collection_id=collection_id)
    print(custom_response.data)

    ######### Test get online store id for unpublishing
    channel_id = Shopify_get_online_store_channel_id(shop=shop, access_token=access_token, api_version="2024-01")
    print(channel_id)
    
    
    filtered_products = [{'id': 'gid://shopify/Product/8896747569487', 'title': 'Campillo Rosé 2021', 'unpublish_metafield': '2023-01-26T08:00:00Z'}]
    ########## Test retrieve products by metafield
    custom_response = Shopify_get_products_with_metafields(shop=shop, access_token=access_token, api_version="2024-01", metafield_key="custom.unpublish_after", filterdate='31/1/2024')
    if custom_response.status_code != 200:
        print("Error")
        exit()
    filtered_products = custom_response.data
    total_product_count = len(filtered_products)
    print(f"Filtered products: {filtered_products}")
    print(f"Total products: {total_product_count}")

    rfplogger(f"filtered_products: {filtered_products}")
    ########## Test unpublish product list by id
    custom_response = Shopify_unpublish_products(shop=shop, access_token=access_token, api_version="2024-01", filtered_products=filtered_products, channel_id=channel_id)
    

    #print(products_with_metafields)
    #print("Total product count with metafields:", total_product_count)    
    exit()
    
    ########## Test shopify multibanner load
    metaobject_type = 'product_banner'
    metaobject_handle = 'vinzo-3-product-banner'
    collection_id = '450597257527'
    collection_id = '473739166007'
    
    image1_url="https://getaiir.s3.eu-central-1.amazonaws.com/wine/20240129215403_1dc3765c.png"
    image2_url="https://getaiir.s3.eu-central-1.amazonaws.com/wine/20240129215346_a08a387b.png"
    image2_url="https://getaiir.s3.eu-central-1.amazonaws.com/wine/20240129212907_38873eb0.png"

    custom_response = Shopify_get_collection_url(shop=shop, access_token=access_token, api_version="2024-01", collection_id=collection_id)    

    print(custom_response.data)

    custom_response = Shopify_get_collection_metadata(shop=shop, access_token=access_token, api_version="2024-01", collection_id=collection_id)
    print(f"Shopify_get_collection_metadata: {custom_response.data}")

    exit()

    # GET CUSTOMERS
    #custom_response=Shopify_get_customers(shop=shop, access_token=access_token, api_version="2024-01")
    #print(f"Shopify_get_customers: {custom_response.status_code}")
    #print(custom_response.data)

    # GET MARKETING LIST CUSTOMERS
    # custom_response=Shopify_get_marketing_customer_list(shop=shop, access_token=access_token, api_version="2024-01")
    # print(custom_response.data)
    # response = custom_response.data
    # Separate newsletter subscribers and SMS marketing subscribers
    # newsletter_subscribers = [subscriber for subscriber in response['newsletter_subscribers']]
    # sms_marketing_subscribers = [subscriber for subscriber in response['sms_marketing_subscribers']]
    # print("Newsletter Subscribers:")
    # print(newsletter_subscribers)
    # print("\nSMS Marketing Subscribers:")
    # print(sms_marketing_subscribers)

    # LOAD BANNERS TO SOPHIFY
    banner_url = image1_url
    mobile_banner_url = image1_url
    metaobject_banner_number = 2
    product_url="https://vinzo.uk/products/emilio-moro-vendimia-seleccionada-2021"
    # metaobject_gid = Shopify_get_metaobject_gid(shop=shop, access_token=access_token, metaobject_type=metaobject_type, handle=metaobject_handle)
    # Shopify_update_metaobject(shop=shop, access_token=access_token, metaobject_gid=metaobject_gid, banner_url=banner_url, mobile_banner_url=mobile_banner_url, product_url=product_url, metaobject_banner_number=metaobject_banner_number)

    custom_response = Shopify_get_collection_metadata(shop=shop, access_token=access_token, collection_id=collection_id)
    print(f"Shopify_get_collection_metadata: {custom_response.status_code}")

    custom_response = Shopify_get_collections(shop=shop, access_token=access_token)
    print(f"Shopify_get_collections: {custom_response.status_code}")

    if custom_response.status_code == 200:
        collections = custom_response.data
        for collection in collections:
            #print(collections)
            custom_response = Shopify_get_collection_metadata(shop=shop, access_token=access_token, collection_id=collection_id)
            print(f"Shopify_get_collection_metadata: {custom_response.status_code}")
            # print (custom_response.data)
            break
    
    custom_response = Shopify_get_products_in_collection(shop=shop, access_token=access_token, collection_id=collection_id)
    print(f"Shopify_get_products_in_collection: {custom_response.status_code}")

    if custom_response.status_code == 200:
        products = custom_response.data
        # Get the ID of the first product
        first_product_id = products[0]['id']
        
        # Call Shopify_get_product_variants to get the variants for the first product
        custom_response = Shopify_get_product_variants(shop=shop, access_token=access_token, product_id=first_product_id)
        if custom_response.status_code == 200:
            variants = custom_response.data
            # Extract the price of the first variant
            print(variants[0])
            first_variant_price = variants[0].get('price')
            first_variant_compare_price = variants[0].get('compare_at_price')
            
            # Print the price
            print("Price of the first variant:", first_variant_price)
            print(first_variant_compare_price)
            print(f"Shopify_get_product_variants: {custom_response.status_code}")

        else:
            print("Shopify_get_product_variants Failed to retrieve variants for the first product")
    else:
        print("Shopify_get_product_variants Failed to retrieve products")
    
if b_test_s3:

    S3_ACCESS_KEY_ID = 'AKIAVRUVVBONIFTN4GAX'
    S3_SECRET_ACCESS_KEY = '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'
    S3_URL = 'https://getaiir.s3.eu-central-1.amazonaws.com'
    S3_CUBE_PUBLIC = 'getaiir/public/'
    S3_BUCKET_NAME = 'getaiir'
    S3_CUBE_NAME = 'eu-central-1'

    s3_config_dict = {
        "S3_ACCESS_KEY_ID": S3_ACCESS_KEY_ID,
        "S3_SECRET_ACCESS_KEY": S3_SECRET_ACCESS_KEY,
        "S3_URL": S3_URL,
        "S3_CUBE_NAME": S3_CUBE_NAME,
        "S3_CUBE_PUBLIC": S3_CUBE_PUBLIC,
        "S3_BUCKET_NAME": S3_BUCKET_NAME
    }

    #################################

    s3_list_files_in_folder(folder_name="wine/image", s3_config_dict=s3_config_dict)

    dest_folder="c:\\users\\rforn\\downloads\\wine"
    dest_folder="C:\\Users\\rforn\\Dropbox\\My PC (LAPTOP-7IFP1HKP)\\Downloads\\BorrarWine"
    dest_folder="C:\\Users\\rforn\\Dropbox\\Code\\RikPy\\Downloads\\Wine"
    folder_name="wine/image"
    s3_download_files_in_folder(folder_name=folder_name, destination_folder=dest_folder, s3_config_dict=s3_config_dict)

    exit()

    url="https://files.canvas.switchboard.ai/4ea249ec-1808-4a19-afd7-0a251a8d8aaf/1aaced80-f587-41a2-855c-33501840f337.png"
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    print(local_filename)

    mobile_banner_image = url

    profile_topic = "wine"

    bnewname = True
    mobile_banner_url = s3_upload_file_from_url(file_url=mobile_banner_image, folder_name=profile_topic, s3_config_dict=s3_config_dict, bnewname=bnewname)        
    print(mobile_banner_url)

    print

    
    #####################

    # s3_config_dict = s3_environment()

    print(s3_config_dict)
    
    objects = s3_list_files_in_folder(folder_name="public", s3_config_dict=s3_config_dict)

    exit()

    file_url="https://cloud-cube-eu2.s3.amazonaws.com/wwmx700brb7g/public/dogs/16264433-d3aa-4dbd-8318-722bde7ca2bb.png"
    local_file_path = '.gitignore'
    folder_name="public/wine"
    response=s3_upload_local_file(file_name=local_file_path, folder_name=folder_name, s3_config_dict=s3_config_dict)
    print(response)
    object_key=folder_name+"/"+local_file_path
    s3_delete_file(object_key=object_key, s3_config_dict=s3_config_dict)

    object_key = s3_upload_file_from_url(file_url=file_url, folder_name=folder_name, s3_config_dict=s3_config_dict, bnewname=True, make_public=False)
    print(object_key)

if b_test_heroku:

    heroku_config_dict = heroku_environment()
    folder="wine"
    files=heroku_list_files_in_folder(folder_name=folder, heroku_config_dict=heroku_config_dict)

    # heroku_download_files_in_folder(folder_name=folder, heroku_config_dict=heroku_config_dict, bdelete=True)
    # response = heroku_delete_file(file_key=file_key, heroku_config_dict=heroku_config_dict)
    # print(response)

if b_test_openai:
    load_dotenv()  # This loads the environment variables from .env
    openai_key = os.getenv("OPEN_AI_KEY")
    prompt="Tell me a joke"
    response = OpenAI_generate_response(prompt=prompt, openai_key=openai_key)
    print(response)
    print(response.data)
    print(response.status_code)
    if response.status_code != 200:
        print(f"Error occurred: {response.data}")
        exit()
    # post_details = json.loads(response.choices[0].message.content.strip())
    message_content = response.data.choices[0].message.content

    print(message_content)

    image_prompt = "An image of a gorila in a surreal jungle with melting timeclocks"
    response = OpenAI_generate_image(image_prompt=image_prompt, number_images=1, size="1024x1792", openai_key=openai_key)
    print(response)
    print(response.data)
    print(response.status_code)
    if response.status_code != 200:
        print(f"Error occurred: {response.data}")
        exit()
    
    image_response = response.data
    image_url = image_response.data[0].url
    print(image_url)