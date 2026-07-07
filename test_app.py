import unittest
from app import app, BARCA_SQUAD

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """הגדרת סביבת עבודה לבדיקות לפני כל טסט"""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        """בדיקת טעינת עמוד הבית (Route /)"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        
        # שימוש במחרוזת בטוחה שלא תלויה בתווים מיוחדים או בדיקת הקידוד הנכון
        self.assertIn(b'FC Barcelona Squad Dashboard', response.data)
        self.assertIn(b'Lamine Yamal', response.data)

    def test_get_squad_api(self):
        """בדיקת ה-API של הסגל (Route /api/squad)"""
        response = self.client.get('/api/squad')
        
        # וידוא הצלחה
        self.assertEqual(response.status_code, 200)
        
        # וידוא שהתוכן מוחזר כ-JSON תקין
        json_data = response.get_json()
        
        # וידוא שאורך הרשימה תואם לרשימה המקורית בקוד
        self.assertEqual(len(json_data), len(BARCA_SQUAD))
        
        # וידוא שנתוני השחקן הראשון תואמים
        self.assertEqual(json_data[0]['name'], "Lamine Yamal")
        self.assertEqual(json_data[0]['number'], 19)

if __name__ == '__main__':
    unittest.main()