import pyarrow
from datetime import date
from tzlocal import get_localzone


class KawaFilter:

    def __init__(self, column):
        self._column = column
        self._exclude = False
        self._clauses = []

    def exclude(self):
        self._exclude = True
        return self

    def add_clause(self, operator, value=None):
        self._clauses.append({
            'arguments': {'value': value} if value is not None else {},
            'operation': operator
        })
        return self

    def add_clause_for_date_filter(self, from_days, to_days):
        self._clauses.append({
            'arguments': {
                'dateFrom': from_days,
                'dateTo': to_days
            }
        })
        return self

    def add_clause_for_date_time_filter(self, instant_from, instant_to):
        self._clauses.append({
            'arguments': {
                'instantFrom': instant_from,
                'instantTo': instant_to
            }
        })
        return self

    def to_dict(self):
        return {
            'column': self._column.to_dict(),
            'exclude': self._exclude,
            'clauses': self._clauses,
        }

    # Empty / Not empty
    def not_empty(self):
        return self.add_clause('not_empty')

    def empty(self):
        return self.add_clause('empty')

    # Text clauses
    def in_list(self, values):
        return self.add_clause('in_list', values)

    def contains(self, value):
        return self.add_clause('contains', value)

    def ends_with(self, value):
        return self.add_clause('contains', value)

    def starts_with(self, value):
        return self.add_clause('contains', value)

    def does_not_contain(self, value):
        return self.add_clause('does_not_contain', value)

    def does_not_end_with(self, value):
        return self.add_clause('does_not_end_with', value)

    def does_not_start_with(self, value):
        return self.add_clause('does_not_start_with', value)

    # Temporal filters
    def weekdays_only(self):
        if self._clauses and self._clauses[0]['arguments']:
            self._clauses[0]['arguments']['keepWeekDaysOnly'] = True
        return self

    def yoy_ytd(self):
        self._clauses.append({'arguments': {'specialMode': 'YOY_YTD'}})
        return self

    def date_range(self, from_inclusive=None, to_inclusive=None):
        from_days = (from_inclusive - date(1970, 1, 1)).days if from_inclusive else None
        to_days = (to_inclusive - date(1970, 1, 1)).days if to_inclusive else None
        return self.add_clause_for_date_filter(
            from_days=from_days,
            to_days=to_days)

    def datetime_range(self, from_inclusive=None, to_inclusive=None):
        from_seconds = int(from_inclusive.timestamp()) if from_inclusive else None
        to_seconds = int(to_inclusive.timestamp()) if to_inclusive else None
        return self.add_clause_for_date_time_filter(
            instant_from=from_seconds,
            instant_to=to_seconds)

    # Numeric clauses
    def lt(self, value):
        return self.add_clause('lt', value)

    def lte(self, value):
        return self.add_clause('lte', value)

    def gt(self, value):
        return self.add_clause('gt', value)

    def gte(self, value):
        return self.add_clause('gte', value)

    def eq(self, value):
        return self.add_clause('eq', value)

    def ne(self, value):
        return self.add_clause('ne', value)


class KawaColumn:

    def __init__(self, column_name, column_regexp=None):
        self._aggregation_method = None
        self._column_name = column_name
        self._column_regexp = column_regexp

    def to_dict(self):
        return {
            'columnName': self.column_name(),
            'aggregationMethod': self.aggregation_method(),
            'columnRegexp': self.column_regexp(),
        }

    def column_regexp(self):
        return self._column_regexp

    def column_name(self):
        return self._column_name

    def aggregation_method(self):
        return self._aggregation_method

    def aggregate(self, aggregation_method):
        self._aggregation_method = aggregation_method.upper()
        return self

    def filter(self):
        return KawaFilter(self)

    def filter_with_list_of_values(self, values):
        return self.filter().in_list(values)

    # Filters
    def yoy_ytd(self):
        return self.filter().yoy_ytd()

    def date_range(self, from_inclusive=None, to_inclusive=None):
        return self.filter().date_range(from_inclusive, to_inclusive)

    def datetime_range(self, from_inclusive=None, to_inclusive=None):
        return self.filter().datetime_range(from_inclusive, to_inclusive)

    def empty(self):
        return self.filter().empty()

    def not_empty(self):
        return self.filter().not_empty()

    def in_list(self, *list_of_strings):
        return self.filter().in_list(list_of_strings)

    def starts_with(self, value):
        return self.filter().starts_with(value)

    def ends_with(self, value):
        return self.filter().ends_with(value)

    def contains(self, value):
        return self.filter().contains(value)

    def does_not_contain(self, value):
        return self.filter().does_not_contain(value)

    def does_not_start_with(self, value):
        return self.filter().does_not_start_with(value)

    def does_not_end_with(self, value):
        return self.filter().does_not_end_with(value)

    def gt(self, value):
        return self.filter().gt(value)

    def lt(self, value):
        return self.filter().lt(value)

    def gte(self, value):
        return self.filter().gte(value)

    def lte(self, value):
        return self.filter().lte(value)

    def eq(self, value):
        return self.filter().eq(value)

    def ne(self, value):
        return self.filter().ne(value)

    # Aggregations
    def first(self):
        return self.aggregate('first')

    def identical(self):
        return self.aggregate('identical')

    def identical_ignore_empty(self):
        return self.aggregate('identical_ignore_empty')

    def count(self):
        return self.aggregate('count')

    def count_unique(self):
        return self.aggregate('count_unique')

    def percent_filled(self):
        return self.aggregate('percent_filled')

    def percent_empty(self):
        return self.aggregate('percent_empty')

    def count_empty(self):
        return self.aggregate('count_empty')

    def sum(self):
        return self.aggregate('sum')

    def avg(self):
        return self.aggregate('avg')

    def median(self):
        return self.aggregate('median')

    def min(self):
        return self.aggregate('min')

    def max(self):
        return self.aggregate('max')

    def min_abs(self):
        return self.aggregate('min_abs')

    def max_abs(self):
        return self.aggregate('max_abs')

    def var_sample(self):
        return self.aggregate('var_sample')

    def var_pop(self):
        return self.aggregate('var_pop')

    def std_dev_sample(self):
        return self.aggregate('std_dev_sample')

    def std_dev_pop(self):
        return self.aggregate('std_dev_pop')

    def lowest_decile(self):
        return self.aggregate('lowest_decile')

    def lowest_quartile(self):
        return self.aggregate('lowest_quartile')

    def highest_decile(self):
        return self.aggregate('highest_decile')

    def highest_quartile(self):
        return self.aggregate('highest_quartile')


