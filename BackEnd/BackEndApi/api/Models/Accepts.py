from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from django.db.models import Subquery, OuterRef
from api.Models.Requests import Requests
from api.Models.RequestPictures import RequestPictures
from api.Models.GameTitles import GameTitles

class Accepts(models.Model):
    request_id = models.IntegerField()
    client_id = models.IntegerField()
    contractor_id = models.IntegerField()
    price = models.IntegerField(null=True)
    status = models.IntegerField()
    canceled_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'accepts'

    def getAcceptsRecordsCount(self, statuses, client_id=None, contractor_id=None):
        try:
            queryset = Accepts.objects.all()
            queryset = queryset.filter(status__in=statuses)
            if client_id is not None:
                queryset = queryset.filter(client_id=client_id)
            elif contractor_id is not None:
                queryset = queryset.filter(contractor_id=contractor_id)
            return queryset.count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getAccepts(self, offset, limit, statuses, client_id=None, contractor_id=None):
        try:
            from api.models import Users
            client_user_subquery = Users.objects.filter(id=OuterRef('client_id')).values('nickname')[:1]
            contractor_user_subquery = Users.objects.filter(id=OuterRef('contractor_id')).values('nickname')[:1]
            queryset = Accepts.objects.filter(
                status__in=statuses
            ).annotate(
                smallest_sort_no=Subquery(
                    RequestPictures.objects.filter(
                        request_id=OuterRef('request_id'),
                        deleted_at__isnull=True
                    ).order_by('sort_no').values('sort_no')[:1]
                ),
                path=Subquery(
                    RequestPictures.objects.filter(
                        request_id=OuterRef('request_id'),
                        sort_no=OuterRef('smallest_sort_no'),
                        deleted_at__isnull=True
                    ).values('path')[:1]
                ),
                request_title=Subquery(
                    Requests.objects.filter(
                        id=OuterRef('request_id')
                    ).values('request_title')[:1]
                ),
                min_price=Subquery(
                    Requests.objects.filter(
                        id=OuterRef('request_id')
                    ).values('min_price')[:1]
                ),
                max_price=Subquery(
                    Requests.objects.filter(
                        id=OuterRef('request_id')
                    ).values('max_price')[:1]
                ),
                game_title_id=Subquery(
                    Requests.objects.filter(
                        id=OuterRef('request_id')
                    ).values('game_title_id')[:1]
                ),
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                client_nickname=Subquery(client_user_subquery),
                contractor_nickname=Subquery(contractor_user_subquery)
            )
            if client_id is not None:
                queryset = queryset.filter(client_id=client_id)
            elif contractor_id is not None:
                queryset = queryset.filter(contractor_id=contractor_id)
            queryset = queryset.order_by('-id')[offset:offset+limit]
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)