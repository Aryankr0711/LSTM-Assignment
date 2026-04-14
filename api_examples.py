"""
LSTM Next Word Predictor - Example API Calls

This script demonstrates how to interact with the FastAPI application.
Make sure the FastAPI server is running before executing this script.

Run the API server with:
    uvicorn app:app --reload

Then run this script:
    python api_examples.py
"""

import requests
import json
from typing import List, Dict
import time

# API Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # seconds

class LSTMPredictorClient:
    """Client for interacting with LSTM Predictor API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check if API is healthy and running"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def predict_next_word(self, text: str, top_k: int = 1) -> Dict:
        """Predict next word(s) for given text"""
        payload = {
            "text": text,
            "top_k": min(top_k, 10)  # API limits to 10
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def batch_predict(self, texts: List[str], top_k: int = 1) -> Dict:
        """Predict for multiple texts at once"""
        payload = [
            {"text": text, "top_k": min(top_k, 10)}
            for text in texts
        ]
        
        try:
            response = self.session.post(
                f"{self.base_url}/batch-predict",
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        try:
            response = self.session.get(
                f"{self.base_url}/info",
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_docs(self) -> str:
        """Get API documentation URL"""
        return f"{self.base_url}/docs"


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_result(result: Dict):
    """Pretty print API result"""
    print(json.dumps(result, indent=2))


def main():
    """Main demonstration function"""
    
    print("\n" + "="*70)
    print("  LSTM NEXT WORD PREDICTOR - API EXAMPLES")
    print("="*70)
    
    # Initialize client
    client = LSTMPredictorClient()
    
    # ==================== Example 1: Health Check ====================
    print_section("Example 1: Health Check")
    print("Checking if API is healthy...")
    health = client.health_check()
    print_result(health)
    
    if "error" in health:
        print("\n⚠️  API is not running!")
        print("Start the API server with: uvicorn app:app --reload")
        return
    
    # ==================== Example 2: Model Information ====================
    print_section("Example 2: Model Information")
    print("Fetching model architecture and configuration...")
    model_info = client.get_model_info()
    
    # Print selected info
    if "error" not in model_info:
        print(f"Model Type: {model_info.get('model_type')}")
        print(f"Vocabulary Size: {model_info.get('vocabulary_size'):,}")
        print(f"Sequence Length: {model_info.get('sequence_length')}")
        print(f"Total Parameters: {model_info.get('total_parameters'):,}")
        print(f"Number of Layers: {model_info.get('layers')}")
    else:
        print_result(model_info)
    
    # ==================== Example 3: Simple Prediction ====================
    print_section("Example 3: Single Word Prediction")
    test_text_3 = "the quick brown"
    print(f"Input: '{test_text_3}'")
    print("Predicting next word...")
    result_3 = client.predict_next_word(test_text_3, top_k=1)
    
    if "predictions" in result_3:
        for pred in result_3["predictions"]:
            print(f"  → {pred['word']:20s} (Confidence: {pred['confidence']:.4f})")
    else:
        print_result(result_3)
    
    # ==================== Example 4: Top-5 Predictions ====================
    print_section("Example 4: Top-5 Word Predictions")
    test_text_4 = "machine learning is a subset of"
    print(f"Input: '{test_text_4}'")
    print("Getting top 5 predictions...\n")
    result_4 = client.predict_next_word(test_text_4, top_k=5)
    
    if "predictions" in result_4:
        for i, pred in enumerate(result_4["predictions"], 1):
            confidence_pct = pred['confidence'] * 100
            bar_length = int(confidence_pct / 2)
            bar = "█" * bar_length
            print(f"  {i}. {pred['word']:15s} | {bar} {confidence_pct:6.2f}%")
    else:
        print_result(result_4)
    
    # ==================== Example 5: Technical Domain ====================
    print_section("Example 5: Technical Domain Prediction")
    test_text_5 = "neural networks are used in deep learning for"
    print(f"Input: '{test_text_5}'")
    print("Getting predictions for technical text...\n")
    result_5 = client.predict_next_word(test_text_5, top_k=5)
    
    if "predictions" in result_5:
        for i, pred in enumerate(result_5["predictions"], 1):
            print(f"  {i}. {pred['word']:20s} - Confidence: {pred['confidence']:.6f}")
    else:
        print_result(result_5)
    
    # ==================== Example 6: Different Domains ====================
    print_section("Example 6: Predictions from Different Domains")
    
    test_cases = [
        ("artificial intelligence and machine learning are",),
        ("data science involves statistics and",),
        ("the future of technology is",),
    ]
    
    for test_text in test_cases:
        print(f"\nInput: '{test_text[0]}'")
        result = client.predict_next_word(test_text[0], top_k=3)
        
        if "predictions" in result:
            print("Top 3 Predictions:")
            for i, pred in enumerate(result["predictions"], 1):
                print(f"  {i}. {pred['word']:15s} ({pred['confidence']:.4f})")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    # ==================== Example 7: Batch Predictions ====================
    print_section("Example 7: Batch Predictions (Multiple Texts)")
    
    batch_texts = [
        "the quick brown fox jumps over",
        "machine learning is",
        "data science involves",
        "artificial intelligence can"
    ]
    
    print(f"Processing {len(batch_texts)} texts in batch...\n")
    batch_result = client.batch_predict(batch_texts, top_k=2)
    
    if "results" in batch_result:
        print(f"Successful: {batch_result['successful']}/{batch_result['total']}")
        print(f"Failed: {batch_result['failed']}\n")
        
        for result in batch_result["results"]:
            if result["success"]:
                response = result["response"]
                print(f"Input: '{response['input_text']}'")
                print("Predictions:")
                for pred in response["predictions"]:
                    print(f"  - {pred['word']:15s} ({pred['confidence']:.4f})")
                print()
    else:
        print_result(batch_result)
    
    # ==================== Example 8: Error Handling ====================
    print_section("Example 8: Error Handling")
    
    print("Test 1: Empty input")
    error_result_1 = client.predict_next_word("", top_k=1)
    if "error" in error_result_1:
        print(f"Expected Error: {error_result_1['error']}")
    
    print("\nTest 2: Invalid top_k (too high)")
    error_result_2 = client.predict_next_word("test", top_k=20)
    if "error" in error_result_2:
        print(f"Expected Error: {error_result_2['error']}")
    
    print("\nTest 3: Invalid top_k (below 1)")
    error_result_3 = client.predict_next_word("test", top_k=0)
    if "error" in error_result_3:
        print(f"Expected Error: {error_result_3['error']}")
    
    # ==================== Performance Test ====================
    print_section("Example 9: Performance Metrics")
    
    print("Measuring average response time...\n")
    test_inputs = [
        "the quick brown",
        "machine learning models",
        "data analysis is important",
        "deep learning networks",
        "artificial intelligence applications"
    ]
    
    response_times = []
    for test_input in test_inputs:
        start_time = time.time()
        result = client.predict_next_word(test_input, top_k=1)
        elapsed_time = time.time() - start_time
        
        if "predictions" in result:
            response_times.append(elapsed_time)
            print(f"'{test_input}' → {result['predictions'][0]['word']:15s} ({elapsed_time*1000:.2f}ms)")
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"\nPerformance Summary:")
        print(f"  Average Response Time: {avg_time*1000:.2f}ms")
        print(f"  Minimum Response Time: {min_time*1000:.2f}ms")
        print(f"  Maximum Response Time: {max_time*1000:.2f}ms")
        print(f"  Requests Processed: {len(response_times)}")
    
    # ==================== API Documentation ====================
    print_section("API Documentation")
    print(f"Interactive API Docs (Swagger UI):")
    print(f"  {client.get_docs()}")
    print(f"\nAlternative Docs (ReDoc):")
    print(f"  {client.base_url}/redoc")
    
    # ==================== Completion ====================
    print_section("Examples Completed Successfully!")
    print("\nAll API examples executed successfully.")
    print("For more information, visit the interactive documentation at:")
    print(f"  {client.get_docs()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure the FastAPI server is running!")
        print("Start it with: uvicorn app:app --reload")
