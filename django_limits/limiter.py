from .exceptions import LimitExceeded
from django.conf import settings
from django.db.models import Q
from django.db.models.sql.where import WhereNode


LOOKUPS = {
    'in': lambda x, y: x in y,
    'exact': lambda x, y: x == y,
    'iexact': lambda x, y: str(x).lower() == str(y).lower(),
    'lt': lambda x, y: x < y,
    'lte': lambda x, y: x <= y,
    'gt': lambda x, y: x > y,
    'gte': lambda x, y: x >= y,
}


class Limiter(object):
    rules = {
        # ModelClass: [rule, rule, etc...]
    }

    def __call__(self, model, **kwargs):
        instance = kwargs['instance']
        if model in self.rules.keys():
            if type(self.rules[model]) is dict:
                rules = [self.rules[model]]
            else:
                rules = self.rules[model]
            for rule in rules:
                qs = self.get_queryset(model, rule)
                fs = self.get_filterset(rule)

                # If the filterset is None, we don't care about attributes
                # If there is a filterset, check this new instance matches
                matches = fs is None or self.instance_matches_filterset(instance, fs)
                if matches:
                    if instance.pk:
                        # This instance exists and match the filterset
                        offset = 0
                    else:
                        # This is a new object, add one to account for the new matching entry
                        offset = 1

                    count_after_save = qs.count() + offset

                    if count_after_save > rule['limit'] or rule['limit'] == 0:
                        raise LimitExceeded(
                            model=model,
                            details=rule,
                            template=rule.get('template', None)
                        )

    def get_filterset(self, rule):
        return rule.get('filterset', None)

    def get_queryset(self, model, rule):
        filters = self.get_filterset(rule)
        if not filters:
            return model.objects.all()
        else:
            return model.objects.filter(filters)

    def instance_matches_filterset(self, instance, clauses):
        model_matches_queryset = True

        for node in clauses.children:
            node_matches_queryset = True
            if type(node) == Q:
                if node.connector == 'AND':
                    node_matches_queryset &= self.instance_matches_filterset(instance, node)
                elif node.connector == 'OR':
                    node_matches_queryset |= self.instance_matches_filterset(instance, node)

                if node.negated:
                    node_matches_queryset = ~node_matches_queryset

                model_matches_queryset = node_matches_queryset
            else:
                lhs, rhs = node
                lhs, lookup_name = self.get_lhs_value(instance, lhs)

                if lookup_name in LOOKUPS.keys():
                    model_matches_queryset &= LOOKUPS[lookup_name](lhs, rhs)
                else:
                    raise NotImplementedError(
                        "Matching with lookup [{lookup}] not supported".format(lookup=node.lookup_name)
                    )
        return model_matches_queryset

    def get_lhs_value(self, instance, join):
        value = instance

        for lookup in LOOKUPS.keys():
            if join.endswith('__%s' % lookup):
                join, lookup = join.rsplit('__', 1)
                break
        else:
            lookup = 'exact'

        for jump in join.split('__'):
            value = getattr(value, jump)

        return value, lookup
