# Legacy code from Bard, not used in Gemini.
from typing import List, Optional, Union, Dict, Tuple

from gemini.models.draft import GeminiDraft
from gemini.models.tools.tool import GeminiTool


class GeminiUserLocation:
    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def location_str(self) -> str:
        return self._input_list[0]

    @property
    def description(self) -> str:
        return self._input_list[1]

    @property
    def geo_position(self) -> list:
        return self._input_list[3][0][0][3]

    @property
    def image_url(self) -> str:
        return "https:" + self._input_list[4]

    def __str__(self) -> str:
        return self.location_str


class GeminiResult:
    def __init__(self, input_list: list):
        self._input_list = input_list
        self.conversation_id = self._input_list[1][0]
        self.response_id = self._input_list[1][1]

    @property
    def search_queries(self) -> list[str, int]:
        return self._input_list[2]

    @property
    def factuality_queries(self) -> Optional[list]:
        return self._input_list[3]

    @property
    def drafts(self) -> list[GeminiDraft]:
        return (
            [GeminiDraft(c) for c in self._input_list[4]] if self._input_list[4] else []
        )

    @property
    def location(self) -> GeminiUserLocation:
        return GeminiUserLocation(self._input_list[5])

    @property
    def progress_tool(self) -> GeminiTool:
        return GeminiTool(self._input_list[6]) if self._input_list[6] else None

    @property
    def country(self) -> str:
        return self._input_list[8]

    @property
    def topic(self) -> Optional[str]:
        if len(self._input_list) < 11 or not self._input_list[10]:
            return None
        return self._input_list[10][0]

    @property
    def tools_applied(self) -> list[GeminiTool]:
        if len(self._input_list) < 12:
            return []
        return (
            [GeminiTool(tool) for tool in self._input_list[11]]
            if self._input_list[11]
            else []
        )
