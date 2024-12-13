from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from blog.models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def viewPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewPostDetail(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addPost(request):
    print(f"Request method: {request.method}")
    
    # Validate and serialize the incoming data
    serializer = PostSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the post and return the serialized data with status code 201
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Created status code
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Bad Request for invalid data

@api_view(['POST'])
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Post successfully deleted!')