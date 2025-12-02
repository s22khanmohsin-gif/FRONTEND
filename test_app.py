import unittest
import json
from app import app

class CVDAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_predict_endpoint(self):
        # Sample data with all 18 features
        data = {
            'Age': 45,
            'Sex': '1',
            'Height': 175,
            'Weight': 80,
            'BMI': 26.12,
            'General_Health': 'Good',
            'Checkup': 'Within 1 year',
            'Diabetes': 'No',
            'Skin_Cancer': 0,
            'Other_Cancer': 0,
            'Depression': 0,
            'Arthritis': 0,
            'Exercise': '1',
            'Smoking': '0',
            'Alcohol': 5,
            'Fruit': 10,
            'Green_Vegetables': 15,
            'Fried_Potato': 2
        }
        
        response = self.app.post('/predict', 
                                 data=json.dumps(data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('probability', result)
        self.assertIn('class', result)
        self.assertIn('risk_level', result)
        print(f"Prediction result: {result}")

if __name__ == '__main__':
    unittest.main()
