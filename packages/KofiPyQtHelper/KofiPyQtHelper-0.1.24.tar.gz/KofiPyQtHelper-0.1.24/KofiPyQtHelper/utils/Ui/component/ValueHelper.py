#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 16:09:53
LastEditors  : Kofi
LastEditTime : 2023-07-11 16:09:53
Description  : 
"""
from KofiPyQtHelper.enums.ComboboxValueType import ComboboxValueType
from PyQt5.QtWidgets import QComboBox, QLineEdit, QTableWidget, QPlainTextEdit


class ValueHelper:
    def setComboValue(self, objInput: QComboBox, type: ComboboxValueType, items, val):
        if type == ComboboxValueType.Index.value:
            val = val if val != "" else 0
            current_index = val
        elif type == ComboboxValueType.Val.value:
            try:
                current_index = items.index(val)
            except:
                current_index = 0
        else:
            current_index = val

        objInput.setCurrentIndex(current_index)

    def setTextValue(self, objInput, val):
        objInput.setText(val)

    def setPlainTextValue(self, objInput, val):
        objInput.setPlainText(val)

    def getCurrentInput(self, name):
        for component in self.components:
            for key, objInput in component.items():
                if key == name:
                    return objInput
        return None

    def initComponentValues(self):
        # for component in self.components:
        #     for key, objInput in component.items():
        #         if key in self.variates:
        #             if type(objInput) == QLineEdit:
        #                 self.setTextValue(objInput, str(self.variates[key]))
        #             elif type(objInput) == QPlainTextEdit:
        #                 self.setPlainTextValue(objInput, str(self.variates[key]))
        #             elif type(objInput) == QComboBox:
        #                 # if key != "color":
        #                 self.setComboValue(
        #                     objInput,
        #                     self.items[key]["type"],
        #                     self.items[key]["data"],
        #                     self.variates[key],
        #                 )
        #             elif type(objInput) == QTableWidget:
        #                 self.setTableData(key, self.variates[key])
        component_setters = {
            QLineEdit: self.setTextValue,
            QPlainTextEdit: self.setPlainTextValue,
            QComboBox: self.setComboValue,
            QTableWidget: self.setTableData,
        }
        for component in self.components:
            for key, objInput in component.items():
                # 确保key存在于variates中
                if key not in self.variates:
                    continue
                # 获取组件的类型
                comp_type = type(objInput)
                # 如果组件类型在映射字典中，则调用相应的处理函数
                if comp_type in component_setters:
                    value = str(self.variates[key])
                    if comp_type == QComboBox:
                        # 对于QComboBox，需要提供额外的参数
                        component_setters[comp_type](
                            objInput,
                            self.items[key]["type"],
                            self.items[key]["data"],
                            value,
                        )
                    elif comp_type == QTableWidget:
                        # 对于QTableWidget，也需要特别处理
                        component_setters[comp_type](key, self.variates[key])
                    else:
                        # 对于其他类型，直接调用函数，并设置值
                        component_setters[comp_type](objInput, value)

    def clearComponentValues(self):
        """清除组件的值,恢复为默认值"""
        for component in self.components:
            for key, objInput in component.items():
                if type(objInput) == QLineEdit:
                    self.variates[key] = ""
                    self.setTextValue(objInput, str(self.variates[key]))
                elif type(objInput) == QComboBox:
                    self.setComboValue(
                        objInput,
                        self.items[key]["type"],
                        self.items[key]["data"],
                        self.variates[key],
                    )
                elif type(objInput) == QTableWidget:
                    self.variates[key] = []
                    self.setTableData(key, self.variates[key])

    def getCuttentInputValue(self, name: str):
        """通过组件名称获取组件值
        Args:
            name (str): 组件名称

        Returns:
            str: 组件当前值
        """
        obj = self.getCurrentInput(name)
        if obj != None:
            current = (
                obj.text()
                if type(obj) == QLineEdit
                else obj.currentText()
                if type(obj) == QComboBox
                else None
            )
            return current
        return None
