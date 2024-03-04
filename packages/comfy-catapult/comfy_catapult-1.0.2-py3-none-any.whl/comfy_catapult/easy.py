import datetime
import uuid
from copy import deepcopy
from typing import Annotated, Any, Dict, Hashable, List, Literal

import pydash
from anyio import Path
from pydantic import BaseModel, Field

from comfy_catapult.catapult import ComfyCatapult
from comfy_catapult.comfy_config import RemoteComfyConfig
from comfy_catapult.comfy_schema import (APIHistoryEntry, APIWorkflow,
                                         APIWorkflowNodeInfo, APINodeID)
from comfy_catapult.comfy_utils import DownloadPreviewImage, GetNode
from comfy_catapult.remote_file_api_base import RemoteFileAPIBase

NodeIDorTitle = Annotated[str, Field(alias='id_or_title')]


class EasySet(BaseModel):
  """What value to set on the inputs of a node."""
  field_path: Hashable | List[Hashable]
  """A pydash path to the field to set.
  
  This operates on the Workflow API JSON, specifically, on a node's `inputs`
  field.
  
  Example: "images" will set the node's `inputs['images']` field.
  
  See https://pydash.readthedocs.io/en/latest/api.html#pydash.objects.set_ .
  """
  value: Any
  """The value to put at the `field_path`.
  
  Raw types (JSON-serializeable) only. Anything more complicated might fail.
  
  See APIWorkflowNodeInfo.inputs for the types of values that can be set.
  Obviously since one of them is a dict, field_path can set things a bit deeper.
  """


class EasyGet(BaseModel):
  """What values to get/download from the outputs of a node."""
  field_path: Hashable | List[Hashable]
  """A pydash path to the field to get/download.
  
  This operates on the /history JSON output (See APIHistoryEntry.outputs), specifically,
  a node's `outputs` field.
  
  Example: "images.0" will get the first image from the node's outputs.
  
  See https://pydash.readthedocs.io/en/latest/api.html#pydash.objects.get .
  """

  type: Literal['literal', 'file']
  """
  'literal' will get the value of the field and return it in the json.
  
  'file' will download the file.
  """
  to: Path | None = None
  """For type=='file', the path to download the file to."""


class EasyParams(BaseModel):
  set: Dict[NodeIDorTitle, List[EasySet]]
  get: Dict[NodeIDorTitle, List[EasyGet]]
  config: RemoteComfyConfig
  remote: RemoteFileAPIBase


async def Easy(*,
               catapult: ComfyCatapult,
               workflow_template: APIWorkflow,
               easy: EasyParams,
               job_id: str | None = None) -> APIHistoryEntry:
  id_or_title: str
  easy_set: EasySet

  workflow = deepcopy(workflow_template)

  ##############################################################################
  for id_or_title, easy_sets in easy.set.items():
    try:
      _, node = GetNode(workflow=workflow, id_or_title=id_or_title)
    except Exception as e:
      raise Exception(f'Failed to find {repr(id_or_title)}: {e}') from e

    for easy_set in easy_sets:
      try:
        pydash.set_(node.inputs, easy_set.field_path, easy_set.value)
        APIWorkflowNodeInfo.model_validate(node)
      except Exception as e:
        raise Exception(
            f'Failed to set {repr(id_or_title)} {easy_set.field_path} to {easy_set.value}: {e}'
        ) from e

  ##############################################################################
  important: List[APINodeID] = []

  for id_or_title in easy.get.keys():
    node_id, _ = GetNode(workflow=workflow, id_or_title=id_or_title)
    important.append(node_id)
  ##############################################################################
  if job_id is None:
    d = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    job_id = d + '_' + uuid.uuid4().hex
  job_history: APIHistoryEntry = await catapult.Catapult(
      job_id=job_id,
      prepared_workflow=workflow.model_dump(),
      important=important)

  for id_or_title, easy_gets in easy.get.items():
    node_id, _ = GetNode(workflow=workflow, id_or_title=id_or_title)
    for easy_get in easy_gets:
      if easy_get.type == 'literal':
        assert easy_get.to is None
        assert job_history.outputs is not None
        print(pydash.get(job_history.outputs[node_id].root,
                         easy_get.field_path))
      elif easy_get.type == 'file':
        assert easy_get.to is not None

        await DownloadPreviewImage(node_id=node_id,
                                   job_history=job_history,
                                   field_path=easy_get.field_path,
                                   config=easy.config,
                                   remote=easy.remote,
                                   local_dst_path=easy_get.to)
      else:
        raise Exception(f'Unknown easy_get.type: {easy_get.type}')
  return job_history
