from bs4 import BeautifulSoup
import requests
import json
import os


def scrape_openai_price() -> dict:
    """
    Thi function scrapes and return a dict of OpenAI's pricing,
    where every key is a model name.
    """
    
    def clean_txt(txt):
        return txt.encode("ISO-8859-1").decode("UTF-8").replace("\xa0", "").replace("Â·", "")

    response = requests.get("https://openai.com/pricing")

    soup = BeautifulSoup(response.text, 'html.parser')

    container_div = soup.find("div", {"id": "content"})
    models_div = container_div.find_all("div", {"class": "ui-block ui-block--pricing-table"})

    prices = {}

    for div in models_div:
        
        #father_model_name = div.get("id")
        #prices[father_model_name] = {}
        
        # find the table in div
        table = div.find("table")
        # find all tr in table
        trs = table.find_all("tr")
        
        # Header row
        columns = [td.text for td in trs[0].find_all("td")]
        
        # Content rows
        for row in trs[1:]:
            
            # Cells
            cells = [td for td in row.find_all("td")]
            assert len(cells) == len(columns)
            
            # First cell
            submodel_name = cells[0].find('span')
            
            if submodel_name:
            
                submodel_name = clean_txt(submodel_name.text)
                #prices[father_model_name][submodel_name] = {}
                prices[submodel_name] = {}
                
                # Other cells
                for i, (cell, column) in enumerate(zip(cells[1:], columns[1:])):
                    
                    # Extract content from cell
                    spans = cell.find_all("span")
                    if spans:
                        if len(spans) > 1:
                            text = "".join([clean_txt(span.text) for span in spans])
                            
                        else:
                            text = clean_txt(spans[0].text)
                        
                        #prices[father_model_name][submodel_name][column] = text
                        prices[submodel_name][column] = text
        
    return prices

def parse_dict(prices:dict) -> dict:
    """
    This function takes the dict of prices and returns a new dict
    parsed and cleaned to contain floats and integers instead of strings,
    ready to be multiplied by the number of tokens.
    """
    
    prices2 = {}
    
    for k,v in prices.items():
        
        prices2[k] = {}
        
        if "gpt" in k.lower() or "older models" in k.lower():
        
            for header, full_price in v.items():
                header = header.lower().replace("usage","").strip()
                full_price = full_price.lower()
                price = float(full_price.split("/")[0].replace("$", "").strip())
                quotient = int(full_price.split("/")[1].replace("tokensm","").replace("tokensk","").replace("tokens","").replace("k","000").replace("m","000000").strip())
                prices2[k][header] = {"price": price, "quotient": quotient, "currency": "$", "um": "tokens"}
        else:
            prices2[k] = v
            
    return prices2
    
def update_pricing(verbose:bool=False) -> dict:
    """
    Main function to update the pricing and save it to a json file.
    :param verbose: if True, prints the prices
    """
    prices = scrape_openai_price()
    prices = parse_dict(prices)
    with open("prices.json", "w") as f:
        json.dump(prices, f)
    if verbose:
        print(prices)
    return prices

def get_pricing(model:str, prompt_tokens:int, completion_tokens:int) -> tuple:
    """
    Given a model name and the number of tokens used for prompt and completion,
    returns the price for the prompt and the completion.
    :param model: the openai model name
    :param prompt_tokens: the number of tokens used for the prompt
    :param completion_tokens: the number of tokens used for the completion
    :return: a tuple with the price for the prompt and the completion
    """
    
    if not os.path.exists("prices.json"):
        _ = update_pricing()
    with open("prices.json", "r") as f:
        prices = json.load(f)
    
    try:
        model_pricing = prices.get(model,None)
        if not model_pricing:
            # if 'gpt-3.5' in model.lower():
            #     input_price = 0.0005
            #     input_quotient = 1000
            #     output_price = 3*0.0005
            #     output_quotient = 1000
            # elif 'gpt-4' in model.lower():
            #     input_price = 0.0015
            #     input_quotient = 1000
            #     output_price = 3*0.0015
            #     output_quotient = 1000
            # else:
            #    return 0,0
            print(f"Model {model} not found. Price will not be added to log.")
            return 0,0
            
        input_price = model_pricing["input"]["price"]
        input_quotient = model_pricing["input"]["quotient"]
        prompt_price = input_price * (prompt_tokens / input_quotient)
        
        output_price = model_pricing["output"]["price"]
        output_quotient = model_pricing["output"]["quotient"]
        completion_price = output_price * (completion_tokens / output_quotient)
        
        return prompt_price, completion_price
        
    except Exception as e:
        print("Exception in get_pricing():",e)
        return 0,0


if __name__ == "__main__":
    prices = update_pricing()
    print(prices)