from django.test import TestCase
from .models import PDV
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.db import IntegrityError
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse


### Testing Views ###
class ViewTestCase(TestCase):
    def setUp(self):
        pnt_near = Point(-46.671436, -23.582727)

        pol_near = Polygon(((-46.674944, -23.579866),
                            (-46.665377, -23.582828),
                            (-46.676696, -23.586689),
                            (-46.674944, -23.579866)))
        mpol_near = MultiPolygon(pol_near)

        self.pdv_near = PDV(tradingName='tradingnamenear',
                            ownerName='ownername',
                            document='54265143000154',
                            address=pnt_near,
                            coverageArea=mpol_near)

        pnt_far = Point(-23.582727, -46.671436)

        pol_far = Polygon(((-23.579866, -46.674944),
                           (-23.582828, -46.665377),
                           (-23.586689, -46.676696),
                           (-23.579866, -46.674944)))
        mpol_far = MultiPolygon(pol_far)

        self.pdv_far = PDV(tradingName='tradingname2',
                           ownerName='ownername2',
                           document='96710030000160',
                           address=pnt_far,
                           coverageArea=mpol_far)

        self.client = APIClient()
        self.pdvs_data = {
            "tradingName": "Adega Osasco",
            "ownerName": "Ze da Ambev",
            "document": "02.453.716/000170",
            "coverageArea": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [
                                -43.36556,
                                -22.99669
                            ],
                            [
                                -43.36539,
                                -23.01928
                            ],
                            [
                                -43.26583,
                                -23.01802
                            ],
                            [
                                -43.36556,
                                -22.99669
                            ]
                        ]
                    ]
                ]
            },
            "address": {
                "type": "Point",
                "coordinates": [
                    -43.297337,
                    -23.013538
                ]
            }
        }

    def test_api_create_pdv(self):
        response = self.client.post(
            reverse('create'),
            self.pdvs_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_same_document_api_create_pdv(self):
        # try to create pdv with same document
        self.client.post(reverse('create'), self.pdvs_data, format='json')
        response = self.client.post(reverse('create'), self.pdvs_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_invalid_document_api_create_pdv(self):
        # try to create pdv with invalid document
        self.pdvs_data['document'] = '00000000000000'
        self.client.post(reverse('create'), self.pdvs_data, format='json')
        response = self.client.post(reverse('create'), self.pdvs_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_by_id(self):
        self.pdv_near.save()
        pdv = PDV.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': pdv.id}),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, pdv)

    def test_fail_get_by_id(self):
        response = self.client.get(
            reverse('details', kwargs={'pk': 21342134}),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_pdv(self):
        self.pdv_near.save()
        self.pdv_far.save()

        response_near = self.client.get(
            reverse('search'),
            {'longlat': '-46.671436, -23.582727'})

        self.assertEqual(response_near.status_code, status.HTTP_200_OK)
        self.assertContains(response_near, self.pdv_near)

        response_far = self.client.get(
            reverse('search'),
            {'longlat': '-23.582727, -46.671436'})

        self.assertEqual(response_far.status_code, status.HTTP_200_OK)
        self.assertContains(response_far, self.pdv_far)

    def test_no_results_search_pdv(self):
        self.pdv_near.save()
        self.pdv_far.save()

        # location outside pdv_near coverage area
        response = self.client.get(
            reverse('search'),
            {'longlat': '-46.689718, -23.569197'})

        # should response OK with empty length
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['pdvs']), 0)


### Testing Models ###
class ModelsTestCase(TestCase):
    def setUp(self):
        pnt = Point(-46.671436, -23.582727)

        pol = Polygon(((-46.674944, -23.579866),
                       (-46.665377, -23.582828),
                       (-46.676696, -23.586689),
                       (-46.674944, -23.579866)))
        mpol = MultiPolygon(pol)

        self.store = PDV(tradingName='tradingname',
                         ownerName='ownername',
                         document='12345678901234',
                         address=pnt,
                         coverageArea=mpol)

    def test_create_pdv(self):
        old_count = PDV.objects.count()
        self.store.save()
        new_count = PDV.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_fail_create_pdv(self):
        try:
            self.store.save()
        except IntegrityError as e:
            pass
