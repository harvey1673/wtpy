from ctypes import c_uint32, cdll, c_char_p, c_bool, c_ulong, c_uint64, c_double, c_int, POINTER
from wtpy.WtCoreDefs import CB_STRATEGY_INIT, CB_STRATEGY_TICK, CB_STRATEGY_CALC, CB_STRATEGY_BAR, CB_STRATEGY_GET_BAR, CB_STRATEGY_GET_TICK, CB_STRATEGY_GET_POSITION, CB_STRATEGY_COND_TRIGGER
from wtpy.WtCoreDefs import CB_HFTSTRA_CHNL_EVT, CB_HFTSTRA_ENTRUST, CB_HFTSTRA_ORD, CB_HFTSTRA_TRD, CB_SESSION_EVENT
from wtpy.WtCoreDefs import CB_HFTSTRA_ORDQUE, CB_HFTSTRA_ORDDTL, CB_HFTSTRA_TRANS, CB_HFTSTRA_GET_ORDQUE, CB_HFTSTRA_GET_ORDDTL, CB_HFTSTRA_GET_TRANS
from wtpy.WtCoreDefs import CHNL_EVENT_READY, CHNL_EVENT_LOST, CB_ENGINE_EVENT
from wtpy.WtCoreDefs import FUNC_LOAD_HISBARS, FUNC_LOAD_HISTICKS, FUNC_LOAD_ADJFACTS
from wtpy.WtCoreDefs import EVENT_ENGINE_INIT, EVENT_SESSION_BEGIN, EVENT_SESSION_END, EVENT_ENGINE_SCHDL, EVENT_BACKTEST_END
from wtpy.WtCoreDefs import WTSTickStruct, WTSBarStruct, WTSOrdQueStruct, WTSOrdDtlStruct, WTSTransStruct
from .PlatformHelper import PlatformHelper as ph
from wtpy.WtUtilDefs import singleton
from wtpy.WtDataDefs import WtNpKline, WtNpOrdDetails, WtNpOrdQueues, WtNpTicks, WtNpTransactions
import os

