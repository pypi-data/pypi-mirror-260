from django.db.models import Lookup


class BitEnumListAllLookup(Lookup):
    lookup_name = 'all'

    def as_sql(self, compiler, connection):
        field_sql, _ = self.process_lhs(compiler, connection)
        value_sql, _ = self.process_rhs(compiler, connection)
        params = [self.rhs, self.rhs]
        return f'{field_sql} & {value_sql} = {value_sql}', params
