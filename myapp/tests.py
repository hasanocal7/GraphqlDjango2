from django.test import TestCase
from graphene.test import Client
from .schema import schema  # Burada, GraphQL şemanızın bulunduğu dosyayı ekleyin
from .models import User

class GraphQLTests(TestCase):
    def setUp(self):
        # Test veritabanına birkaç örnek ekleyin
        User.objects.create(username="testuser1", birthdate="2000-01-01", gender="Male")
        User.objects.create(username="testuser2", birthdate="1995-05-15", gender="Female")

    def test_query_users(self):
        # Kullanıcıları sorgula
        query = '''
            query {
                users {
                    id
                    username
                    birthdate
                    gender
                }
            }
        '''
        client = Client(schema)
        response = client.execute(query)
        self.assertEqual(response.status_code, 200)

        # Sorgudan dönen sonucu kontrol et
        expected_data = {
            'users': [
                {'id': '1', 'username': 'testuser1', 'birthdate': '2000-01-01', 'gender': 'Male'},
                {'id': '2', 'username': 'testuser2', 'birthdate': '1995-05-15', 'gender': 'Female'}
            ]
        }
        self.assertEqual(response.json()['data'], expected_data)

    def test_mutation_create_user(self):
        mutation = '''
            mutation {
                createUser(username: "newuser", birthdate: "1990-12-31", gender: "Other") {
                    user {
                        id
                        username
                        birthdate
                        gender
                    }
                }
            }
        '''
        client = Client(schema)
        response = client.execute(mutation)
    
        # response'ın içindeki errors ve data alanlarını kontrol et
        self.assertFalse(response.get('errors'))
        self.assertTrue(response.get('data'))
    
        # Eğer kullanıcı oluşturma başarılıysa, oluşturulan kullanıcının bilgilerini içeren user alanını kontrol et
        created_user = response['data']['createUser']['user']
        self.assertEqual(created_user['username'], 'newuser')
        # Diğer alanları da kontrol et...
    
        # Eğer kullanıcı oluşturma başarısızsa, hata mesajlarını kontrol et
        self.assertIsNone(response.get('data'))
        self.assertTrue(response.get('errors'))
        # Hata mesajlarını kontrol et...
    