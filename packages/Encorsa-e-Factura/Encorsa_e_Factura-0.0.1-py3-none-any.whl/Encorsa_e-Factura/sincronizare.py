import subprocess
import sys
from io import BytesIO
import base64
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import os

namespaces = {
    'ubl': "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
    'qdt': "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDataTypes-2",
    'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    # Add the rest of the namespaces as needed
}
xpath_CUI = './cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID'
xpath_CUI2 = './cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID'
xpath_ID = './cbc:ID'

def check_and_install_lxml():
    try:
        # Try to import the lxml module
        import lxml
        # print("The 'lxml' module is loaded")
    except ImportError:
        # If the import fails, the requests module is not installed, so install it
        print("The 'lxml' module is missing. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"])
        # Import requests again after installing
        import lxml
        print("The 'lxml' module has been successfully installed.")

def check_and_install_requests():
    try:
        # Try to import the requests module
        import requests
        # print("The 'requests' module is loaded")
    except ImportError:
        # If the import fails, the requests module is not installed, so install it
        print("The 'requests' module is missing. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        # Import requests again after installing
        import requests
        print("The 'requests' module has been successfully installed.")

def check_and_install_zipfile():
    try:
        # Try to import the requests module
        import zipfile
        # print("The 'zipfile' module is loaded")
    except ImportError:
        # If the import fails, the requests module is not installed, so install it
        print("The 'zipfile' module is missing. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "zipfile"])
        # Import requests again after installing
        import zipfile
        print("The 'zipfile' module has been successfully installed.")

check_and_install_requests()
check_and_install_zipfile()
check_and_install_lxml()

import requests
import zipfile
from requests.auth import HTTPBasicAuth
from lxml import etree

def get_token_with_refresh(refresh_token, clientID, clientSecret):
    url = "https://logincert.anaf.ro/anaf-oauth2/v1/token"
    auth = HTTPBasicAuth(clientID, clientSecret)
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    try:
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()  # This checks for HTTP errors and raises an exception if any

        json_response = response.json()  # Attempt to parse JSON response
        
        if 'access_token' in json_response:
            return json_response['access_token']
        else:
            # Handle cases where 'access_token' is not in response
            raise Exception("Error at getting ANAF aceess token. Access token not found in the response.")
    except Exception as e:
        # Catch all other errors
        raise Exception(f"Error at getting ANAF aceess token. Error message: {str(e)}")

def get_lista_paginata_mesaje(token, start_time, end_time, cif, pagina, filter = None):
    url = f"https://api.anaf.ro/prod/FCTEL/rest/listaMesajePaginatieFactura?startTime={start_time}&endTime={end_time}&cif={cif}&pagina={pagina}"
    if filter is not None:
        if filter != "":
            url += "&filtru=" + filter
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ridică o excepție pentru coduri de răspuns HTTP eronate
        return response.json()
    except Exception as e:
        return {'eroare': f'Error at getting messages for page {pagina}. Error message: {str(e)}'}

def get_all_messages(token, start_time, end_time, cif, filter = None):
    all_messages = []  # Lista pentru a stoca toate mesajele
    current_page = 1  # Indexul paginii curente începe de la 0

    # Încercăm să obținem mesajele de pe prima pagină pentru a verifica dacă există date
    first_page_response = get_lista_paginata_mesaje(token, start_time, end_time, cif, current_page)

    # Verificăm dacă răspunsul conține o eroare
    if "eroare" in first_page_response:
        if 'Nu exista mesaje' in first_page_response["eroare"]:
            print(first_page_response["eroare"])
            exit(0)
        raise Exception("Error at getting all messages from ANAF: " + first_page_response["eroare"])        

    # Dacă există mesaje, continuăm să le adunăm din toate paginile
    total_pages = first_page_response['numar_total_pagini']
    all_messages.extend(first_page_response['mesaje'])

    # Continuăm cu următoarele pagini, dacă există
    for current_page in range(2, total_pages + 1):
        response = get_lista_paginata_mesaje(token, start_time, end_time, cif, current_page, filter)
        if "eroare" in response:
            if 'Nu exista mesaje' in response["eroare"]:
                print(response["eroare"])
                exit(0)
            else:
                raise Exception("Error at getting all messages from ANAF: " + response["eroare"])    
        all_messages.extend(response['mesaje'])

    return all_messages

"""
Această funcție descarcă o arhivă ZIP de la ANAF folosind un ID de factură
și extrage un fișier specificat prin nume_fisier din aceasta. 
"""
def descarca_factura_si_extrage_fisier(token, id, nume_fisier):
    try:
        url = f"https://api.anaf.ro/prod/FCTEL/rest/descarcare?id={id}"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        
        # Verify the response status code
        if response.status_code != 200:
            # Raise an exception for non-200 status codes with the HTTP status code
            raise Exception(f"Error while downloading ZIP archive with the XML. Code: {response.status_code}")
    
        # Create a BytesIO object from the response content
        zip_in_memory = BytesIO(response.content)
        
        try:
            # Open the ZIP archive
            with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
                # Check if the file exists in the archive
                if nume_fisier in zip_ref.namelist():
                    # Extract the specified file content
                    with zip_ref.open(nume_fisier) as fisier:
                        content_bytes = fisier.read()
                        # Decode bytes into a string using UTF-8
                        content_string = content_bytes.decode('utf-8')
                        return content_string
                else:
                    # File not found in the archive, handle according to your preference
                    raise Exception(f"File '{nume_fisier}' not found in the ZIP archive")
        except zipfile.BadZipFile as zp_err:
            # Handle a bad ZIP file error
            raise Exception("The downloaded file is not a valid ZIP archive: " + str(zp_err))
    except Exception as e:
        # Handle other errors
        raise Exception(f"Error while downloading ZIP archive with the XML. Message: {e}")

"""
Funcția trimite date XML către un serviciu web al ANAF pentru a fi convertite
într-un document PDF, apoi encodează conținutul binar al PDF-ului obținut în format Base64
"""
def xml_to_pdf_to_base64(xml_data):
    try:
        url = "https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FACT1/DA"
        headers = {
            'Content-Type': 'text/plain'
        }
        response = requests.post(url, headers=headers, data=xml_data)
        # Check the response status code to ensure the request was successful
        if response.status_code != 200:
            # Raise an exception for non-200 status codes with the HTTP status code and error message
            response.raise_for_status()  # This will raise an HTTPError with detailed info
        # Assuming the response.content is the binary content of the PDF
        pdf_content = response.content
        # Encode the PDF content to Base64
        base64_encoded_pdf = base64.b64encode(pdf_content)
        # Convert the bytes object to a string to return it
        return base64_encoded_pdf.decode('utf-8')
    except Exception as e:
        # Catch-all for any other errors that might occur
        raise Exception("Error when converting the XML to PDF: " + str(e))

"""
Această funcție obține un token de autentificare de la serviciul WebCon
"""
def get_webcon_token(base_url, client_id, client_secret):
    url = f"{base_url}/api/login"  # Ensure this is the correct API endpoint
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "clientId": client_id,
        "clientSecret": client_secret
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            try:
                return response.json()["token"]
            except KeyError:
                # Key 'token' does not exist in the response
                raise Exception("Error at getting WebCon TOKEN: The response JSON does not contain a 'token' key")
        else:
            # For non-successful responses, raise an exception with status code and error
            raise Exception(f"Error at getting WebCon TOKEN: HTTP {response.status_code} - {response.text}")
    except Exception as e:
        # A single catch-all for any exception, including request errors, HTTP errors, and JSON parsing errors
        raise Exception(f"Error at getting WebCon TOKEN: {str(e)}")

def create_invoice_instance(parameters, token, body):
    url = f"{parameters['webcon_base_url']}/api/data/{parameters['webcon_api_version']}/db/{parameters['webcon_dbid']}/elements?path={parameters['webcon_path']}&mode={parameters['webcon_mode']}"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        
        if response.status_code == 200:
            return response.json()
        else:
            error_message = response.json().get('description', 'Unknown error occurred')
            error_code = response.status_code
            # Including more detailed information in the exception
            raise Exception(f"Failed to create WebCon invoice instance. Error code: {error_code}, Message: {error_message}")    
    except Exception as e:
        # Catching any other exceptions that weren't anticipated
        raise Exception(f"Failed to create WebCon invoice instance. An unexpected error occurred: {str(e)}")

"""
Functia trebuie sa isi ia datele dintr-un raport cu facturi care
contine numai doua coloane: ID-factura si CUI, fara a schimba ordinea lor
"""
def check_if_invoice_exists(parameters, token, invoice_id, supplier_company_id):
    base_url = f"{parameters['webcon_base_url']}/api/data/{parameters['webcon_api_version']}"
    url = f"{base_url}/db/{parameters['webcon_dbid']}/applications/{parameters['webcon_report_app_id']}/reports/{parameters['webcon_report_id']}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    filters = {
        f'{parameters["invoice_id_url_filter"]}': invoice_id,
        f'{parameters["supplier_company_id_url_filter"]}':supplier_company_id,
        'page': 1,
        'size': 1
    }

    try:
        response = requests.get(url, headers=headers, params=filters)
        response.raise_for_status()
        data = response.json()
        count = len(data['rows'])

    except Exception as err:
        raise Exception(f"Failed to get Invoices list from WebCon report. An unexpected error occurred: {str(err)}")
        
    if count <= 0:
        return False
    else:
        return True

def create_webcon_body(parameters, xml_b64, pdf_b64, xml_file_data, id, cui, template_xml_path):

    processor = XMLProcessor(template_xml_path, xml_file_data, namespaces)
    all_lists_data, extracted_data = processor.process_xml()
    
    item_lists_json = create_list_of_dicts(all_lists_data)
    form_fields_json = create_form_filed_json(extracted_data)

    form_fields_json.extend([
            {
                "guid": parameters['id_field_guid'],
                "svalue": id
            },
            {
                "guid": parameters['cui_field_guid'],
                "svalue": cui
            }
        ])

    body = {
        "workflow": {
            "guid": parameters['webcon_wfid'],
        },
        "formType": {
            "guid": parameters['webcon_wfdid'],
        },
        "formFields": form_fields_json,
        "itemLists": item_lists_json,
        "attachments": [
            {
                "name": "fisierXML.xml",
                "content": xml_b64
            },
            {
                "name": "fisierPDF.pdf",
                "content": pdf_b64
            }
        ],
        "businessEntity": {
            "id": parameters['webcon_bentity']
        }
    }
    #print(json.dumps(body, indent=4))
    return body

def send_to_WebCon(parameters, token , messages, xml_template_file_path):
    wtoken = get_webcon_token(parameters['webcon_base_url'], parameters['webcon_clientID'], parameters['webcon_clientSecret'])
    current_message = 1

    for message in messages:
        # print(f'Processing message {current_message} of {len(messages)}')
        try:
            id_solicitare = message["id_solicitare"]
            id = message["id"]
            tip_factura = message["tip"]
            filtru_facturi = parameters.get('ANAF_invoice_type_filter_E_T_P_R', '')

            if filtru_facturi != '':
                if tip_factura != filtru_facturi:
                    print(f"Skipping invoice with ANAF_ID: {id}, because type filters are applied. The filter is: {filtru_facturi})")
                    continue
            else:
                if tip_factura != "FACTURA TRIMISA" and tip_factura != "FACTURA PRIMITA":
                    print(f"Skipping invoice with ANAF_ID: {id}. The message type is not <FACTURA TRIMISA> or <FACTURA PRIMITA>")
                    continue
            
            xml_text = descarca_factura_si_extrage_fisier(token, str(id), f"{id_solicitare}.xml")

            # Se verifica daca factura preluata exista deja in WebCon pe baza cheii unice formate din ID-factura si CUI
            root = ET.fromstring(xml_text)
            invoice_id_element = root.find(xpath_ID, namespaces)
            company_id_element = root.find(xpath_CUI, namespaces)
            company_id_element2 = root.find(xpath_CUI2, namespaces)
            company_id = ""

            if invoice_id_element is None:
                print('Cannot get Invoice ID from XML, skipping invoice. ID from ANAF: ' + id)
                continue
            else:
                invoice_id_element = invoice_id_element.text

            if company_id_element is None:
                if company_id_element2 is None:
                    print('Cannot get Invoice Supplier Company ID, skipping invoice. ID from ANAF: ' + id)
                else:
                    company_id = company_id_element2.text
            else:
                company_id = company_id_element.text

            if check_if_invoice_exists(parameters, wtoken, invoice_id_element, company_id):
                print(f"Skipping invoice with ID: {invoice_id_element}, COMPANY ID: {company_id}, because it already exists in WebCon")
                continue
            
            pdf_content = xml_to_pdf_to_base64(xml_text)
            xml_bytes = str(xml_text).encode('utf-8')
            base64_encoded_xml = base64.b64encode(xml_bytes)
            base64_string_xml = base64_encoded_xml.decode('utf-8')

            body = create_webcon_body(parameters, base64_string_xml, pdf_content, xml_text, invoice_id_element, company_id, xml_template_file_path)
            response = create_invoice_instance(parameters, wtoken, body)
            print(f"Invoice instance created with SUCCESS having WFD_ID: < {response['id']} >")
        except Exception as ex:
            # Preparing and printing a detailed error message
            error_details = f"Error at processing message: {message}.\nError message: {str(ex)}"
            raise Exception(error_details)
        current_message += 1

def read_json_parameters(file_path):
    """Read and return the parameters stored in a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            file_content = file.read().strip()
            parameters = json.loads(file_content)
            return parameters
    except FileNotFoundError:
        raise Exception(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        raise Exception(f"Error: The file {file_path} contains invalid JSON.")
    except Exception as ex:
        raise Exception(f"Error: The file {file_path} cannot opened/used. " + str(ex))

def main():
    # Check if the JSON file path is provided as a command line argument
    if len(sys.argv) < 2:
        raise Exception("The JSON file path is missing. Usage: python script.py <path_to_json_file>")
    
    # The first command line argument is the JSON file path
    json_file_path = sys.argv[1]
    xml_template_file_path = sys.argv[2]
    
    # Read parameters from the JSON file
    parameters = read_json_parameters(json_file_path)
  
    try:
        unix_timestamp_from = datetime.fromisoformat(parameters['get_invoices_from_timestamp'])
        unix_timestamp_to = datetime.fromisoformat(parameters['get_invoices_to_timestamp'])

        unix_timestamp_from = int(unix_timestamp_from.timestamp() * 1000)
        unix_timestamp_to = int(unix_timestamp_to.timestamp() * 1000)
        print(unix_timestamp_from)
        print(unix_timestamp_to)

        token_aux = get_token_with_refresh(parameters['refresh_token_anaf'], parameters['efactura_clientID'], parameters['efactura_clientSecret'])

        # get message filter
        messages = get_all_messages(token_aux, str(unix_timestamp_from), str(unix_timestamp_to), parameters['cod_fiscal_client'])
        send_to_WebCon(parameters, token_aux, messages, xml_template_file_path)
    except Exception as ex:
        raise Exception("Error in main function: " + str(ex))
    
class XMLDataExtractor:
    def __init__(self, xml_tree, result_dict, namespaces=None):
        self.xml_tree = xml_tree
        self.result_dict = result_dict
        self.namespaces = namespaces if namespaces is not None else {}

    def extract_list_data(self, parent_path, columns):
        list_data = []
        parent_nodes = self.xml_tree.xpath(parent_path, namespaces=self.namespaces)

        for parent_node in parent_nodes:
            row_data = {}
            for column_path, column_name in columns:
                if '@' in column_path:
                    element_path, attribute_name = column_path.rsplit('@', 1)
                    child = parent_node.xpath(element_path, namespaces=self.namespaces)
                    if child:
                        value = child[0].get(attribute_name)
                    else:
                        value = None
                else:
                    child = parent_node.xpath(column_path, namespaces=self.namespaces)
                    value = child[0].text.strip() if child else None

                row_data[column_name] = value
            list_data.append(row_data)

        return list_data

    def extract_all_lists(self):
        all_lists_data = {}
        for list_id, info in self.result_dict.items():
            parent_path, columns = info[0], info[1]
            all_lists_data[list_id] = self.extract_list_data(parent_path, columns)
        return all_lists_data

class XMLTemplateParser:
    def __init__(self, xml_tree, namespaces):
        self.xml_tree = xml_tree
        self.namespaces = namespaces

    def parse_template(self):
        template_data = {}

        def traverse(node, path='', isParentList=False, parentListID=""):
            if isinstance(node.tag, str):
                qname = etree.QName(node)
                node_tag = qname.localname
                namespace_prefix = None
                for prefix, uri in self.namespaces.items():
                    if uri == qname.namespace:
                        namespace_prefix = prefix
                        break

                current_path = f"{path}/{namespace_prefix}:{node_tag}" if namespace_prefix else f"{path}/{node_tag}"
                node_list_id = next((t[1] for t in node.attrib.items() if t[0] == "itemList"), "")
                node_is_list = node_list_id != ""

                if node_is_list and isParentList:
                    raise Exception("Template incorrectly configured. You cannot have nested list in template configuration!")

                for attr_name, attr_value in node.attrib.items():
                    if attr_name == "itemList":
                        continue
                    attr_qname = etree.QName(attr_name)
                    attr_localname = attr_qname.localname
                    attr_namespace_uri = attr_qname.namespace
                    attr_namespace_prefix = ''
                    for prefix, uri in self.namespaces.items():
                        if uri == attr_namespace_uri:
                            attr_namespace_prefix = prefix
                            break
                    full_attr_name = f"{attr_namespace_prefix}:{attr_localname}" if attr_namespace_prefix else attr_localname

                    if node_is_list:
                        template_data[f"{current_path}@{full_attr_name}"] = (attr_value, node_list_id)
                    elif isParentList:
                        template_data[f"{current_path}@{full_attr_name}"] = (attr_value, parentListID)
                    else:
                        template_data[f"{current_path}@{full_attr_name}"] = (attr_value, "")

                if node.text and node.text.strip():
                    if node_is_list:
                        template_data[current_path] = (node.text.strip(), node_list_id)
                    elif isParentList:
                        template_data[current_path] = (node.text.strip(), parentListID)
                    else:
                        template_data[current_path] = (node.text.strip(), "")

                for child in node:
                    if node_is_list:
                        traverse(child, current_path, node_is_list, node_list_id)
                    elif isParentList:
                        traverse(child, current_path, isParentList, parentListID)
                    else:
                        traverse(child, current_path, False, "")

        traverse(self.xml_tree.getroot())
        return template_data

class XMLDataProcessor:
    def __init__(self, data_xml_tree, template_keys, namespaces):
        self.data_xml_tree = data_xml_tree
        self.template_keys = template_keys
        self.namespaces = namespaces

    def apply_template(self):
        extracted_data = {}

        for path, (key, listId) in self.template_keys.items():
            if "@" in path:
                element_path, attribute_name = path.rsplit('@', 1)
                nodes = self.data_xml_tree.xpath(element_path, namespaces=self.namespaces)
                if nodes:
                    node = nodes[0]
                    attr_value = node.get(attribute_name)
                    if attr_value:
                        extracted_data[key] = attr_value
            else:
                nodes = self.data_xml_tree.xpath(path, namespaces=self.namespaces)
                if nodes:
                    node = nodes[0]
                    value = node.text.strip() if node.text and node.text.strip() else None
                    extracted_data[key] = value

        return extracted_data

class XMLProcessor:
    def __init__(self, template_xml_path, xml_file_data, namespaces):
        self.template_xml_path = template_xml_path
        self.xml_file_data = xml_file_data
        self.namespaces = namespaces

    def process_xml(self):
        # Parsarea template-ului XML
        with open(self.template_xml_path, 'r', encoding='utf-8-sig') as file:
            template_tree = etree.parse(file)
        template_parser = XMLTemplateParser(template_tree, self.namespaces)
        template_data = template_parser.parse_template()

        # Dictionary to store removed elements
        removed_elements = {}

        # Iterate over the original dictionary
        for key, (first_val, second_val) in template_data.copy().items():
            if second_val != "":
                if second_val not in removed_elements:
                    removed_elements[second_val] = [(key, first_val)]
                else:
                    removed_elements[second_val].append((key, first_val))
                del template_data[key]

        transformed_dict = {}

        for key, paths_list in removed_elements.items():
            common_prefix = os.path.commonprefix([path[0] for path in paths_list])
            common_base_path = common_prefix.rsplit('/', 1)[0]
            transformed_dict[key] = (common_base_path, paths_list)

        # Parsarea XML-ului cu date reale
        data_tree = etree.fromstring(self.xml_file_data.encode('utf-8'))
        data_processor = XMLDataProcessor(data_tree, template_data, self.namespaces)
        extracted_data = data_processor.apply_template()

        extractor = XMLDataExtractor(data_tree, transformed_dict, self.namespaces)
        all_lists_data = extractor.extract_all_lists()

        return all_lists_data, extracted_data

def create_list_of_dicts(data_dict):
    result_list = []
    for item_list_guid, rows in data_dict.items():
        item_list_wrapper = {}
        item_list_wrapper['guid'] = item_list_guid
        row_lists = []
        for row in rows:
            row_dict = {}
            cells_list = []
            for cell_guid, cell_value in row.items():  # Iterate over the items in the row dictionary
                cell_dict = {'guid': cell_guid, 'svalue': cell_value if cell_value is not None else ''}
                cells_list.append(cell_dict)
            row_dict['cells'] = cells_list
            row_lists.append(row_dict)
        item_list_wrapper['rows'] = row_lists
        result_list.append(item_list_wrapper)
    return result_list

def create_form_filed_json(extracted_data):
    form_fields = []
    for key, value in extracted_data.items():
        field = {'guid': key, 'svalue': value if value is not None else '' }
        form_fields.append(field)
    return form_fields

if __name__ == "__main__":
    main()

