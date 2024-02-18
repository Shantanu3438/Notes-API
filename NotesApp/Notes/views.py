from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSignupSerializer, NoteSerializer, NoteHistorySerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Note, NoteHistory
from django.contrib.auth.models import User

@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        user = User.objects.get(username=username)
        return Response({'token': token.key, 'userID': user.id}, status=200)
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createNote(request):
    serializer = NoteSerializer(data=request.data, context={'exclude_user_field': True})
    if serializer.is_valid():
        serializer.validated_data['user'] = request.user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteNote(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    if note.user != request.user:
        return Response({'error': 'Not authorized to delete this note'}, status=status.HTTP_403_FORBIDDEN)
    note.delete()
    return Response({'STATUS': 'Note deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getNote(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({'error':'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    if (note.user != request.user) and (request.user not in note.sharedUser.all()):
        return Response({'error':'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    serializer = NoteSerializer(note)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def updateNote(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != note.user and request.user not in note.sharedUser.all():
        return Response({'error': 'You are not authorized to update this note'}, status=status.HTTP_403_FORBIDDEN)

    oldTitle = note.title
    oldContent = note.content

    serializer = NoteSerializer(note, data=request.data, context={'exclude_user_field': True})

    if serializer.is_valid():
        serializer.save()

        NoteHistory.objects.create(
            note = note,
            title = oldTitle,
            content = oldContent
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def noteHistory(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({"error": "Note does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != note.user and request.user not in note.sharedUser.all():
        return Response({'error': 'You are not authorized to update this note'}, status=status.HTTP_403_FORBIDDEN)

    noteHistory = NoteHistory.objects.filter(note=note)
    # if noteHistory:
    serializer = NoteHistorySerializer(noteHistory, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)    
    # else:
    #     return Response({'error':'No history for this note found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def shareNote(request, pk, userpk):
        try:
            note = Note.objects.get(pk=pk)
            if note.user != request.user:
                return Response({"error": "You are not the owner of this note"}, status=status.HTTP_403_FORBIDDEN)

        except Note.DoesNotExist:
            return Response({"error": "Note does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=userpk)
            note.sharedUser.add(user)
            return Response({'STATUS':'Note shared'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

