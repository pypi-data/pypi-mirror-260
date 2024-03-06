from unittest import mock

import google

from gcloudc.db.backends.datastore.caching import get_context
from . import TestCase
from .models import NullableFieldModel, StringPkModel, KeysOnlyModel


class QueryByKeysTest(TestCase):
    """
        Tests for the Get optimisation when keys are
        included in all branches of a query.
    """

    databases = "__all__"

    def test_missing_results_are_skipped(self):
        NullableFieldModel.objects.create(pk=1)
        NullableFieldModel.objects.create(pk=5)

        results = NullableFieldModel.objects.filter(
            pk__in=[1, 2, 3, 4, 5]
        ).order_by("nullable").values_list("pk", flat=True)

        self.assertCountEqual(results, [1, 5])

    def test_none_namespace(self):
        NullableFieldModel.objects.using("nonamespace").create(pk=1)
        NullableFieldModel.objects.using("nonamespace").create(pk=5)

        results = NullableFieldModel.objects.using(
            "nonamespace").filter(
                pk__in=[1, 2, 3, 4, 5]
        ).order_by("nullable").values_list("pk", flat=True)

        self.assertCountEqual(results, [1, 5])

    def test_large_number_of_keys(self):
        keys = []

        for i in range(1001):
            keys.append(NullableFieldModel.objects.create(pk=i + 1).pk)

        try:
            results = list(NullableFieldModel.objects.filter(pk__in=keys))
        except google.api_core.exceptions.InvalidArgument:
            self.fail("Didn't correctly deal with a large number of keys")

        self.assertEqual(len(results), 1001)
        self.assertCountEqual([x.pk for x in results], keys)

    def test_multiple_pk_filters(self):
        for i in range(10):
            NullableFieldModel.objects.create(pk=i + 1)

        qs = NullableFieldModel.objects.all()
        self.assertEqual(qs.count(), 10)

        qs = qs.filter(pk__lt=10)
        self.assertEqual(qs.count(), 9)

        qs = qs.filter(pk__gte=2)
        self.assertEqual(qs.count(), 8)

        qs = qs.filter(pk__gte=3)
        self.assertEqual(qs.count(), 7)

    def test_multiple_str_pk_filters(self):
        for i in range(9):
            StringPkModel.objects.create(pk=str(i + 1))

        qs = StringPkModel.objects.all()
        self.assertEqual(qs.count(), 9)

        qs = qs.filter(pk__lt=str(9))
        self.assertEqual(qs.count(), 8)

        qs = qs.filter(pk__gte=str(2))
        self.assertEqual(qs.count(), 7)

        qs = qs.filter(pk__gte=str(3))
        self.assertEqual(qs.count(), 6)

    def test_projection_query_not_cached(self):
        instance = KeysOnlyModel.objects.create(name="Alice", flag=False)

        # Clear the process cache as the create call will add it
        get_context().reset(keep_disabled_flags=True)

        # Run two queries that result in a keys only query and use a projection
        with mock.patch("gcloudc.db.backends.datastore.caching.add_entities_to_cache") as add_entities_to_cache:

            # Running a non-projection should put to cache
            list(KeysOnlyModel.objects.filter(pk__in=[instance.pk], flag=False))
            add_entities_to_cache.assert_called()

            get_context().reset(keep_disabled_flags=True)
            add_entities_to_cache.reset_mock()

            # Running a query that uses a projection should not
            list(KeysOnlyModel.objects.filter(pk__in=[instance.pk], flag=False).values_list("id", flat=True))
            add_entities_to_cache.assert_not_called()
