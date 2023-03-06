from tradinghelper.models import Record


def get_trade_records():
    result = []
    records = Record.objects.all()
    for record in records:
        in_result = False
        for e in result:
            if e['type'] == record.strategy_type and e['params']==record.params:
                e['number_of_trades']+=1
                if record.benefit>0:
                    e['number_of_wins']+=1
                e['total_benefit']+=record.benefit
                in_result = True
        if in_result == False:
            result.append({'type':record.strategy_type, 'params':record.params, 'number_of_trades':1,'number_of_wins':( 1 if record.benefit>=0 else 0), 'total_benefit':record.benefit})
    return result