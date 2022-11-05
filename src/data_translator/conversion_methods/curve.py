from ..util import float_calculator


def convert(current_source_item, source_file, source_key):
    values = {}
    stat_types = []
    base_stat_values = []
    curve_types = []
    for index, stat in enumerate(current_source_item[source_key]):
        for value in stat:
            if type(stat[value]) == str and stat[value].startswith('GROW_CURVE'):
                curve_type = stat[value]
                curve_types.append(curve_type)
            elif type(stat[value]) == str and stat[value].startswith('FIGHT_PROP'):
                stat_type = stat[value]
                stat_types.append(stat_type)
            elif type(stat[value]) == float:
                base_value = stat[value]
                base_stat_values.append(base_value)

        if len(stat_types) <= index:
            stat_types.append(None)
        if len(base_stat_values) <= index:
            base_stat_values.append(1)
        if len(curve_types) <= index:
            curve_types.append(None)

    for level in source_file:
        stats = []
        for index, curve_type in enumerate(curve_types):
            stat = {'statType': stat_types[index]}

            for curve in level['curveInfos']:
                if curve['type'] == curve_type:
                    stat['value'] = float_calculator.calculate(base_stat_values[index], curve['value'], curve['arith'])
            stats.append(stat)

        values[level['level']] = stats
    return values
