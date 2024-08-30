"""
server.py

This module sets up a Flask web server with an endpoint to analyze emotions 
from a given text input using the EmotionDetection package. It includes 
error handling for invalid or missing text and formats the response accordingly.

The application is deployed on localhost:5000 and listens for POST requests 
to the /emotionDetector endpoint. The response includes emotion scores and 
the dominant emotion extracted from the input text.
"""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Endpoint to analyze emotions from the provided text.

    Expects a JSON payload with a 'text' field. Uses the emotion_detector function 
    to analyze the text and return a formatted response with emotion scores and the 
    dominant emotion. If the text is invalid or missing, returns an error message.

    Returns:
        Response: JSON object with the formatted message or an error message.
    """
    # Get the JSON data from the request
    data = request.get_json()
    text_to_analyze = data.get('text', '')

    # Use the emotion_detector function
    result = emotion_detector(text_to_analyze)

    # Check if dominant_emotion is None
    if result['dominant_emotion'] is None:
        return jsonify({"message": "Invalid text! Please try again!"}), 400

    # Prepare the response
    response = {
        "anger": result["anger"],
        "disgust": result["disgust"],
        "fear": result["fear"],
        "joy": result["joy"],
        "sadness": result["sadness"],
        "dominant_emotion": result["dominant_emotion"]
    }

    # Format the output string
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

    return jsonify({"message": formatted_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)