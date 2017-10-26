from django.contrib.gis.db import models


class PDV(models.Model):
    tradingName = models.TextField(db_column='trading_name')
    ownerName = models.TextField(db_column='owner_name')
    document = models.CharField(unique=True, max_length=14)
    coverageArea = models.MultiPolygonField(db_column='coverage_area')
    address = models.PointField()

    def __str__(self):
        return self.tradingName
