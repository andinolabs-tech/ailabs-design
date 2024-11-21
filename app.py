import os, torch, json, time
from dotenv import load_dotenv
from flask import Flask, request, jsonify 
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)
load_dotenv()
NUEXTRACT_1_5_MODEL_PATH = os.getenv('NUEXTRACT_1_5_MODEL_PATH') 
CORS(app)

# For caching the model and tokenizer
model = None
tokenizer = None

class ModelNotLoadedError(Exception):
    pass

def load_model_and_tokenizer():
    global model, tokenizer
    if model is None or tokenizer is None:
        print(f"\n\nLoading model numind/NuExtract-v1.5 first time from {NUEXTRACT_1_5_MODEL_PATH} \n\n")
        model_path =  NUEXTRACT_1_5_MODEL_PATH # Check the .env file to ensure the path points to nuextract-v1.5 model foler
        device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, trust_remote_code=True).to(device).eval()
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            print(f"\n\nModel numind/NuExtract-v1.5 loaded from {NUEXTRACT_1_5_MODEL_PATH} successfully ! \n\n")
        except Exception as e:
            print(f"Error loading model numind/NuExtract-v1.5 or tokenizer: {e}")
            return (e)

def predict_NuExtract(texts, template):
    
    if model is None or tokenizer is None:
        raise ModelNotLoadedError("Model numind/NuExtract-v1.5 or Tokenizer not loaded")
    
    max_length = 10_000 
    max_new_tokens = 4_000    

    template = json.dumps(json.loads(template), indent=4)
    prompts = [f"""<|input|>\n### Template:\n{template}\n### Text:\n{text}\n\n<|output|>""" for text in texts]
    
    print(f"\n\ntemplate : {template}\n\n")
    print(f"\n\nprompts: {prompts}\n\n")

    outputs = []
    start_time = time.time()
    with torch.no_grad():
        for i in range(0, len(prompts), 1):  # batch_size set to 1
            batch_prompts = prompts[i:i+1]
            batch_encodings = tokenizer(batch_prompts, return_tensors="pt", truncation=True, padding=True, max_length=max_length).to(model.device)

            # Adjusting for flash-attention
            pred_ids = model.generate(
                **batch_encodings,
                max_new_tokens=max_new_tokens
            )
            outputs += tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    end_time = time.time()
    latency = end_time - start_time
    return [output.split("<|output|>")[1].strip() for output in outputs], latency


@app.route('/api/predict_NuExtract', methods=['POST'])
def api_Predict_NuExtract():
    data = request.get_json()
    print(f"\n\n=== Received data : === \n\n {data}\n\n")  
    required_parameters = ['text', 'template']     
    missing_fields = [field.replace('_', ' ').title() for field in required_parameters if not data.get(field)]    
    if missing_fields:
        response_data = {
            "error": f"Error: Please supply the following mandatory fields:\n\n{', '.join(missing_fields)}"
        }
        return jsonify(response_data), 400
    try:
        response_data, latency = predict_NuExtract(          
            texts=[data['text']],
            template=data['template']
        )        
        return jsonify({'model_response': response_data[0],'latency': latency}), 200
        
    except ModelNotLoadedError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    load_model_and_tokenizer()  
    app.run(debug=True, host='0.0.0.0', port=6999)