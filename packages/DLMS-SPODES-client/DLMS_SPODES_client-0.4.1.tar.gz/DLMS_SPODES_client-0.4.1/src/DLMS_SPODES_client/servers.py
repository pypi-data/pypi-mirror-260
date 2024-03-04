from threading import Thread
from functools import cached_property
import asyncio
from .client import Client, Errors
from . import task
from DLMS_SPODES.enums import Transmit, Application
from DLMS_SPODES import exceptions as exc
from .enums import LogLevel as logL


class Result:
    client: Client
    complete: bool
    errors: Errors

    def __init__(self, client: Client):
        self.client = client
        self.complete = False
        """complete exchange"""
        self.errors = Errors()


class Results:
    __values: tuple[Result, ...]
    name: str

    def __init__(self, clients: tuple[Client],
                 name: str = None):
        self.__values = tuple(Result(c) for c in clients)
        self.name = name
        """common operation name"""

    def __iter__(self):
        return iter(self.__values)

    @cached_property
    def clients(self) -> set[Client]:
        return {res.client for res in self.__values}

    @cached_property
    def ok_results(self) -> set[Result]:
        """without errors exchange clients"""
        ret = set()
        for res in self.__values:
            if all(map(lambda err_code: err_code.is_ok(), res.errors)):
                ret.add(res)
        return ret

    @cached_property
    def nok_results(self) -> set[Result]:
        """ With errors exchange clients """
        return set(self.__values).difference(self.ok_results)

    def is_complete(self) -> bool:
        return all((res.complete for res in self))


class TransactionServer:
    __t: Thread
    results: Results

    def __init__(self,
                 clients: list[Client] | tuple[Client],
                 tsk: task.ExTask,
                 name: str = None):
        self.results = Results(clients, name)
        self.task = tsk
        self._tg = None
        self.__t = Thread(
            target=self.start_coro,
            args=(self.results,))

    def start(self):
        self.__t.start()

    def start_coro(self, results):
        asyncio.run(self.coro_loop(results))

    async def coro_loop(self, results: Results):
        async with asyncio.TaskGroup() as self._tg:
            for res in results:
                self._tg.create_task(
                    coro=session(
                        c=res.client,
                        t=self.task,
                        result=res))


async def session(c: Client,
                  t: task.ExTask,
                  result: Result,
                  is_public: bool = False):
    try:
        await c.connect(is_public)
        await t.exchange(c)
    except TimeoutError as e:
        c.set_error(Transmit.TIMEOUT, 'Таймаут при обмене')
    except exc.DLMSException as e:
        c.set_error(e.error, e.args[0])
    except ConnectionError as e:
        c.set_error(Transmit.NO_TRANSPORT, F"При соединении{e}")
    except Exception as e:
        c.log(logL.INFO, F'UNKNOWN ERROR: {e}...')
        c.set_error(Transmit.UNKNOWN, F'При обмене{e}')
    finally:
        result.complete = True
        result.errors = c.errors
        match c.errors:
            case {Transmit.OK: _} if len(c.errors) == 1:
                await c.close()
                # await self.start_disconnect()
            case {Transmit.NO_TRANSPORT: _} | {Transmit.NO_PORT: _}:
                """ nothing need do. Port not open ... etc """
            case {Application.MISSING_OBJ: _}:
                await c.close()
                # await self.start_disconnect()
            case {Transmit.TIMEOUT: _} | {Transmit.ABORT: _}:
                await c.force_disconnect()
            case {Transmit.NO_ACCESS: _} | {Application.ID_ERROR: _} | {Application.VERSION_ERROR: _}:
                await c.close()
            case _:
                await c.force_disconnect()
        return result
