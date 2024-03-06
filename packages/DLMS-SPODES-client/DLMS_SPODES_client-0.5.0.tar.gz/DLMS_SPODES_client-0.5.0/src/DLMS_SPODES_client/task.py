from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import time
import datetime
from DLMS_SPODES.types.implementations import enums, long_unsigneds, bitstrings, octet_string, structs
from DLMS_SPODES import exceptions as exc
from DLMS_SPODES.cosem_interface_classes import collection, overview
from DLMS_SPODES.types import cdt, ut
from DLMS_SPODES.enums import Transmit, Application
from .client import Client, pdu, logL, AppVersion, RelationGroup


class ExTask(ABC):
    """Exchange task for DLMS client"""
    @abstractmethod
    async def exchange(self, c: Client):
        """common exchange in session"""


class Sequence(ExTask):
    """for exchange task sequence"""
    tasks: list[ExTask]
    __is_exchange: bool

    def __init__(self, *tasks: ExTask):
        assert all((isinstance(t, ExTask) for t in tasks))
        self.tasks = list(tasks)
        self.__is_exchange = False

    def append(self, task: ExTask):
        if not self.__is_exchange:
            self.tasks.append(task)
        else:
            raise RuntimeError(F"append to {self.__class__.__name__} not allowed, already exchange started")

    async def exchange(self, c: Client):
        self.__is_exchange = True
        for t in self.tasks:
            await t.exchange(c)


class InitType(ExTask):
    """nothing params"""
    async def exchange(self, c: Client):
        # read LDN
        ldn = octet_string.LDN(await c.read_attr(collection.AttrDesc.LDN_VALUE))
        # find device_id(type for Russia)
        type_value, _ = cdt.get_instance_and_pdu_from_value(await c.read_attr(ut.CosemAttributeDescriptor((1, "0.0.96.1.1.255", 2))))
        # find version data
        for desc in (ut.CosemAttributeDescriptor((1, "0.0.0.2.1.255", 2)), ut.CosemAttributeDescriptor((1, "0.0.96.1.2.255", 2))):
            try:
                ver_value, _ = cdt.get_instance_and_pdu_from_value(await c.read_attr(desc))
                break
            except exc.ResultError as e:
                if e.result == pdu.DataAccessResult.OBJECT_UNDEFINED:
                    """try search in old object and set to new"""
                    continue
                else:
                    raise e
            except exc.NeedUpdate as e:
                c.log(logL.WARN, F"{e}. I do it...")
                break
        else:
            raise exc.NoObject(F"not find version object in server")
        try:
            c.objects = collection.get_collection(
                manufacturer=ldn.manufacturer(),
                server_type=type_value,
                server_ver=AppVersion.from_str(ver_value.to_str()))
            c.objects.LDN.set_attr(2, ldn)
        except exc.NoConfig as e:
            c.log(logL.WARN, F"false init type procedure: {e}, start create objects from device")
            new_collection = collection.Collection(ldn=ldn)
            # read association
            object_list: cdt.Array = cdt.Array(await c.read_attr(collection.AttrDesc.OBJECT_LIST), type_=structs.ObjectListElement)
            for c_id, ver, ln, _ in object_list:
                new_obj = new_collection.add_if_missing(
                    class_id=ut.CosemClassId(int(c_id)),
                    version=ver,
                    logical_name=ln)
                if new_obj.CLASS_ID == overview.ClassID.ASSOCIATION_LN:  # search association for keep object_list into
                    await c.read_attr(new_obj.get_attr_descriptor(3))
                    if new_obj.associated_partners_id.client_SAP == c.SAP:
                        new_obj.set_attr(2, object_list)
            new_collection.get_class_version()
            c.objects = new_collection
            # read all DeviceIDObjects
            for d_id in collection.group_filter(new_collection, (RelationGroup.DEVICE_ID_OBJECTS, RelationGroup.OTHER_ABSTRACT_GENERAL_PURPOSE_OBIS_CODES)):
                await c.read_attribute(d_id, 2)

            # TODO: handle 6.2.42 DLMS UA 1000-1 Ed. 14 - Device ID objects, 6.2.4 Other abstract general purpose OBIS codes(Program entries for version)
            # TODO: keep in Types
        c.log(logL.INFO, F"added {len(c.objects)} DLMS objects")


@dataclass
class ReadAttribute(ExTask):
    ln: collection.LNContaining
    index: int

    async def exchange(self, c: Client):
        # TODO: check is_readable
        obj = c.objects.get_object(self.ln)
        data = await self.read_from_obj(c, obj, self.index)

    @staticmethod
    async def read_from_obj(c: Client, obj: collection.InterfaceClass, index: int):
        c.get_get_request_normal(
            attr_desc=obj.get_attr_descriptor(
                value=index,
                with_selection=bool(c.negotiated_conformance.selective_access)))
        start_read_time: float = time.perf_counter()
        reply = await c.read_data_block()
        c.last_transfer_time = datetime.timedelta(seconds=time.perf_counter()-start_read_time)
        obj.set_attr(index, reply.data.get_data())