# Python对接C接口的库
@singleton
class WtBtWrapper:
    '''
    Wt平台C接口底层对接模块
    '''

    # api可以作为公共变量
    api = None
    ver = "Unknown"

    _engine = None
    
    # 构造函数, 传入动态库名
    def __init__(self, engine):
        self._engine = engine
        paths = os.path.split(__file__)
        dllname = ph.getModule("WtBtPorter")
        a = (paths[:-1] + (dllname,))
        _path = os.path.join(*a)
        self.api = cdll.LoadLibrary(_path)
            
        self.api.get_version.restype = c_char_p
        self.api.cta_get_last_entertime.restype = c_uint64
        self.api.cta_get_first_entertime.restype = c_uint64
        self.api.cta_get_last_exittime.restype = c_uint64
        self.api.cta_get_detail_entertime.restype = c_uint64
        self.api.cta_get_last_entertag.restype = c_char_p
        self.api.cta_enter_long.argtypes = [c_ulong, c_char_p, c_double, c_char_p, c_double, c_double]
        self.api.cta_enter_short.argtypes = [c_ulong, c_char_p, c_double, c_char_p, c_double, c_double]
        self.api.cta_exit_long.argtypes = [c_ulong, c_char_p, c_double, c_char_p, c_double, c_double]
        self.api.cta_exit_short.argtypes = [c_ulong, c_char_p, c_double, c_char_p, c_double, c_double]
        self.api.cta_set_position.argtypes = [c_ulong, c_char_p, c_double, c_char_p, c_double, c_double]
        self.ver = bytes.decode(self.api.get_version())

        self.api.cta_save_userdata.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.cta_load_userdata.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.cta_load_userdata.restype = c_char_p

        self.api.cta_get_position.restype = c_double
        self.api.cta_get_position_profit.restype = c_double
        self.api.cta_get_position_avgpx.restype = c_double
        self.api.cta_get_detail_cost.restype = c_double
        self.api.cta_get_detail_profit.restype = c_double
        self.api.cta_get_price.restype = c_double
        self.api.cta_get_day_price.restype = c_double
        self.api.cta_get_fund_data.restype = c_double

        self.api.sel_save_userdata.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.sel_load_userdata.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.sel_load_userdata.restype = c_char_p
        self.api.sel_get_position.restype = c_double
        self.api.sel_set_position.argtypes = [c_ulong, c_char_p, c_double, c_char_p]
        self.api.sel_get_position_profit.restype = c_double
        self.api.sel_get_position_avgpx.restype = c_double
        self.api.sel_get_detail_cost.restype = c_double
        self.api.sel_get_detail_profit.restype = c_double
        self.api.sel_get_price.restype = c_double
        self.api.sel_get_day_price.restype = c_double
        self.api.sel_get_fund_data.restype = c_double
        self.api.sel_get_last_entertime.restype = c_uint64
        self.api.sel_get_first_entertime.restype = c_uint64
        self.api.sel_get_last_exittime.restype = c_uint64
        self.api.sel_get_detail_entertime.restype = c_uint64
        self.api.sel_get_last_entertag.restype = c_char_p

        self.api.hft_save_userdata.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.hft_load_userdata.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.hft_load_userdata.restype = c_char_p
        self.api.hft_get_position.restype = c_double
        self.api.hft_get_position_profit.restype = c_double
        self.api.hft_get_position_avgpx.restype = c_double
        self.api.hft_get_undone.restype = c_double
        self.api.hft_get_price.restype = c_double
        
        self.api.hft_buy.restype = c_char_p
        self.api.hft_buy.argtypes = [c_ulong, c_char_p, c_double, c_double, c_char_p, c_int]
        self.api.hft_sell.restype = c_char_p
        self.api.hft_sell.argtypes = [c_ulong, c_char_p, c_double, c_double, c_char_p, c_int]
        self.api.hft_cancel_all.restype = c_char_p

        self.api.cta_set_chart_kline.argtypes = [c_ulong, c_char_p, c_char_p]
        self.api.cta_add_chart_mark.argtypes = [c_ulong, c_double, c_char_p, c_char_p]
        self.api.cta_register_index.argtypes = [c_ulong, c_char_p, c_uint32]
        self.api.cta_register_index_line.argtypes = [c_ulong, c_char_p, c_char_p, c_uint32]
        self.api.cta_add_index_baseline.argtypes = [c_ulong, c_char_p, c_char_p, c_double]
        self.api.cta_set_index_value.argtypes = [c_ulong, c_char_p, c_char_p, c_double]

        self.api.set_time_range.argtypes = [c_uint64, c_uint64]
        self.api.enable_tick.argtypes = [c_bool]

        self.api.get_raw_stdcode.restype = c_char_p

    def on_engine_event(self, evtid:int, evtDate:int, evtTime:int):
        engine = self._engine
        if evtid == EVENT_ENGINE_INIT:
            engine.on_init()
        elif evtid == EVENT_ENGINE_SCHDL:
            engine.on_schedule(evtDate, evtTime)
        elif evtid == EVENT_SESSION_BEGIN:
            engine.on_session_begin(evtDate)
        elif evtid == EVENT_SESSION_END:
            engine.on_session_end(evtDate)
        elif evtid == EVENT_BACKTEST_END:
            engine.on_backtest_end()
        return

    def on_stra_init(self, id:int):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_init()
        return

    def on_session_event(self, id:int, udate:int, isBegin:bool):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            if isBegin:
                ctx.on_session_begin(udate)
            else:
                ctx.on_session_end(udate)
        return

    def on_stra_calc(self, id:int, curDate:int, curTime:int):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_calculate()
        return

    def on_stra_calc_done(self, id:int, curDate:int, curTime:int):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_calculate_done()
        return

    def on_stra_tick(self, id:int, stdCode:str, newTick:POINTER(WTSTickStruct)):
        engine = self._engine
        ctx = engine.get_context(id)

        if ctx is not None:
            ctx.on_tick(bytes.decode(stdCode), newTick)
        return
    
    def on_stra_bar(self, id:int, stdCode:str, period:str, newBar:POINTER(WTSBarStruct)):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_bar(bytes.decode(stdCode), bytes.decode(period), newBar)
        return

    def on_stra_get_bar(self, id:int, stdCode:str, period:str, curBar:POINTER(WTSBarStruct), count:int, isLast:bool):
        '''
        获取K线回调, 该回调函数因为是python主动发起的, 需要同步执行, 所以不走事件推送
        @id     策略id
        @stdCode   合约代码
        @period K线周期
        @curBar 最新一条K线
        @isLast 是否是最后一条
        '''
        engine = self._engine
        ctx = engine.get_context(id)
        period = bytes.decode(period)
        isDay = period[0]=='d'

        npBars = WtNpKline(isDay)
        npBars.set_data(curBar, count)

        if ctx is not None:
            ctx.on_getbars(bytes.decode(stdCode), period, npBars)

    def on_stra_get_tick(self, id:int, stdCode:str, curTick:POINTER(WTSTickStruct), count:int, isLast:bool):
        '''
        获取Tick回调, 该回调函数因为是python主动发起的, 需要同步执行, 所以不走事件推送
        @id         策略id
        @stdCode       合约代码
        @curTick    最新一笔Tick
        @isLast     是否是最后一条
        '''
        engine = self._engine
        ctx = engine.get_context(id)

        npTicks = WtNpTicks(forceCopy=False)
        npTicks.set_data(curTick, count)

        if ctx is not None:
            ctx.on_getticks(bytes.decode(stdCode), npTicks)
        return

    def on_stra_get_position(self, id:int, stdCode:str, qty:float, isLast:bool):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_getpositions(bytes.decode(stdCode), qty, isLast)

    def on_stra_cond_triggerd(self, id:int, stdCode:str, target:float, price:float, usertag:str):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_condition_triggered(bytes.decode(stdCode), target, price, bytes.decode(usertag))

    def on_hftstra_channel_evt(self, id:int, trader:str, evtid:int):
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is None:
            return
        if evtid == CHNL_EVENT_READY:
            ctx.on_channel_ready()
        elif evtid == CHNL_EVENT_LOST:
            ctx.on_channel_lost()

    def on_hftstra_order(self, id:int, localid:int, stdCode:str, isBuy:bool, totalQty:float, leftQty:float, price:float, isCanceled:bool, userTag:str):
        stdCode = bytes.decode(stdCode)
        userTag = bytes.decode(userTag,"gbk")
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_order(localid, stdCode, isBuy, totalQty, leftQty, price, isCanceled, userTag)

    def on_hftstra_trade(self, id:int, localid:int, stdCode:str, isBuy:bool, qty:float, price:float, userTag:str):
        stdCode = bytes.decode(stdCode)
        userTag = bytes.decode(userTag,"gbk")
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_trade(localid, stdCode, isBuy, qty, price, userTag)

    def on_hftstra_entrust(self, id:int, localid:int, stdCode:str, bSucc:bool, message:str, userTag:str):
        stdCode = bytes.decode(stdCode)
        message = bytes.decode(message, "gbk")
        userTag = bytes.decode(userTag, "gbk")
        engine = self._engine
        ctx = engine.get_context(id)
        if ctx is not None:
            ctx.on_entrust(localid, stdCode, bSucc, message, userTag)

    def on_hftstra_order_queue(self, id:int, stdCode:str, newOrdQue:POINTER(WTSOrdQueStruct)):
        stdCode = bytes.decode(stdCode)
        engine = self._engine
        ctx = engine.get_context(id)
      
        if ctx is not None:
            ctx.on_order_queue(stdCode, newOrdQue.to_tuple())

    def on_hftstra_get_order_queue(self, id:int, stdCode:str, newOrdQue:POINTER(WTSOrdQueStruct), count:int, isLast:bool):
        engine = self._engine
        ctx = engine.get_context(id)
        
        npHftData = WtNpOrdQueues(forceCopy=False)
        npHftData.set_data(newOrdQue, count)

        if ctx is not None:
            ctx.on_get_order_queue(bytes.decode(stdCode), npHftData)

    def on_hftstra_order_detail(self, id:int, stdCode:str, newOrdDtl:POINTER(WTSOrdDtlStruct)):
        stdCode = bytes.decode(stdCode)
        engine = self._engine
        ctx = engine.get_context(id)
        
        if ctx is not None:
            ctx.on_order_detail(stdCode, newOrdDtl.to_tuple())

    def on_hftstra_get_order_detail(self, id:int, stdCode:str, newOrdDtl:POINTER(WTSOrdDtlStruct), count:int, isLast:bool):
        engine = self._engine
        ctx = engine.get_context(id)
        
        npHftData = WtNpOrdDetails(forceCopy=False)
        npHftData.set_data(newOrdDtl, count)
            
        if ctx is not None:
            ctx.on_get_order_detail(bytes.decode(stdCode), npHftData)

    def on_hftstra_transaction(self, id:int, stdCode:str, newTrans:POINTER(WTSTransStruct)):
        stdCode = bytes.decode(stdCode)
        engine = self._engine
        ctx = engine.get_context(id)
        
        if ctx is not None:
            ctx.on_transaction(stdCode, newTrans.to_tuple())
        
    def on_hftstra_get_transaction(self, id:int, stdCode:str, newTrans:POINTER(WTSTransStruct), count:int, isLast:bool):
        engine = self._engine
        ctx = engine.get_context(id)

        npHftData = WtNpTransactions(forceCopy=False)
        npHftData.set_data(newTrans, count)
            
        if ctx is not None:
            ctx.on_get_transaction(bytes.decode(stdCode), npHftData)

    def on_load_fnl_his_bars(self, stdCode:str, period:str) -> bool:
        engine = self._engine
        loader = engine.get_extended_data_loader()
        if loader is None:
            return False

        return loader.load_final_his_bars(bytes.decode(stdCode), bytes.decode(period), self.api.feed_raw_bars)

    def on_load_raw_his_bars(self, stdCode:str, period:str) -> bool:
        engine = self._engine
        loader = engine.get_extended_data_loader()
        if loader is None:
            return False

        return loader.load_raw_his_bars(bytes.decode(stdCode), bytes.decode(period), self.api.feed_raw_bars)

    def feed_adj_factors(self, stdCode:str, dates:list, factors:list):
        stdCode = bytes(stdCode, encoding="utf8")
        '''
        TODO 这里类型要转一下! 底层接口是传数组的
        feed_adj_factors(WtString stdCode, WtUInt32* dates, double* factors, WtUInt32 count)
        '''
        self.api.feed_adj_factors(stdCode, dates, factors, len(dates))

    def on_load_adj_factors(self, stdCode:str) -> bool:
        engine = self._engine
        loader = engine.get_extended_data_loader()
        if loader is None:
            return False

        stdCode = bytes.decode(stdCode)
        return loader.load_adj_factors(stdCode, self.feed_adj_factors)

    def on_load_his_ticks(self, stdCode:str, uDate:int) -> bool:
        engine = self._engine
        loader = engine.get_extended_data_loader()
        if loader is None:
            return False
        
        # feed_raw_ticks(WTSTickStruct* ticks, WtUInt32 count);
        return loader.load_his_ticks(bytes.decode(stdCode), uDate, self.api.feed_raw_ticks)

    def write_log(self, level, message:str, catName:str = ""):
        self.api.write_log(level, ph.auto_encode(message), bytes(catName, encoding = "utf8"))

    def set_time_range(self, beginTime:int, endTime:int):
        '''
        设置回测时间区间
        @beginTime  开始时间, 格式如yyyymmddHHMM
        @endTime    结束时间, 格式如yyyymmddHHMM
        '''
        self.api.set_time_range(beginTime, endTime)

    def enable_tick(self, bEnabled:bool = True):
        '''
        启用tick回测
        @bEnabled   是否启用
        '''
        self.api.enable_tick(bEnabled)

    ### 实盘和回测有差异 ###
    def run_backtest(self, bNeedDump:bool = False, bAsync:bool = False):
        self.api.run_backtest(bNeedDump, bAsync)

    def stop_backtest(self):
        self.api.stop_backtest()

    def release_backtest(self):
        self.api.release_backtest()

    def clear_cache(self):
        self.api.clear_cache()

    def get_raw_stdcode(self, stdCode:str):
        return bytes.decode(self.api.get_raw_stdcode(bytes(stdCode, encoding = "utf8")))

    def config_backtest(self, cfgfile:str = 'config.yaml', isFile:bool = True):
        self.api.config_backtest(bytes(cfgfile, encoding = "utf8"), isFile)
    ### 实盘和回测有差异 ###

    def initialize_cta(self, logCfg:str = "logcfgbt.yaml", isFile:bool = True, outDir:str = "./outputs_bt"):
        '''
        C接口初始化
        '''
        self.cb_stra_init = CB_STRATEGY_INIT(self.on_stra_init)
        self.cb_stra_tick = CB_STRATEGY_TICK(self.on_stra_tick)
        self.cb_stra_calc = CB_STRATEGY_CALC(self.on_stra_calc)
        self.cb_stra_calc_done = CB_STRATEGY_CALC(self.on_stra_calc_done)
        self.cb_stra_bar = CB_STRATEGY_BAR(self.on_stra_bar)
        self.cb_session_event = CB_SESSION_EVENT(self.on_session_event)
        self.cb_stra_cond_trigger = CB_STRATEGY_COND_TRIGGER(self.on_stra_cond_triggerd)

        self.cb_engine_event = CB_ENGINE_EVENT(self.on_engine_event)
        try:
            self.api.register_evt_callback(self.cb_engine_event)
            self.api.register_cta_callbacks(self.cb_stra_init, self.cb_stra_tick, 
                self.cb_stra_calc, self.cb_stra_bar, self.cb_session_event, self.cb_stra_calc_done, self.cb_stra_cond_trigger)
            self.api.init_backtest(bytes(logCfg, encoding = "utf8"), isFile, bytes(outDir, encoding = "utf8"))
        except OSError as oe:
            print(oe)

        self.write_log(102, "WonderTrader CTA backtest framework initialzied, version: %s" % (self.ver))

    def initialize_hft(self, logCfg:str = "logcfgbt.yaml", isFile:bool = True, outDir:str = "./outputs_bt"):
        '''
        C接口初始化
        '''
        self.cb_stra_init = CB_STRATEGY_INIT(self.on_stra_init)
        self.cb_stra_tick = CB_STRATEGY_TICK(self.on_stra_tick)
        self.cb_stra_bar = CB_STRATEGY_BAR(self.on_stra_bar)
        self.cb_session_event = CB_SESSION_EVENT(self.on_session_event)

        self.cb_hftstra_channel_evt = CB_HFTSTRA_CHNL_EVT(self.on_hftstra_channel_evt)
        self.cb_hftstra_order = CB_HFTSTRA_ORD(self.on_hftstra_order)
        self.cb_hftstra_trade = CB_HFTSTRA_TRD(self.on_hftstra_trade)
        self.cb_hftstra_entrust = CB_HFTSTRA_ENTRUST(self.on_hftstra_entrust)
        self.cb_hftstra_order_detail = CB_HFTSTRA_ORDDTL(self.on_hftstra_order_detail)
        self.cb_hftstra_order_queue = CB_HFTSTRA_ORDQUE(self.on_hftstra_order_queue)
        self.cb_hftstra_transaction = CB_HFTSTRA_TRANS(self.on_hftstra_transaction)

        self.cb_engine_event = CB_ENGINE_EVENT(self.on_engine_event)

        try:
            self.api.register_evt_callback(self.cb_engine_event)
            self.api.register_hft_callbacks(self.cb_stra_init, self.cb_stra_tick, self.cb_stra_bar, 
                self.cb_hftstra_channel_evt, self.cb_hftstra_order, self.cb_hftstra_trade, 
                self.cb_hftstra_entrust, self.cb_hftstra_order_detail, self.cb_hftstra_order_queue, 
                self.cb_hftstra_transaction, self.cb_session_event)
            self.api.init_backtest(bytes(logCfg, encoding = "utf8"), isFile, bytes(outDir, encoding = "utf8"))
        except OSError as oe:
            print(oe)

        self.write_log(102, "WonderTrader HFT backtest framework initialzied, version: %s" % (self.ver))

    def initialize_sel(self, logCfg:str = "logcfgbt.yaml", isFile:bool = True, outDir:str = "./outputs_bt"):
        '''
        C接口初始化
        '''
        self.cb_stra_init = CB_STRATEGY_INIT(self.on_stra_init)
        self.cb_stra_tick = CB_STRATEGY_TICK(self.on_stra_tick)
        self.cb_stra_calc = CB_STRATEGY_CALC(self.on_stra_calc)
        self.cb_stra_calc_done = CB_STRATEGY_CALC(self.on_stra_calc_done)
        self.cb_stra_bar = CB_STRATEGY_BAR(self.on_stra_bar)
        self.cb_session_event = CB_SESSION_EVENT(self.on_session_event)

        self.cb_engine_event = CB_ENGINE_EVENT(self.on_engine_event)

        try:
            self.api.register_evt_callback(self.cb_engine_event)
            self.api.register_sel_callbacks(self.cb_stra_init, self.cb_stra_tick, 
                self.cb_stra_calc, self.cb_stra_bar, self.cb_session_event, self.cb_stra_calc_done)
            self.api.init_backtest(bytes(logCfg, encoding = "utf8"), isFile, bytes(outDir, encoding = "utf8"))
        except OSError as oe:
            print(oe)

        self.write_log(102, "WonderTrader SEL backtest framework initialzied, version: %s" % (self.ver))

    def register_extended_data_loader(self, bAutoTrans:bool = True):
        '''
        注册扩展历史数据加载器
        @bAutoTrans 是否自动转储
        '''
        self.cb_load_fnlbars = FUNC_LOAD_HISBARS(self.on_load_fnl_his_bars)
        self.cb_load_rawbars = FUNC_LOAD_HISBARS(self.on_load_raw_his_bars)
        self.cb_load_histicks = FUNC_LOAD_HISTICKS(self.on_load_his_ticks)
        self.cb_load_adjfacts = FUNC_LOAD_ADJFACTS(self.on_load_adj_factors)
        self.api.register_ext_data_loader(self.cb_load_fnlbars, self.cb_load_rawbars, self.cb_load_adjfacts, self.cb_load_histicks, bAutoTrans)

    def cta_enter_long(self, id:int, stdCode:str, qty:float, usertag:str, limitprice:float = 0.0, stopprice:float = 0.0):
        '''
        开多
        @id         策略id
        @stdCode    合约代码
        @qty        手数, 大于等于0
        '''
        self.api.cta_enter_long(id, bytes(stdCode, encoding = "utf8"), qty, bytes(usertag, encoding = "utf8"), limitprice, stopprice)

    def cta_exit_long(self, id:int, stdCode:str, qty:float, usertag:str, limitprice:float = 0.0, stopprice:float = 0.0):
        '''
        平多
        @id         策略id
        @stdCode    合约代码
        @qty        手数, 大于等于0
        '''
        self.api.cta_exit_long(id, bytes(stdCode, encoding = "utf8"), qty, bytes(usertag, encoding = "utf8"), limitprice, stopprice)

    def cta_enter_short(self, id:int, stdCode:str, qty:float, usertag:str, limitprice:float = 0.0, stopprice:float = 0.0):
        '''
        开空
        @id         策略id
        @stdCode    合约代码
        @qty        手数, 大于等于0
        '''
        self.api.cta_enter_short(id, bytes(stdCode, encoding = "utf8"), qty, bytes(usertag, encoding = "utf8"), limitprice, stopprice)

    def cta_exit_short(self, id:int, stdCode:str, qty:float, usertag:str, limitprice:float = 0.0, stopprice:float = 0.0):
        '''
        平空
        @id         策略id
        @stdCode    合约代码
        @qty        手数, 大于等于0
        '''
        self.api.cta_exit_short(id, bytes(stdCode, encoding = "utf8"), qty, bytes(usertag, encoding = "utf8"), limitprice, stopprice)
    
    def cta_get_bars(self, id:int, stdCode:str, period:str, count:int, isMain:bool):
        '''
        读取K线
        @id         策略id
        @stdCode    合约代码
        @period     周期, 如m1/m3/d1等
        @count      条数
        @isMain     是否主K线
        '''
        return self.api.cta_get_bars(id, bytes(stdCode, encoding = "utf8"), bytes(period, encoding = "utf8"), count, isMain, CB_STRATEGY_GET_BAR(self.on_stra_get_bar))
    
    def cta_get_ticks(self, id:int, stdCode:str, count:int):
        '''
        读取Tick
        @id         策略id
        @stdCode    合约代码
        @count      条数
        '''
        return self.api.cta_get_ticks(id, bytes(stdCode, encoding = "utf8"), count, CB_STRATEGY_GET_TICK(self.on_stra_get_tick))

    def cta_get_position_profit(self, id:int, stdCode:str):
        '''
        获取浮动盈亏
        @id         策略id
        @stdCode    合约代码
        @return     指定合约的浮动盈亏
        '''
        return self.api.cta_get_position_profit(id, bytes(stdCode, encoding = "utf8"))

    def cta_get_position_avgpx(self, id:int, stdCode:str):
        '''
        获取持仓均价
        @id         策略id
        @stdCode    合约代码
        @return     指定合约的持仓均价
        '''
        return self.api.cta_get_position_avgpx(id, bytes(stdCode, encoding = "utf8"))

    def cta_get_all_position(self, id:int):
        '''
        获取全部持仓
        @id     策略id
        '''
        return self.api.cta_get_all_position(id, CB_STRATEGY_GET_POSITION(self.on_stra_get_position))
    
    def cta_get_position(self, id:int, stdCode:str, bonlyvalid:bool = False, usertag:str = ""):
        '''
        获取持仓
        @id     策略id
        @stdCode    合约代码
        @usertag    进场标记, 如果为空则获取该合约全部持仓
        @return 指定合约的持仓手数, 正为多, 负为空
        '''
        return self.api.cta_get_position(id, bytes(stdCode, encoding = "utf8"), bonlyvalid, bytes(usertag, encoding = "utf8"))

    def cta_get_fund_data(self, id:int, flag:int) -> float:
        '''
        获取资金数据
        @id     策略id
        @flag   0-动态权益, 1-总平仓盈亏, 2-总浮动盈亏, 3-总手续费
        @return 资金数据
        '''
        return self.api.cta_get_fund_data(id, flag)

    def cta_get_price(self, stdCode:str) -> float:
        '''
        @stdCode   合约代码
        @return     指定合约的最新价格 
        '''
        return self.api.cta_get_price(bytes(stdCode, encoding = "utf8"))

    def cta_get_day_price(self, stdCode:str, flag:int = 0) -> float:
        '''
        获取当日价格
        @stdCode    合约代码
        @flag       价格标记, 0-开盘价, 1-最高价, 2-最低价, 3-最新价
        @return     指定合约的价格 
        '''
        return self.api.cta_get_day_price(bytes(stdCode, encoding = "utf8"), flag)

    def cta_set_position(self, id:int, stdCode:str, qty:float, usertag:str = "", limitprice:float = 0.0, stopprice:float = 0.0):
        '''
        设置目标仓位
        @id         策略id
        @stdCode    合约代码
        @qty        目标仓位, 正为多, 负为空
        '''
        self.api.cta_set_position(id, bytes(stdCode, encoding = "utf8"), qty, bytes(usertag, encoding = "utf8"), limitprice, stopprice)

    def cta_get_tdate(self) -> int:
        '''
        获取当前交易日
        @return    当前交易日
        '''
        return self.api.cta_get_tdate()

    def cta_get_date(self) -> int:
        '''
        获取当前日期
        @return    当前日期 
        '''
        return self.api.cta_get_date()

    def cta_get_time(self) -> int:
        '''
        获取当前时间
        @return    当前时间 
        '''
        return self.api.cta_get_time()

    def cta_get_first_entertime(self, id:int, stdCode:str) -> int:
        '''
        获取当前持仓的首次进场时间
        @stdCode    合约代码
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.cta_get_first_entertime(id, bytes(stdCode, encoding = "utf8"))

    def cta_get_last_entertime(self, id:int, stdCode:str) -> int:
        '''
        获取当前持仓的最后进场时间
        @stdCode    合约代码
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.cta_get_last_entertime(id, bytes(stdCode, encoding = "utf8"))

    def cta_get_last_entertag(self, id:int, stdCode:str) -> str:
        '''
        获取当前持仓的最后进场标记
        @stdCode    合约代码
        @return     进场标记 
        '''
        return bytes.decode(self.api.cta_get_last_entertag(id, bytes(stdCode, encoding = "utf8")))

    def cta_get_last_exittime(self, id:int, stdCode:str) -> int:
        '''
        获取当前持仓的最后出场时间
        @stdCode    合约代码
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.cta_get_last_exittime(id, bytes(stdCode, encoding = "utf8"))

    def cta_log_text(self, id:int, level:int, message:str):
        '''
        日志输出
        @id         策略ID
        @level      日志级别
        @message    日志内容
        '''
        self.api.cta_log_text(id, level, ph.auto_encode(message))

    def cta_get_detail_entertime(self, id:int, stdCode:str, usertag:str) -> int:
        '''
        获取指定标记的持仓的进场时间
        @id         策略id
        @stdCode    合约代码
        @usertag    进场标记
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.cta_get_detail_entertime(id, bytes(stdCode, encoding = "utf8"), bytes(usertag, encoding = "utf8")) 

    def cta_get_detail_cost(self, id:int, stdCode:str, usertag:str) -> float:
        '''
        获取指定标记的持仓的开仓价
        @id         策略id
        @stdCode    合约代码
        @usertag    进场标记
        @return     开仓价 
        '''
        return self.api.cta_get_detail_cost(id, bytes(stdCode, encoding = "utf8"), bytes(usertag, encoding = "utf8")) 

    def cta_get_detail_profit(self, id:int, stdCode:str, usertag:str, flag:int):
        '''
        获取指定标记的持仓的盈亏
        @id         策略id
        @stdCode       合约代码
        @usertag    进场标记
        @flag       盈亏记号, 0-浮动盈亏, 1-最大浮盈, -1-最大亏损（负数）, 2-最大浮盈价格， -2-最大浮亏价格
        @return     盈亏 
        '''
        return self.api.cta_get_detail_profit(id, bytes(stdCode, encoding = "utf8"), bytes(usertag, encoding = "utf8"), flag) 

    def cta_save_user_data(self, id:int, key:str, val:str):
        '''
        保存用户数据
        @id         策略id
        @key        数据名
        @val        数据值
        '''
        self.api.cta_save_userdata(id, bytes(key, encoding = "utf8"), bytes(val, encoding = "utf8"))

    def cta_load_user_data(self, id:int, key:str, defVal:str  = ""):
        '''
        加载用户数据
        @id         策略id
        @key        数据名
        @defVal     默认值
        '''
        ret = self.api.cta_load_userdata(id, bytes(key, encoding = "utf8"), bytes(defVal, encoding = "utf8"))
        return bytes.decode(ret)

    def cta_sub_ticks(self, id:int, stdCode:str):
        '''
        订阅行情
        @id         策略id
        @stdCode    品种代码
        '''
        self.api.cta_sub_ticks(id, bytes(stdCode, encoding = "utf8"))

    def cta_sub_bar_events(self, id:int, stdCode:str, period:str):
        '''
        订阅K线事件
        @id         策略id
        @stdCode    品种代码
        @period     周期
        '''
        self.api.cta_sub_bar_events(id, bytes(stdCode, encoding = "utf8"), bytes(period, encoding = "utf8"))

    def cta_step(self, id:int) -> bool:
        '''
        单步执行
        @id         策略id
        '''
        return self.api.cta_step(id)

    def cta_set_chart_kline(self, id:int, stdCode:str, period:str):
        '''
        设置图表K线
        @stdCode    合约代码
        @period     K线周期
        '''
        self.api.cta_set_chart_kline(id, bytes(stdCode, encoding = "utf8"), bytes(period, encoding = "utf8"))

    def cta_add_chart_mark(self, id:int, price:float, icon:str, tag:str = 'Notag'):
        '''
        添加图表标记
        @price  价格, 决定图标出现的位置
        @icon   图标, 系统一定的图标ID
        @tag    标签, 自定义的
        '''
        self.api.cta_add_chart_mark(id, price, bytes(icon, encoding = "utf8"), bytes(tag, encoding = "utf8"))

    def cta_register_index(self, id:int, idxName:str, idxType:int = 1):
        '''
        注册指标, on_init调用
        @idxName    指标名
        @idxType    指标类型, 0-主图指标, 1-副图指标
        '''
        self.api.cta_register_index(id, bytes(idxName, encoding = "utf8"), idxType)

    def cta_register_index_line(self, id:int, idxName:str, lineName:str, lineType:int = 0) -> bool:
        '''
        注册指标线, on_init调用
        @idxName    指标名称
        @lineName   线名称
        @lineType   线型, 0-曲线, 1-柱子
        '''
        return self.api.cta_register_index_line(id, bytes(idxName, encoding = "utf8"), bytes(lineName, encoding = "utf8"), lineType)

    def cta_add_index_baseline(self, id:int, idxName:str, lineName:str, value:float) -> bool:
        '''
        添加基准线, on_init调用
        @idxName    指标名称
        @lineName   线名称
        @value      数值
        '''
        return self.api.cta_add_index_baseline(id, bytes(idxName, encoding = "utf8"), bytes(lineName, encoding = "utf8"), value)

    def cta_set_index_value(self, id:int, idxName:str, lineName:str, val:float) -> bool:
        '''
        设置指标值, 只有在oncalc的时候才生效
        @idxName    指标名称
        @lineName   线名称
        '''
        return self.api.cta_set_index_value(id, bytes(idxName, encoding = "utf8"), bytes(lineName, encoding = "utf8"), val)

    
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''SEL接口'''    
    def sel_get_bars(self, id:int, stdCode:str, period:str, count:int):
        '''
        读取K线
        @id     策略id
        @stdCode   合约代码
        @period 周期, 如m1/m3/d1等
        @count  条数
        '''
        return self.api.sel_get_bars(id, bytes(stdCode, encoding = "utf8"), bytes(period, encoding = "utf8"), count, CB_STRATEGY_GET_BAR(self.on_stra_get_bar))
    
    def sel_get_ticks(self, id:int, stdCode:str, count:int):
        '''
        读取Tick
        @id     策略id
        @stdCode   合约代码
        @count  条数
        '''
        return self.api.sel_get_ticks(id, bytes(stdCode, encoding = "utf8"), count, CB_STRATEGY_GET_TICK(self.on_stra_get_tick))

    def sel_save_user_data(self, id:int, key:str, val:str):
        '''
        保存用户数据
        @id         策略id
        @key        数据名
        @val        数据值
        '''
        self.api.sel_save_userdata(id, bytes(key, encoding = "utf8"), bytes(val, encoding = "utf8"))

    def sel_load_user_data(self, id:int, key:str, defVal:str  = ""):
        '''
        加载用户数据
        @id         策略id
        @key        数据名
        @defVal     默认值
        '''
        ret = self.api.sel_load_userdata(id, bytes(key, encoding = "utf8"), bytes(defVal, encoding = "utf8"))
        return bytes.decode(ret)

    def sel_get_all_position(self, id:int):
        '''
        获取全部持仓
        @id     策略id
        '''
        return self.api.sel_get_all_position(id, CB_STRATEGY_GET_POSITION(self.on_stra_get_position))

    def sel_get_position(self, id:int, stdCode:str, bonlyvalid:bool = False, usertag:str = ""):
        '''
        获取持仓
        @id     策略id
        @stdCode   合约代码
        @usertag    进场标记, 如果为空则获取该合约全部持仓
        @return 指定合约的持仓手数, 正为多, 负为空
        '''
        return self.api.sel_get_position(id, bytes(stdCode, encoding = "utf8"), bonlyvalid, bytes(usertag, encoding = "utf8"))

    def sel_get_price(self, stdCode:str):
        '''
        @stdCode   合约代码
        @return 指定合约的最新价格 
        '''
        return self.api.sel_get_price(bytes(stdCode, encoding = "utf8"))

    def sel_set_position(self, id:int, stdCode:str, qty:float, usertag:str = ""):
        '''
        设置目标仓位
        @id     策略id
        @stdCode   合约代码
        @qty    目标仓位, 正为多, 负为空
        '''
        self.api.sel_set_position(id, bytes(stdCode, encoding = "utf8"), qty, bytes(usertag, encoding = "utf8"))
    
    def sel_get_tdate(self) -> int:
        '''
        获取当前交易日
        @return    当前交易日
        '''
        return self.api.sel_get_tdate()
    
    def sel_get_date(self):
        '''
        获取当前日期
        @return    当前日期 
        '''
        return self.api.sel_get_date()

    def sel_get_time(self):
        '''
        获取当前时间
        @return    当前时间 
        '''
        return self.api.sel_get_time()

    def sel_log_text(self, id:int, level:int, message:str):
        '''
        日志输出
        @id         策略ID
        @level      日志级别
        @message    日志内容
        '''
        self.api.sel_log_text(id, level, ph.auto_encode(message))

    def sel_sub_ticks(self, id:int, stdCode:str):
        '''
        订阅行情
        @id         策略id
        @stdCode    品种代码
        '''
        self.api.sel_sub_ticks(id, bytes(stdCode, encoding = "utf8"))

    def sel_get_day_price(self, stdCode:str, flag:int = 0) -> float:
        '''
        获取当日价格
        @stdCode    合约代码
        @flag       价格标记, 0-开盘价, 1-最高价, 2-最低价, 3-最新价
        @return     指定合约的价格 
        '''
        return self.api.sel_get_day_price(bytes(stdCode, encoding = "utf8"), flag)

    def sel_get_fund_data(self, id:int, flag:int) -> float:
        '''
        获取资金数据
        @id     策略id
        @flag   0-动态权益, 1-总平仓盈亏, 2-总浮动盈亏, 3-总手续费
        @return 资金数据
        '''
        return self.api.sel_get_fund_data(id, flag)

    def sel_get_position_profit(self, id:int, stdCode:str):
        '''
        获取浮动盈亏
        @id         策略id
        @stdCode    合约代码
        @return     指定合约的浮动盈亏
        '''
        return self.api.sel_get_position_profit(id, bytes(stdCode, encoding = "utf8"))

    def sel_get_position_avgpx(self, id:int, stdCode:str):
        '''
        获取持仓均价
        @id         策略id
        @stdCode    合约代码
        @return     指定合约的持仓均价
        '''
        return self.api.sel_get_position_avgpx(id, bytes(stdCode, encoding = "utf8"))

    def sel_get_first_entertime(self, id:int, stdCode:str) -> int:
        '''
        获取当前持仓的首次进场时间
        @stdCode    合约代码
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.sel_get_first_entertime(id, bytes(stdCode, encoding = "utf8"))

    def sel_get_last_entertime(self, id:int, stdCode:str) -> int:
        '''
        获取当前持仓的最后进场时间
        @stdCode    合约代码
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.sel_get_last_entertime(id, bytes(stdCode, encoding = "utf8"))

    def sel_get_last_entertag(self, id:int, stdCode:str) -> str:
        '''
        获取当前持仓的最后进场标记
        @stdCode    合约代码
        @return     进场标记 
        '''
        return bytes.decode(self.api.sel_get_last_entertag(id, bytes(stdCode, encoding = "utf8")))

    def sel_get_last_exittime(self, id:int, stdCode:str) -> int:
        '''
        获取当前持仓的最后出场时间
        @stdCode    合约代码
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.sel_get_last_exittime(id, bytes(stdCode, encoding = "utf8"))

    def sel_get_detail_entertime(self, id:int, stdCode:str, usertag:str) -> int:
        '''
        获取指定标记的持仓的进场时间
        @id         策略id
        @stdCode    合约代码
        @usertag    进场标记
        @return     进场时间, 格式如201907260932 
        '''
        return self.api.sel_get_detail_entertime(id, bytes(stdCode, encoding = "utf8"), bytes(usertag, encoding = "utf8")) 

    def sel_get_detail_cost(self, id:int, stdCode:str, usertag:str) -> float:
        '''
        获取指定标记的持仓的开仓价
        @id         策略id
        @stdCode    合约代码
        @usertag    进场标记
        @return     开仓价 
        '''
        return self.api.sel_get_detail_cost(id, bytes(stdCode, encoding = "utf8"), bytes(usertag, encoding = "utf8")) 

    def sel_get_detail_profit(self, id:int, stdCode:str, usertag:str, flag:int):
        '''
        获取指定标记的持仓的盈亏
        @id         策略id
        @stdCode       合约代码
        @usertag    进场标记
        @flag       盈亏记号, 0-浮动盈亏, 1-最大浮盈, -1-最大亏损（负数）, 2-最大浮盈价格， -2-最大浮亏价格
        @return     盈亏 
        '''
        return self.api.sel_get_detail_profit(id, bytes(stdCode, encoding = "utf8"), bytes(usertag, encoding = "utf8"), flag) 


    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''HFT接口'''    
    def hft_get_bars(self, id:int, stdCode:str, period:str, count:int):
        '''
        读取K线
        @id     策略id
        @stdCode   合约代码
        @period 周期, 如m1/m3/d1等
        @count  条数
        '''
        return self.api.hft_get_bars(id, bytes(stdCode, encoding = "utf8"), bytes(period, encoding = "utf8"), count, CB_STRATEGY_GET_BAR(self.on_stra_get_bar))
    
    def hft_get_ticks(self, id:int, stdCode:str, count:int):
        '''
        读取Tick
        @id     策略id
        @stdCode   合约代码
        @count  条数
        '''
        return self.api.hft_get_ticks(id, bytes(stdCode, encoding = "utf8"), count, CB_STRATEGY_GET_TICK(self.on_stra_get_tick))

    def hft_get_ordque(self, id:int, stdCode:str, count:int):
        '''
        读取委托队列
        @id        策略id
        @stdCode   合约代码
        @count     条数
        '''
        return self.api.hft_get_ordque(id, bytes(stdCode, encoding = "utf8"), count, CB_HFTSTRA_GET_ORDQUE(self.on_hftstra_get_order_queue))

    def hft_get_orddtl(self, id:int, stdCode:str, count:int):
        '''
        读取逐笔委托
        @id        策略id
        @stdCode   合约代码
        @count     条数
        '''
        return self.api.hft_get_orddtl(id, bytes(stdCode, encoding = "utf8"), count, CB_HFTSTRA_GET_ORDDTL(self.on_hftstra_get_order_detail))

    def hft_get_trans(self, id:int, stdCode:str, count:int):
        '''
        读取逐笔成交
        @id        策略id
        @stdCode   合约代码
        @count     条数
        '''
        return self.api.hft_get_trans(id, bytes(stdCode, encoding = "utf8"), count, CB_HFTSTRA_GET_TRANS(self.on_hftstra_get_transaction))

    def hft_save_user_data(self, id:int, key:str, val:str):
        '''
        保存用户数据
        @id         策略id
        @key        数据名
        @val        数据值
        '''
        self.api.hft_save_userdata(id, bytes(key, encoding = "utf8"), bytes(val, encoding = "utf8"))

    def hft_load_user_data(self, id:int, key:str, defVal:str  = ""):
        '''
        加载用户数据
        @id         策略id
        @key        数据名
        @defVal     默认值
        '''
        ret = self.api.hft_load_userdata(id, bytes(key, encoding = "utf8"), bytes(defVal, encoding = "utf8"))
        return bytes.decode(ret)

    def hft_get_position(self, id:int, stdCode:str, bonlyvalid:bool = False):
        '''
        获取持仓
        @id     策略id
        @stdCode   合约代码
        @return 指定合约的持仓手数, 正为多, 负为空
        '''
        return self.api.hft_get_position(id, bytes(stdCode, encoding = "utf8"), bonlyvalid)

    def hft_get_position_profit(self, id:int, stdCode:str):
        '''
        获取持仓盈亏
        @id     策略id
        @stdCode   合约代码
        @return 指定持仓的浮动盈亏
        '''
        return self.api.hft_get_position_profit(id, bytes(stdCode, encoding = "utf8"))

    def hft_get_position_avgpx(self, id:int, stdCode:str):
        '''
        获取持仓均价
        @id     策略id
        @stdCode   合约代码
        @return 指定持仓的浮动盈亏
        '''
        return self.api.hft_get_position_avgpx(id, bytes(stdCode, encoding = "utf8"))

    def hft_get_undone(self, id:int, stdCode:str):
        '''
        获取持仓
        @id     策略id
        @stdCode   合约代码
        @return 指定合约的持仓手数, 正为多, 负为空
        '''
        return self.api.hft_get_undone(id, bytes(stdCode, encoding = "utf8"))

    def hft_get_price(self, stdCode:str):
        '''
        @stdCode   合约代码
        @return 指定合约的最新价格 
        '''
        return self.api.hft_get_price(bytes(stdCode, encoding = "utf8"))

    def hft_get_date(self):
        '''
        获取当前日期
        @return    当前日期 
        '''
        return self.api.hft_get_date()

    def hft_get_time(self):
        '''
        获取当前时间
        @return    当前时间 
        '''
        return self.api.hft_get_time()

    def hft_get_secs(self):
        '''
        获取当前时间
        @return    当前时间 
        '''
        return self.api.hft_get_secs()

    def hft_log_text(self, id:int, level:int, message:str):
        '''
        日志输出
        @id         策略ID
        @level      日志级别
        @message    日志内容
        '''
        self.api.hft_log_text(id, level, ph.auto_encode(message))

    def hft_sub_ticks(self, id:int, stdCode:str):
        '''
        订阅实时行情数据
        @id         策略ID
        @stdCode    品种代码
        '''
        self.api.hft_sub_ticks(id, bytes(stdCode, encoding = "utf8"))

    def hft_sub_order_queue(self, id:int, stdCode:str):
        '''
        订阅实时委托队列数据
        @id         策略ID
        @stdCode    品种代码
        '''
        self.api.hft_sub_order_queue(id, bytes(stdCode, encoding = "utf8"))

    def hft_sub_order_detail(self, id:int, stdCode:str):
        '''
        订阅逐笔委托数据
        @id         策略ID
        @stdCode    品种代码
        '''
        self.api.hft_sub_order_detail(id, bytes(stdCode, encoding = "utf8"))

    def hft_sub_transaction(self, id:int, stdCode:str):
        '''
        订阅逐笔成交数据
        @id         策略ID
        @stdCode    品种代码
        '''
        self.api.hft_sub_transaction(id, bytes(stdCode, encoding = "utf8"))

    def hft_cancel(self, id:int, localid:int):
        '''
        撤销指定订单
        @id         策略ID
        @localid    下单时返回的本地订单号
        '''
        return self.api.hft_cancel(id, localid)

    def hft_cancel_all(self, id:int, stdCode:str, isBuy:bool):
        '''
        撤销指定品种的全部买入订单or卖出订单
        @id         策略ID
        @stdCode    品种代码
        @isBuy      买入or卖出
        '''
        ret = self.api.hft_cancel_all(id, bytes(stdCode, encoding = "utf8"), isBuy)
        return bytes.decode(ret)

    def hft_buy(self, id:int, stdCode:str, price:float, qty:float, userTag:str, flag:int):
        '''
        买入指令
        @id         策略ID
        @stdCode    品种代码
        @price      买入价格, 0为市价
        @qty        买入数量
        '''
        ret = self.api.hft_buy(id, bytes(stdCode, encoding = "utf8"), price, qty, bytes(userTag, encoding = "utf8"), flag)
        return bytes.decode(ret)

    def hft_sell(self, id:int, stdCode:str, price:float, qty:float, userTag:str, flag:int):
        '''
        卖出指令
        @id         策略ID
        @stdCode    品种代码
        @price      卖出价格, 0为市价
        @qty        卖出数量
        '''
        ret = self.api.hft_sell(id, bytes(stdCode, encoding = "utf8"), price, qty, bytes(userTag, encoding = "utf8"), flag)
        return bytes.decode(ret)

    def hft_step(self, id:int):
        '''
        单步执行
        @id         策略id
        '''
        self.api.hft_step(id)


    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''本地撮合接口'''
    def init_cta_mocker(self, name:str, slippage:int = 0, hook:bool = False, persistData:bool = True, incremental:bool = False, isRatioSlp:bool = False) -> int:
        '''
        创建策略环境
        @name       策略名称 
        @slippage   滑点大小
        @hook       是否安装钩子，主要用于单步控制重算
        @persistData    回测生成的数据是否落地, 默认为True
        @incremental    是否增量回测, 默认为False
        @isRatioSlp     滑点是否是比例, 默认为False, 如果为True, 则slippage为万分比
        @return    系统内策略ID
        '''
        return self.api.init_cta_mocker(bytes(name, encoding = "utf8"), slippage, hook, persistData, incremental, isRatioSlp)

    def init_hft_mocker(self, name:str, hook:bool = False) -> int:
        '''
        创建策略环境
        @name      策略名称
        @return    系统内策略ID 
        '''
        return self.api.init_hft_mocker(bytes(name, encoding = "utf8"), hook)

    def init_sel_mocker(self, name:str, date:int, time:int, period:str, trdtpl:str = "CHINA", session:str = "TRADING", slippage:int = 0, isRatioSlp:bool = False) -> int:
        '''
        创建策略环境
        @name      策略名称
        @return    系统内策略ID 
        '''
        return self.api.init_sel_mocker(bytes(name, encoding = "utf8"), date, time, 
            bytes(period, encoding = "utf8"), bytes(trdtpl, encoding = "utf8"), bytes(session, encoding = "utf8"), slippage, isRatioSlp)
