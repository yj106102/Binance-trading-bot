from django.shortcuts import  HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import sys, os
import threading

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from trader import main
from stat_calc import get_trade_records

# Create your views here.
current_strategy = None


def index(request):
    # 기본 view
    current_strategy_article = None
    if current_strategy is None:
        current_strategy_article = """
        현재 트레이딩봇이 실행중이지 않습니다.
        """
    else:
        current_strategy_article = f"""
        현재 {current_strategy['type']} 전략이 실행중입니다.
    인자는 {str(current_strategy['params'])}입니다.
        """

    return HttpResponse(
        f"""
    <html>
        <p>{current_strategy_article}</p>
        <a href="/create/">새로운 전략 만들기</a>
        <a href="/records/">과거 전략 기록 보기</a>
        <form action = "/stop/" method = "post">
            <input type="submit" value="트레이딩봇 실행 중지">
        </form>


    """
    )



@csrf_exempt
def create_strategy(request):
    # 새로운 전략 생성
    global current_strategy
    if request.method == "GET":
        response = """
        <html>
        <body>
            <h1>새로운 전략 생성</h1>
            <form action="/create/" method="POST">

                <select name="type" >
                    <option value="">전략 선택</option>
                    <option value="RSI">RSI 매매</option>
                </select>
                <p>매수를 할 RSI 값을 입력해주세요<p>
                <input type="number" name="open_rsi_threshold" placeholder="0-50">
                <p>매도를 할 RSI 값을 입력해주세요<p>
                <input type="number" name="close_rsi_threshold" placeholder="0-100">
                <input type="submit"></p>
            <li><a href="/">메인 페이지로 돌아가기</a></li>
            </form>
        </body>
        </html>

        """
        return HttpResponse(response)
    elif request.method == "POST":
        type = request.POST["type"]
        if type == "":
            print("잘못된 입력입니다.")
            return redirect("/create/")
        print(request.POST["type"])
        try:
            symbols = [
                "ETH/USDT",
                "BTC/USDT",
                "XRP/USDT",
                "CFX/USDT",
                "OP/USDT",
                "APT/USDT",
                "MATIC/USDT",
            ]
            open_rsi_threshold = int(request.POST["open_rsi_threshold"])
            close_rsi_threshold = int(request.POST["close_rsi_threshold"])
            params = {
                "type": type,
                "params": {
                    "open_rsi_threshold": open_rsi_threshold,
                    "close_rsi_threshold": close_rsi_threshold,
                },
            }
            current_strategy = params
            trader_thread = threading.Thread(target=main.start_trade, args=(symbols, params))

            trader_thread.start()
            # strategy.append({'type': type, 'params':{'rsi_threshold': rsi}})
            return redirect("index")
        except:
            print("잘못된 입력입니다.")
            return redirect("/create/")


@csrf_exempt
def stop(request):
    # 전략 사용 중지
    global current_strategy
    if request.method == "POST":
        event = main.get_event()
        event.set()
        current_strategy = None
    return redirect("/")


def records(request):
    # 과거 거래 기록 열람
    trade_records = get_trade_records()
    article = ""
    for record in trade_records:
        article += f"""
            <p>거래 종류: {record['type']}</p>
            <p>파라미터: {record['params']}</p>
            <p>총 이득: {record['total_benefit']}, 총 거래 수: {record['number_of_trades']}</p>
            <p>승률: {record['number_of_wins']/record['number_of_trades']*100}%</p>
            <hr>
        """

    response = f"""
        <html>
        <body>
            <h1>과거 기록</h1>
            {article}
        </body>
        </html>

        """
    return HttpResponse(response)
