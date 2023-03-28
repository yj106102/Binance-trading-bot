from tradinghelper.models import Record


def get_trade_records():
    # 데이터베이스의 전략 기록을 배열으로 반환
    result = []
    records = Record.objects.all()
    for record in records:
        in_result = False
        for element in result:
            if element['type'] == record.strategy_type and element['params']==record.params:
                element['number_of_trades']+=1
                if record.benefit>0:
                    element['number_of_wins']+=1
                element['total_benefit']+=record.benefit
                in_result = True
        if in_result == False:
            result.append({'type':record.strategy_type, 'params':record.params, 'number_of_trades':1,'number_of_wins':( 1 if record.benefit>=0 else 0), 'total_benefit':record.benefit})
    return result