from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,APIView,permission_classes,authentication_classes
from rest_framework import status,generics,mixins
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from  accounts.serializers import CurrentUserPostsSerializer
from .permissions import AuthorOrReadOnly



@api_view(["GET","POST"])
def homepage(request):
    if request.method=="POST":
        data=request.data
        response={"message":"Hello World","data":data}
        return Response(data=response,status=status.HTTP_201_CREATED)
    
    else:
        response={"message":"Hello World"}

        return Response(data=response,status=status.HTTP_200_OK)

class PostListCreateView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class=PostSerializer 
    permission_classes=[IsAuthenticated]
    queryset=Post.objects.all()

    def perform_create(self, serializer):
        user= self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
        

class PostRetrieveUpdateDeleteView(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):

    serializer_class=PostSerializer
    permission_classes=[AuthorOrReadOnly]
    queryset=Post.objects.all()

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request:Request):
    user=request.user
    serializer=CurrentUserPostsSerializer(instance=user,context={"request":request})

    return Response(data=serializer.data,status=status.HTTP_200_OK)


class ListPostsForAuthor(generics.GenericAPIView,mixins.ListModelMixin):

    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated]
    queryset=Post.objects.all()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
















# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# @api_view(['GET','POST'])
# def list_posts(request):
#     posts=Post.objects.all()
#     if request.method=="POST":
#         data=request.data
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message": "New Post Created",
#                 "Post": serializer.data
#             }
#             return Response(data=response, status=status.HTTP_201_CREATED)
#         else:
#             response = {
#                 "message": "Error: Post not Created",
#                 "errors": serializer.errors
#             }
#             return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

#     serializer=PostSerializer(instance=posts,many=True)
#     return Response(data=serializer.data,status=status.HTTP_200_OK)


# @api_view(['GET'])
# def post_details(request,pk):
#     post=Post.objects.get(id=pk)
#     if post:
#         serializer=PostSerializer(instance=post,many=False)
#         return Response(data=serializer.data,status=status.HTTP_200_OK)
#     else:
#         return Response(data="Post Does not exist",status=status.HTTP_204_NO_CONTENT)


# @api_view(['PUT'])
# def updatePost(request,pk):
#     post= Post.objects.get(id=pk)
#     data=request.data

#     serializer=PostSerializer(instance=post,data=data)

#     if serializer.is_valid():
#         serializer.save()

#         response={
#             "message":'update',
#             "data":serializer.data
#         }

#         return Response(data=response,status=status.HTTP_202_ACCEPTED)
    
#     return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def deletePost(request,pk):
#     post= get_object_or_404(Post,pk=pk)

#     post.delete()

#     return Response(data={"message":"Post deleted"},status=status.HTTP_204_NO_CONTENT)
    