class KawaLazyQuery:

    def __init__(self, kawa_client, sheet_name, force_tz=None, no_output=False):
        self._k = kawa_client
        self._sheet_name = sheet_name
        self._group_by = None
        self._sample = None
        self._order_by = None
        self._as_user_id = None
        self._column_aggregations = []
        self._columns = []
        self._tz = force_tz if force_tz else str(get_localzone())
        self._filters = []
        self._limit = 100
        self._view_id = None
        self._no_output = no_output

    def widget(self, dashboard_name, widget_name):
        dashboards = self._k.entities.dashboards()
        dashboard = dashboards.get_entity(entity_name=dashboard_name)
        if dashboard is None:
            raise Exception('Dashboard with name {} not found in workspace'.format(dashboard_name))

        widgets = dashboard.get('widgets', [])
        for candidate_widget in widgets:
            candidate_widget_name = candidate_widget.get('displayInformation').get('displayName')
            if candidate_widget_name == widget_name:
                widget_definition = candidate_widget.get('definition')
                layout_id = widget_definition.get('layoutId')
                return self.view_id(layout_id)

        raise Exception('No widget with name {} was found in dashboard {}'.format(widget_name, dashboard_name))

    def view_id(self, view_id):
        self._view_id = str(view_id)
        return self

    def as_user_id(self, as_user_id):
        self._as_user_id = str(as_user_id)
        return self

    def filter(self, column_filter):
        self._filters.append(column_filter.to_dict())
        return self

    def group_by(self, column_name):
        self._group_by = column_name
        return self

    def order_by(self, column_name, ascending):
        self._order_by = {
            'columnName': column_name,
            'ascending': ascending
        }
        return self

    def select(self, *columns_or_column_names):
        columns = []
        for column_or_column_name in columns_or_column_names:
            if isinstance(column_or_column_name, KawaColumn):
                columns.append(column_or_column_name)
            else:
                column = KawaColumn(column_name=str(column_or_column_name))
                columns.append(column)

        self._columns = [c.to_dict() for c in columns]
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def no_limit(self):
        self._limit = -1
        return self

    def agg(self, *column_aggregations):
        self._column_aggregations = [c.to_dict() for c in column_aggregations]
        return self

    def sample(self, sampler, how_many_buckets=10, bucket_size=10, buckets=None):
        self._sample = {
            'sampler': sampler,
            'howManyBuckets': how_many_buckets,
            'bucketSize': bucket_size,
            'buckets': buckets
        }
        return self

    def compute(self, skip_cache=False):
        return self.collect(skip_cache=skip_cache)

    def collect(self, skip_cache=False):
        url = '{}/computation/compute-from-dsl'.format(self._k.kawa_api_url)

        body = {
            'sheetName': self._sheet_name,
            'timeZone': self._tz,
            'limit': self._limit,
            'skipCache': skip_cache,
            'noOutput': self._no_output
        }

        if self._group_by is not None:
            body['groupBy'] = self._group_by

        if self._sample is not None:
            body['sample'] = self._sample

        if self._column_aggregations:
            body['aggregation'] = {'columns': self._column_aggregations}

        if self._columns:
            body['select'] = {'columns': self._columns}

        if self._filters:
            body['filters'] = self._filters

        if self._order_by:
            body['orderBy'] = self._order_by

        if self._view_id:
            body['viewId'] = self._view_id

        if self._as_user_id:
            body['asUserId'] = self._as_user_id

        response = self._k.post(url=url, data=body, stream=True)

        if self._no_output:
            return

        with pyarrow.ipc.open_stream(response.content) as reader:
            return reader.read_pandas()

    def schema(self):
        sheet = self._k.entities.sheets().get_entity(self._sheet_name)
        if not sheet:
            raise Exception('Sheet with name {} was not found in the current workspace'.format(self._sheet_name))

        indicator_columns = sheet.get('indicatorColumns', [])
        computed_columns = sheet.get('computedColumns', [])

        return [{c['displayInformation']['displayName']: c['type']} for c in [*indicator_columns, *computed_columns]]
