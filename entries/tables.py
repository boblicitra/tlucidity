# entries/tables.py
import django_tables2 as tables
from django_tables2.utils import A
from entries.models import Entry

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class ClientWidthColumn(tables.Column):
    def render(self, value):
        tmp_str = value.name + '                                       '
        fixed_width = tmp_str[0:35].title() + ' ' + value.code[0:2]
        return fixed_width

class ActiveWidthColumn(tables.Column):
    def render(self, value):
        tmp_str = value.code + ' ' + value.description[0:12]
        fixed_width = tmp_str
        return fixed_width


class ForReleaseTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input": 
                                        {"onclick": "toggle(this)"}},
                                        orderable=False)
    work_date = tables.Column(verbose_name='Service Date')
    client = tables.Column(verbose_name='Client')
    matter = tables.Column(orderable=False)
    hours = tables.Column(verbose_name='Hours',orderable=False)
    activity_code1 = ActiveWidthColumn(verbose_name='Activity Code 1',orderable=False)
    activity_code2 = ActiveWidthColumn(verbose_name='Activity Code 2',orderable=False)
    details = tables.LinkColumn('entry-detail', args=[A('pk')], orderable=False, empty_values=(), text="Details", verbose_name='')

    class Meta:
        model = Entry
        fields = ('selection',)
        attrs = {'class': 'paleblue'}


class DashTable(tables.Table):
    work_date = tables.Column(verbose_name='Service Date',orderable=False)
    client = ClientWidthColumn(verbose_name='Client Name including Company Code',orderable=False)
    matter = tables.Column(orderable=False)
    hours = SummingColumn(verbose_name='Hours',orderable=False)
    activity_code1 = ActiveWidthColumn(verbose_name='Activity Code 1',orderable=False)
    activity_code2 = ActiveWidthColumn(verbose_name='Activity Code 2',orderable=False)
    status = tables.Column(verbose_name='Status',orderable=False)
    edit = tables.LinkColumn('entry-edit', args=[A('pk')], orderable=False, empty_values=(), text="Edit", verbose_name='')

    class Meta:
        model = Entry
        fields = ('work_date',)
        attrs = {'class': 'paleblue'}


class FullTable(tables.Table):
    client = ClientWidthColumn(verbose_name='Client Name including Company Code',orderable=False)
    class Meta:
        model = Entry
        fields = ('who', 'work_date', 'client', 'matter', 'hours', 'activity_code1', 'activity_code2', 'status',)
        attrs = {'class': 'paleblue'}


class SelectedRelTable(tables.Table):
    activity_code1 = ActiveWidthColumn(verbose_name='Activity Code 1',orderable=False)
    activity_code2 = ActiveWidthColumn(verbose_name='Activity Code 2',orderable=False)
    selection = tables.CheckBoxColumn(accessor="pk",)
    class Meta:
        model = Entry
        fields = ('who', 'work_date', 'client', 'matter', 'hours',)
        attrs = {'class': 'paleblue'}

