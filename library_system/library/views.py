from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, BorrowTransaction, User
from .serializers import BookSerializer, BorrowTransactionSerializer

class UserList(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'username')
        return Response(users)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        has_active_borrow = book.borrowtransaction_set.filter(status='borrowed').exists()
        if has_active_borrow:
            return Response({'error': 'Cannot delete a book that is currently borrowed.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

class BorrowTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowTransaction.objects.all()
    serializer_class = BorrowTransactionSerializer

class BorrowBookView(APIView):
    def post(self, request):
        serializer = BorrowTransactionSerializer(data=request.data)
        if serializer.is_valid():
            book = Book.objects.get(pk=serializer.validated_data['book'].id)
            if book.copies_available < 1:
                return Response({"error": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)
            book.copies_available -= 1
            book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(APIView):
    def post(self, request, pk):
        try:
            transaction = BorrowTransaction.objects.get(pk=pk)
        except BorrowTransaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

        if transaction.status != 'returned':
            transaction.status = 'returned'
            transaction.return_date = timezone.now()
            transaction.book.copies_available += 1
            transaction.book.save()
            transaction.save()

        return Response({"message": "Book returned successfully."})
    
    