@dataclass
class ReadEmptyAttribute(ExTask):
    """read if attribute is empty"""
    ln: collection.LNContaining
    index: int

    async def exchange(self, c: Client):
        # TODO: check is_readable
        if c.objects.get_object(self.ln).get_attr(self.index) is None:
            data = await ReadAttribute(
                ln=self.ln,
                index=self.index).exchange(c)


@dataclass
class ReadAttributes(ExTask):
    ln: collection.LNContaining
    indexes: tuple[int, ...]

    async def exchange(self, c: Client):
        obj = c.objects.get_object(self.ln)
        # TODO: check for Get-Request-With-List
        for i in self.indexes:
            await ReadAttribute.read_from_obj(c, obj, i)


@dataclass
class WriteAttribute(ExTask):
    ln: collection.LNContaining
    index: int
    value: bytes | str | int | list | tuple | datetime.datetime

    async def exchange(self, c: Client):
        if c.objects.is_writable(
                ln=(obj := c.objects.get_object(self.ln)).logical_name,
                index=self.index,
                association_id=c.objects.get_association_id(c.SAP)):
            if isinstance(self.value, (str, int, list, tuple, datetime.datetime)):
                value2 = await c.encode(
                    obj=obj,
                    index=self.index,
                    value=self.value)
                enc = value2.encoding
            else:
                enc = self.value
            data = c.get_set_request_normal(
                obj=obj,
                attr_index=self.index,
                value=enc)
            await c.read_data_block()
        else:
            raise exc.ITEApplication(F"Access Error. From current association: {obj}: {self.index} is not writable")


@dataclass
class WriteAttributesOld(ExTask):
    """todo: use for write without value(from object) replace all to WriteAttribute in future."""
    ln: collection.LNContaining
    indexes: tuple[int, ...]

    async def exchange(self, c: Client):
        for i in self.indexes:
            if c.objects.is_writable(
                    ln=(obj := c.objects.get_object(self.ln)).logical_name,
                    index=i,
                    association_id=c.objects.get_association_id(c.SAP)):
                data = c.get_set_request_normal(
                    obj=obj,
                    attr_index=i)
                await c.read_data_block()
            else:
                raise exc.ITEApplication(F"Access Error. From current association: {obj}: {i} is not writable")


@dataclass
class ExecuteByDesc(ExTask):
    """execute method by method descriptor # TODO: rewrite this"""
    desc: ut.CosemMethodDescriptor

    async def exchange(self, c: Client):
        try:
            await c.execute_method(self.desc)
            c.set_error(Transmit.OK, F'Execute {self.desc}.')
        except Exception as e:
            c.log(logL.INFO, F'ERROR: Исполнение {self.desc}')
            c.set_error(Transmit.EXECUTE_ERROR, F'Исполнение {self.desc}')


@dataclass
class Execute(ExTask):
    """execute method by method descriptor # TODO: rewrite this with <value>"""
    ln: collection.LNContaining
    index: int
    value: str

    async def exchange(self, c: Client):
        obj = c.objects.get_object(self.ln)
        try:
            await c.execute_method(ut.CosemMethodDescriptor(
                (obj.CLASS_ID,
                 ut.CosemObjectInstanceId(obj.logical_name.contents),
                 ut.CosemObjectMethodId(self.index))
            ))
            c.set_error(Transmit.OK, F'Execute {self.ln}: {self.index}.')
        except Exception as e:
            c.log(logL.INFO, F'ERROR: Исполнение {self.ln}: {self.index}')
            c.set_error(Transmit.EXECUTE_ERROR, F'Исполнение {self.ln}: {self.index}')


class WriteTime(ExTask):
    """write Clock.time depend from transfer time"""

    async def exchange(self, c: Client):
        try:
            obj = c.objects.clock
            c.get_get_request_normal(obj.get_attr_descriptor(3))
            reply = await c.read_data_block()
            tz = obj.get_attr_element(3).DATA_TYPE(reply.data.get_data())
            await WriteAttribute(
                ln=obj.logical_name,
                index=2,
                value=(datetime.datetime.utcnow() + datetime.timedelta(minutes=tz.decode()) + c.last_transfer_time)
            ).exchange(c)
            # obj.set_attr(2, (cst.OctetStringDateTime(datetime.datetime.utcnow() + datetime.timedelta(minutes=obj.time_zone.decode()) + dev.last_transfer_time)))
            # dev.write_attr(obj, 2)
            # logger.info(F'Write attribute: 2 success')
            c.errors[Transmit.OK] = 'Запись времени'
        except Exception as e:
            # logger.info(F'ERROR: write Clock: attribute 2 {e}')
            c.errors[Transmit.WRITE_ERROR] = F"write time: {e}"
