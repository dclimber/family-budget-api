from django.urls import reverse

from ...models import Budget
from ..permissions import IsOwnerOrReadOnly


class TestIsOwnerOrReadOnlyPermission:
    def test_safe_methods_are_accessible(self, api_rf, user1):
        budget = Budget(owner=user1, name='test')
        url = reverse('budget-detail', args=(budget.pk,))
        safe_methods = (
            api_rf.get,
            api_rf.head,
            api_rf.options
        )

        permission = IsOwnerOrReadOnly()

        for request in safe_methods:
            assert permission.has_object_permission(
                request(url), None, budget
            )

    def test_only_owner_can_access_unsafe_methods(self, api_rf, user1, user2):
        budget = Budget(owner=user1, name='test')
        url = reverse('budget-detail', args=(budget.pk,))
        unsafe_methods = (
            api_rf.post,
            api_rf.put,
            api_rf.patch,
            api_rf.delete
        )
        users = (
            (user1, True),
            (user2, False)
        )

        permission = IsOwnerOrReadOnly()

        for user, result in users:
            for request in unsafe_methods:
                request = request(url)
                request.user = user
                assert permission.has_object_permission(
                    request, None, budget
                ) == result
