#!/usr/bin/env python
# coding=utf-8
"""
Author       : Kofi
Date         : 2022-08-10 10:24:51
LastEditors  : Kofi
LastEditTime : 2022-08-12 10:57:32
Description  : 组件创建
"""

import json, os
from loguru import logger
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from KofiPyQtHelper.utils.Command import Command
from KofiPyQtHelper.utils.Ui.LayoutHelper import LayoutHelper
from KofiPyQtHelper.utils.Ui.ComponentHelper import ComponentHelper


class UiHelper(Command, LayoutHelper, ComponentHelper):
    def __init__(self) -> None:
        self.class_ = self
        self.commands = {}
        self.variates = {}
        self.items = {}
        self.tables = {}
        self.trees = {}
        self.components = []
        self.load_layout_datas()
        self.gridInfo = {}
        Command.__init__(self)
        super(UiHelper, self).__init__()

    def load_layout_datas(self) -> None:
        """
        加载布局数据
        使用 self.category和self.name获取数据
        """
        path = os.path.abspath(
            "./config/interface/{0}/{1}.json".format(self.category, self.name)
        )
        try:
            with open(path, "r", encoding="UTF-8") as f:
                jsonData = json.load(f)
                if isinstance(jsonData, list):
                    self.layout_datas = jsonData
                    self.button_datas = None
                    self.closeCommand = None
                elif isinstance(jsonData, dict):
                    self.layout_datas = jsonData.get("layout", jsonData)
                    self.button_datas = jsonData.get("buttons", None)
                    # 分配关闭命令，不存在时默认为None
                    self.closeCommand = jsonData.get("closeCommand", None)
                else:
                    # 如果json_data既不是列表也不是字典，记录一个错误
                    logger.error(
                        f"Unexpected JSON data format in {path}. Must be list or dict."
                    )
        except FileNotFoundError:
            logger.error(f"File not found: {path}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in file {path}: {e}")
        except OSError as e:
            # 其他与操作系统相关的I/O异常（例如文件权限问题）
            logger.error(f"OS error while opening file {path}: {e}")
        except Exception as e:
            # 捕获其他可能的异常并记录
            logger.exception(
                f"An unexpected error occurred while loading layout data: {e}"
            )

    def init(self, parent: QWidget, infos):
        for info in infos:
            currentType = info["type"] if isinstance(info, dict) else info.type
            functionName = (
                "init" + currentType.capitalize()
                if isinstance(info["type"], str)
                else str(currentType.value).capitalize()
            )
            fun = getattr(self, functionName)
            box = fun(parent, info)
            if "content" in info and box is not None:
                if info["type"].capitalize() == "Gridbox" or (
                    info["type"].capitalize() == "Groupbox"
                    and "layout" in info
                    and info["layout"].capitalize() == "Gridbox"
                ):
                    self.initGridInfo(info, box)
                self.init(box, info["content"])

    def initGridInfo(self, info, component):
        self.gridInfo[component] = {
            "columns": info["columns"],
            "currentColumn": 0,
            "currentRow": 0,
        }

    def gridCalculate(self, component):
        self.gridInfo[component]["currentColumn"] += 1
        if (
            self.gridInfo[component]["currentColumn"]
            >= self.gridInfo[component]["columns"]
        ):
            self.gridInfo[component]["currentRow"] += 1
            self.gridInfo[component]["currentColumn"] = 0
