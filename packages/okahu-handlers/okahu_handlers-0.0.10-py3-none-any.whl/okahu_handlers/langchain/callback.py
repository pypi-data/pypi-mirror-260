import json
import logging
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID

import requests
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.outputs import LLMResult

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.document import Document

logger = logging.getLogger(__name__)


def to_json(obj):
    return json.dumps(obj, indent=4, default=lambda obj: obj.__dict__)


@dataclass
class Context:
    trace_id: str
    span_id: str

    @staticmethod
    def from_dict(obj: Any) -> "Context":
        _trace_id = str(obj.get("trace_id"))
        _span_id = str(obj.get("span_id"))
        return Context(_trace_id, _span_id)


@dataclass
class Event:
    name: str
    timestamp: str
    attributes: dict[str, Any]

    @staticmethod
    def from_dict(obj: Any) -> "Event":
        _name = str(obj.get("name"))
        _timestamp = str(obj.get("timestamp"))
        _attributes = obj.get("attributes")
        return Event(_name, _timestamp, _attributes)


@dataclass
class Root:
    name: str
    context: Context
    parent_id: str
    start_time: str
    end_time: str
    attributes: dict[str, Any]
    events: List[Event]

    @staticmethod
    def from_dict(obj: Any) -> "Root":
        _name = str(obj.get("name"))
        _context = Context.from_dict(obj.get("context"))
        _parent_id = str(obj.get("parent_id"))
        _start_time = str(obj.get("start_time"))
        _end_time = str(obj.get("end_time"))
        _attributes = obj.get("attributes")
        _events = [Event.from_dict(y) for y in obj.get("events")]
        return Root(
            _name, _context, _parent_id, _start_time, _end_time, _attributes, _events
        )


# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)


