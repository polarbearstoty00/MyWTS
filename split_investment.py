# https://blog.naver.com/zacra/223530451234

# 투자할 종목! 예시.. 2개 종목 투자.
TargetStockList = ['QQQM','SCHD']

# 투자할 종목! 예시.. 2개 종목 투자.
TargetStockList = ['305540','329750']
# 305540 TIGER 2차전지테마
# 329750 TIGER 미국달러단기채권액티브

if stock_code == 'QQQM':

    #1차수 설정!!!
    SplitItem = {"number":1, "target_rate":10.0 , "trigger_rate":None , "invest_money":500}  #차수, 목표수익률, 매수기준 손실률 (1차수는 이 정보가 필요 없다),투자금액
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":2, "target_rate":2.0 , "trigger_rate":-3.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":3, "target_rate":3.0 , "trigger_rate":-4.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":4, "target_rate":3.0 , "trigger_rate":-5.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":5, "target_rate":3.0 , "trigger_rate":-5.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":6, "target_rate":4.0 , "trigger_rate":-6.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":7, "target_rate":4.0 , "trigger_rate":-6.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)   
    SplitItem = {"number":8, "target_rate":4.0 , "trigger_rate":-6.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":9, "target_rate":5.0 , "trigger_rate":-7.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
    SplitItem = {"number":10, "target_rate":5.0 , "trigger_rate":-7.0 , "invest_money":300} 
    SplitInfoList.append(SplitItem)
