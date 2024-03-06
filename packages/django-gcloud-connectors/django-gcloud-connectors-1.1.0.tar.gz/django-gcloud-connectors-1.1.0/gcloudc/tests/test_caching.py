from gcloudc.db.backends.datastore.caching import get_context

from . import TestCase
from .models import KeysOnlyModel


class RegressionsTestCase(TestCase):
    databases = "__all__"

    def test_keysonly_query_with_projection_returns_results_every_time(self):
        """Regression test for https://gitlab.com/potato-oss/google-cloud/django-gcloud-connectors/-/issues/56"""

        instance = KeysOnlyModel.objects.create(name="Alice", flag=False)

        # Clear the process cache as the create call adds `instance` to the
        # process cache
        get_context().reset(keep_disabled_flags=True)

        # Run two queries that result in a keys only query that use a projection
        first_queryset = KeysOnlyModel.objects.filter(
            pk__in=[instance.pk], flag=False
        ).values_list("id", flat=True)
        second_queryset = first_queryset.all()  # Clones the queryset above

        # Both should yield the same results
        self.assertEqual(list(first_queryset), [instance.pk])
        self.assertEqual(list(second_queryset), [instance.pk])
