import json
import requests

def test_predict_NuExtract():
    text = """We introduce Mistral 7B, a 7–billion-parameter language model engineered for superior performance and efficiency.
      Mistral 7B outperforms the best open 13B model (Llama 2) across all evaluated benchmarks, and the best released 34B model (Llama 1) in reasoning, mathematics, 
      and code generation. Our model leverages grouped-query attention (GQA) for faster inference, coupled with sliding window attention (SWA) to effectively handle sequences of arbitrary length with a reduced inference cost. We also provide a model fine-tuned to follow instructions, 
    Mistral 7B – Instruct, that surpasses Llama 2 13B – chat model both on human and automated benchmarks. Our models are released under the Apache 2.0 license. 
    Code: <https://github.com/mistralai/mistral-src> Webpage: <https://mistral.ai/news/announcing-mistral-7b/>"""

    template = """{        "Model": {            "Name": "",            "Number of parameters": "",            
    "Number of max token": "",            "Architecture": []        },        "Usage": {            
    "Use case": [],            "Licence": ""        }    }"""

    payload = {
        "text": text,
        "template": template
    }

    endpoint_url = "http://127.0.0.1:6999/api/predict_NuExtract"    
    # endpoint_url = "http://localhost:6999/api/predict_NuExtract"   
    headers = {
        "Content-Type": "application/json"
    }   
    try:
        response = requests.post(endpoint_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    response = test_predict_NuExtract()
    if response is not None:
        try:
            response_data = response.json()
            model_response = response_data.get('model_response', 'No model_response available')
            latency = response_data.get('latency', 'Latency not provided')
            print(f"\nNuExtract 1.5 Response:\n")
            print(f"\nModel Response: {model_response}\n")
            print(f"\nLatency: {latency:.4f} seconds\n")
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON response")
            print("Response content:", response.text)
    else:
        print("No response received from the server")