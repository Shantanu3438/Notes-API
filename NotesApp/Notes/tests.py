from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Note

class APITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.note = Note.objects.create(title='Test Note', content='Test Content', user=self.user)
        
        self.shared_user = User.objects.create_user(username='shareduser', password='sharedpassword')
        
    def testSignup(self):
        url = reverse('signup')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def testLogin(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testCreateNote(self):
        url = reverse('createNote')
        data = {'title': 'New Note', 'content': 'New Content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def testDeleteNote(self):
        url = reverse('deleteNote', kwargs={'pk': self.note.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def testGetNote(self):
        url = reverse('getNote', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testUpdateNote(self):
        url = reverse('updateNote', kwargs={'pk': self.note.pk})
        data = {'title': 'Updated Note', 'content': 'Updated Content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testNoteHistory(self):
        url = reverse('noteHistory', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testShareNote(self):
        url = reverse('shareNote', kwargs={'pk': self.note.pk, 'userpk': self.shared_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
