from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowTransactionViewSet
from django.urls import path
from .views import UserList
from .views import BorrowBookView, ReturnBookView


router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'transactions', BorrowTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserList.as_view(), name='user-list'),
     path('borrow/', BorrowBookView.as_view(), name='borrow'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return'),
]