class OkahuCallbackHandler(BaseCallbackHandler):
    """Callback Handler that sends traces to Okahu."""

    def start_decorator(func):
        def wrapper( self,
        *args,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
            if func.__name__.endswith("_start"):
                """A wrapper function"""
                self.__populateIndices(run_id, parent_run_id)
                func(self,*args,run_id=run_id,parent_run_id=parent_run_id,**kwargs)
        return wrapper
    
    def end_decorator(func):
        def wrapper( self,
        *args,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
            if func.__name__.endswith("_end") or func.__name__.endswith("_error"):
                """A wrapper function"""
                try:
                    func(self,*args,run_id=run_id,parent_run_id=parent_run_id,**kwargs)
                finally:
                    self.__cleanIndices(run_id)
        return wrapper

    def __init__(
        self,
        app_name: str,
        mode: str = "a",
        color: Optional[str] = None,
    ) -> None:
        """Initialize callback handler."""
        self.color = color
        self.runs = dict[str, Root]() 
        '''traceIndex consists of map of trace_id1 ->[span_id1, span_id2 ]'''
        self.traceIndex = dict[UUID, set[UUID]]()
        '''invertedTraceIndex consists of {span_id1 -> trace_id1, span_id2 -> trace_id1} '''
        self.invertedTraceIndex = dict[UUID, UUID]() 
        self.app_name = app_name


    def __populateIndices(self, run_id, parent_run_id: Optional[UUID] = None):
        if run_id is not None:
            if (parent_run_id is None) or (parent_run_id == run_id):
                    """this is trace_id"""
                    self.invertedTraceIndex[run_id]= run_id
                    if run_id not in self.traceIndex:
                        self.traceIndex[run_id]= set()
            else:
                if parent_run_id in self.invertedTraceIndex:
                    parent_trace_id = self.invertedTraceIndex[parent_run_id]
                    if parent_trace_id in self.traceIndex:
                        self.traceIndex[parent_trace_id].add(run_id)
                    self.invertedTraceIndex[run_id]= parent_trace_id


    def __cleanIndices(self, run_id):
        if run_id is not None:
            self.traceIndex.pop(run_id, None)
            if run_id in self.traceIndex:
                set_of_ids = self.traceIndex[run_id]
                for val in set_of_ids:
                    self.invertedTraceIndex.pop(val, None)

    def __getTraceId(self, run_id):
            if (run_id is not None) and (run_id in self.invertedTraceIndex):
                fetched_trace_id = self.invertedTraceIndex[run_id]
                return str(fetched_trace_id)
            else:
                return None

    @start_decorator
    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        
        trace_id = self.__getTraceId(run_id)
    
        """Print out that we are entering a retriever."""
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        curr_time = get_date_time_current()
        context = Context(trace_id=trace_id, span_id=str(run_id))
        curr_span = Root(
            name=class_name,
            context=context,
            attributes=None,
            end_time="",
            start_time="",
            events="",
            parent_id=str(parent_run_id),
        )
        curr_span.start_time = curr_time
        curr_span.parent_id = str(parent_run_id)
        self.runs[str(run_id)] = curr_span

    @end_decorator
    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        self.runs[str(run_id)].end_time = get_date_time_current()
        dict_text = to_json(self.runs[str(run_id)])
        print_text_wrapper(dict_text)

    @end_decorator
    def on_retriever_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        curr_span = self.runs[str(run_id)]
        curr_span.end_time = get_date_time_current()
        attributes = dict[str, str]()
        attributes["errormessage"] = str(error)
        add_event(
            root=curr_span,
            attributes=attributes,
            eventName="error",
            timestamp=curr_span.end_time,
        )
        add_attribute(root=curr_span, key="status", value="error")
        dict_text = to_json(curr_span)
        print_text_wrapper(dict_text)

    @start_decorator
    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Print out that we are entering a chain."""
        trace_id = self.__getTraceId(run_id)

        print_text_wrapper("triggered on_chain_start")
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        curr_time = get_date_time_current()
        # dict_text = json.dumps(serialized, indent=4)
        context = Context(trace_id=trace_id, span_id=str(run_id))
        curr_span = Root(
            name=class_name,
            context=context,
            attributes=None,
            end_time="",
            start_time="",
            events="",
            parent_id=str(parent_run_id),
        )
        curr_span.start_time = curr_time
        curr_span.parent_id = str(parent_run_id)
        if parent_run_id is None:
            add_attribute(root=curr_span, key="input", value=inputs)
            add_attribute(root=curr_span, key="app_name", value=self.app_name)
        self.runs[str(run_id)] = curr_span

    @end_decorator
    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Print out that we finished a chain."""
        curr_span = self.runs[str(run_id)]
        curr_span.end_time = get_date_time_current()

        if parent_run_id is None:
            add_attribute(root=curr_span, key="output", value=outputs)
        dict_text = to_json(curr_span)
        print_text_wrapper(dict_text)

        if parent_run_id is None:
            self.send_okahu_traces()
        

    @end_decorator
    def on_chain_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        curr_span = self.runs[str(run_id)]
        curr_span.end_time = get_date_time_current()
        attributes = dict[str, str]()
        attributes["errormessage"] = str(error)
        add_event(
            root=curr_span,
            attributes=attributes,
            eventName="error",
            timestamp=curr_span.end_time,
        )
        add_attribute(root=curr_span, key="status", value="error")
        dict_text = to_json(curr_span)
        print_text_wrapper(dict_text)
        if parent_run_id is None:
            self.send_okahu_traces()


    def send_okahu_traces(self):
        try:
            api_key: str = os.environ["OKAHU_API_KEY"]
            okahu_endpoint: str = os.environ["OKAHU_INGESTION_ENDPOINT"]
            response = requests.post(
                okahu_endpoint,
                data=to_json({"batch": list(self.runs.values())}),
                # json={"batch": list(self.runs.values())},
                headers={"Content-Type": "application/json", "x-functions-key": api_key},
            )
            print_text_wrapper(f"okahu ingestion response code:{str(response.status_code)}")
            print_text_wrapper(f"okahu ingestion response content:{str(response.content)}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Ingestion to Okahu endpoint unsuccessful:{e.response.text}")
        finally:
            '''The following cleans up the runs'''
            self.runs.clear()   

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        print_text_wrapper(action.log)

    @start_decorator
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: uuid,
        parent_run_id: Optional[uuid.UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        
        trace_id = self.__getTraceId(run_id)
    
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        curr_time = get_date_time_current()
        # dict_text = json.dumps(serialized, indent=4)
        context = Context(trace_id=trace_id, span_id=str(run_id))
        curr_span = Root(
            name=class_name,
            context=context,
            attributes=None,
            end_time="",
            start_time="",
            events="",
            parent_id=str(parent_run_id),
        )
        self.update_llm_endpoint(curr_span)
        curr_span.start_time = curr_time
        curr_span.parent_id = str(parent_run_id)
        self.runs[str(run_id)] = curr_span

    def update_llm_endpoint(self, curr_span: Root):
        triton_llm_endpoint = os.environ.get("TRITON_LLM_ENDPOINT")
        if triton_llm_endpoint is not None and len(triton_llm_endpoint) > 0:
            curr_span.attributes = curr_span.attributes or dict[str, str]()
            curr_span.attributes["server_url"] = triton_llm_endpoint

    @end_decorator
    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self.runs[str(run_id)].end_time = get_date_time_current()
        dict_text = to_json(self.runs[str(run_id)])
        print_text_wrapper(dict_text)

    @end_decorator
    def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        curr_span = self.runs[str(run_id)]
        curr_span.end_time = get_date_time_current()
        attributes = dict[str, str]()
        attributes["errormessage"] = str(error)
        add_event(
            root=curr_span,
            attributes=attributes,
            eventName="error",
            timestamp=curr_span.end_time,
        )
        add_attribute(root=curr_span, key="status", value="error")
        dict_text = to_json(curr_span)
        print_text_wrapper(dict_text)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            print_text_wrapper(f"{observation_prefix}")
        print_text_wrapper(output)
        if llm_prefix is not None:
            print_text_wrapper(f"{llm_prefix}")

    def on_text(
        self, text: str, color: Optional[str] = None, end: str = "", **kwargs: Any
    ) -> None:
        """Run when agent ends."""
        print_text_wrapper(text)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        print_text_wrapper(finish.log)


def add_event(
    root: Root, eventName: str, timestamp: str, attributes: dict[str, str]
) -> None:
    if root.events is None or root.events == "":
        root.events = []
    root.events.append(
        Event(name=eventName, timestamp=timestamp, attributes=attributes)
    )


def add_attribute(root: Root, key: str, value: str) -> None:
    if root.attributes is None or root.attributes == "":
        root.attributes = dict[str, str]()
    root.attributes[key] = value


def get_date_time_current() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def print_text_wrapper(text: str) -> None:
    logger.info(text)
