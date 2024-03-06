from django.db.models import Lookup


class BitEnumListNoneLookup(Lookup):
    lookup_name = 'none'

    def as_sql(self, compiler, connection):
        field_sql, _ = self.process_lhs(compiler, connection)
        value_sql, _ = self.process_rhs(compiler, connection)
        params = [self.rhs]
        return f'{field_sql} & {value_sql} = 0', params
