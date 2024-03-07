# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from tikit.tencentcloud.tione.v20211111 import models


def framework_table(framework_response):
    """

    :param framework_response:
    :type framework_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "框架名称",
        "版本",
        "训练模式"
    ]
    for framework in framework_response.FrameworkInfos:
        for framework_version in framework.VersionInfos:
            table.add_row([
                framework.Name,
                "".join(framework_version.Environment),
                ", ".join(framework_version.TrainingModes)
            ])
    table.align = 'l'
    return table


def framework_str(self):
    return framework_table(self).get_string()


def framework_html(self):
    return framework_table(self).get_html_string()


def bill_specs_table(bill_specs_response):
    """

    :param bill_specs_response:
    :type bill_specs_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "配置名称",
        "描述",
        "每小时价格（单位：元）"
    ]
    for spec in bill_specs_response.Specs:
        table.add_row([
            spec.SpecName,
            spec.SpecAlias,
            spec.SpecId
        ])
    return table


def bill_specs_str(self):
    return bill_specs_table(self).get_string()


def bill_specs_html(self):
    return bill_specs_table(self).get_html_string()


def taiji_hy_specs_table(taiji_hy_specs_response: models.DescribeTaijiHYSpecsResponse):
    """

    :param taiji_hy_specs_response: the response
    :type taiji_hy_specs_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTaijiHYSpecsResponse`
    :return: pretty table
    :rtype: PrettyTable
    """
    t = bill_specs_table(taiji_hy_specs_response)
    t.field_names = [
        "配置名称",
        "描述",
        "刊例价（单位：元/时）"
    ]
    return t


def taiji_hy_specs_str(self):
    return taiji_hy_specs_table(self).get_string()


def taiji_hy_specs_html(self):
    return taiji_hy_specs_table(self).get_html_string()


def training_task_table(training_task_response):
    """

    :param training_task_response:
    :type training_task_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`
    :return:
    :rtype:
    """
    paid_dict = {
        "PREPAID": "预付费",
        "POSTPAID_BY_HOUR": "后付费"
    }
    table = PrettyTable()
    table.field_names = [
        "任务ID",
        "名称",
        "训练框架",
        "训练模式",
        "计费模式",
        "标签",
        "状态",
        "运行时长",
        "训练开始时间"
    ]
    for task in training_task_response.TrainingTaskSet:
        if task.RuntimeInSeconds > 86400:
            time_str = "{}天{}小时{}分{}秒".format(int(task.RuntimeInSeconds / 86400),
                                              int((task.RuntimeInSeconds % 86400) / 3600),
                                              int((task.RuntimeInSeconds % 3600) / 60),
                                              task.RuntimeInSeconds % 60)
        elif task.RuntimeInSeconds > 3600:
            time_str = "{}小时{}分{}秒".format(int(task.RuntimeInSeconds / 3600),
                                           int((task.RuntimeInSeconds % 3600) / 60),
                                           task.RuntimeInSeconds % 60)
        else:
            time_str = "{}分{}秒".format(int(task.RuntimeInSeconds / 60), task.RuntimeInSeconds % 60)
        if len(task.FrameworkName) > 0:
            framework = "{}:{}".format(task.FrameworkName, task.FrameworkEnvironment)
        else:
            framework = "CUSTOM"  # TODO
        table.add_row([
            task.Id,
            task.Name,
            framework,
            task.TrainingMode,
            paid_dict[task.ChargeType],
            "\n".join(map(lambda x: "%s:%s" % (x.TagKey, x.TagValue), task.Tags)),
            task.Status,
            time_str,
            task.StartTime
        ])
    return table


def training_task_str(self):
    return training_task_table(self).get_string()


def training_task_html(self):
    return training_task_table(self).get_html_string()


def taiji_hy_task_table(taiji_hy_task_response):
    """

    :param taiji_hy_task_response:
    :type taiji_hy_task_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTaiJiHYTasksResponse`
    :return:
    :rtype:
    """
    paid_dict = {
        "PREPAID": "预付费",
        "POSTPAID_BY_HOUR": "后付费"
    }
    table = PrettyTable()
    table.field_names = [
        "任务ID",
        "名称",
        "训练模版",
        "训练模式",
        "计费模式",
        "标签",
        "状态",
        "运行时长",
        "训练开始时间"
    ]
    for task in taiji_hy_task_response.TrainingTaskSet:
        if task.RuntimeInSeconds > 86400:
            time_str = "{}天{}小时{}分{}秒".format(int(task.RuntimeInSeconds / 86400),
                                                   int((task.RuntimeInSeconds % 86400) / 3600),
                                                   int((task.RuntimeInSeconds % 3600) / 60),
                                                   task.RuntimeInSeconds % 60)
        elif task.RuntimeInSeconds > 3600:
            time_str = "{}小时{}分{}秒".format(int(task.RuntimeInSeconds / 3600),
                                               int((task.RuntimeInSeconds % 3600) / 60),
                                               task.RuntimeInSeconds % 60)
        else:
            time_str = "{}分{}秒".format(int(task.RuntimeInSeconds / 60), task.RuntimeInSeconds % 60)
        table.add_row([
            task.Id,
            task.Name,
            task.TAIJITemplateId,
            task.TrainingMode,
            paid_dict[task.ChargeType],
            "\n".join(map(lambda x: "%s:%s" % (x.TagKey, x.TagValue), task.Tags)),
            task.Status,
            time_str,
            task.StartTime
        ])
    return table


def taiji_hy_task_str(self):
    return taiji_hy_task_table(self).get_string()


def taiji_hy_task_html(self):
    return taiji_hy_task_table(self).get_html_string()


def log_table(log_response):
    """

    :param log_response:
    :type log_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "日志时间",
        "实例名称",
        "日志数据"
    ]
    for one_log in log_response.Content:
        table.add_row([
            one_log.Timestamp,
            one_log.PodName,
            one_log.Message
        ])
    table.align = 'l'
    return table


def log_str(self):
    return log_table(self).get_string()


def log_html(self):
    return log_table(self).get_html_string()


def taiji_hy_template_str(self):
    print(taiji_hy_template_table(self).get_string())
    print(taiji_hy_template_param_table(self).get_string())
    return "\n"

def taiji_hy_template_html(self):
    return taiji_hy_template_table(self).get_html_string() + "\n" + taiji_hy_template_param_table(self).get_html_string()

def taiji_hy_template_table(taiji_hy_template_response: models.DescribeTAIJITemplateResponse):
    """
    :param taiji_hy_template_response: the response
    :type DescribeTAIJITemplateResponse:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTAIJITemplateResponse`
    :return: pretty table
    :rtype: PrettyTable
    """
    table = PrettyTable()
    template = taiji_hy_template_response.Template
    template_dict={}
    template_dict["模型ID (ModelId)"] = template.ModelId
    template_dict["训练模式 (Pattern)"] = template.Pattern
    
    resource_value = "GPU类型 (GpuType）:" + str(template.ResourceConfig.GpuType) + "\n"
    resource_value += "GPU数量 (GpuNum) :" + str(template.ResourceConfig.Gpu) + "\n"
    resource_value += "实例数量 (InstanceNum) :" + str(template.ResourceConfig.InstanceNum) + "\n"
    resource_value += "机型 (InstanceType) :" + str(template.ResourceConfig.InstanceType) + "\n"
    template_dict["资源配置"] = resource_value
    
    table.field_names = list(["模板信息","  "])
    for k in template_dict.keys():
        table.add_row((k,template_dict[k]))
    table.set_style(12)
    # 设定左对齐
    table.align = 'l'
    ### 设定左侧不填充空白字符
    table.left_padding_width = 0
    return table

def taiji_hy_template_param_table(taiji_hy_template_response: models.DescribeTAIJITemplateResponse):
    """
    :param taiji_hy_template_response: the response
    :type DescribeTAIJITemplateResponse:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTAIJITemplateResponse`
    :return: pretty table
    :rtype: PrettyTable
    """
    table = PrettyTable()
    template = taiji_hy_template_response.Template
    params_table_dict = {}
    
    params_dict = params_str_to_dict(template.Params)

    params_remark_dict = params_str_to_dict(template.ParamsRemark)

    table.field_names = list(["可调参数名","参数描述","参考值"])
    for k in params_dict.keys():
        table.add_row((k,params_remark_dict[k],params_dict[k]))
    table.set_style(12)
    # 设定左对齐
    table.align = 'l'
    ### 设定左侧不填充空白字符
    table.left_padding_width = 0
    return table
    
def params_str_to_dict(input_str):
    input_str = input_str.strip("\"")
    input_str = input_str.strip("{")
    input_str = input_str.strip("}")
    # Split the string into key-value pairs
    key_value_pairs = input_str.split(', ')
    # Create a dictionary from the key-value pairs
    result_dict = {}
    for pair in key_value_pairs:
        key, value = pair.split('=')
        result_dict[key] = value
    return result_dict

def taiji_hy_template_list_str(self):
    return taiji_hy_template_list_table(self).get_string()

def taiji_hy_template_list_html(self):
    return taiji_hy_template_list_table(self).get_html_string()

def taiji_hy_template_list_table(taiji_hy_template_list_response: models.DescribeTAIJITemplateListResponse):
    """

    :param taiji_hy_template_list_response: the response
    :type DescribeTAIJITemplateListResponse:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTAIJITemplateListResponse`
    :return: pretty table
    :rtype: PrettyTable
    """
    table = PrettyTable()
    template_list = taiji_hy_template_list_response.TemplateList
    if len(template_list) < 0:
        return table
    table.field_names = [ 
        "模版名称",
        "模版描述",
        "模型ID",
        "训练模式",
        "配置方式",
    ]
    
    for template_info in template_list:
        table.add_row([
            template_info.Name,
            template_info.Desc,
            template_info.ModelId,
            template_info.Pattern,
            template_info.Style,
        ])
    return table

models.DescribeTrainingFrameworksResponse.__repr__ = framework_str
models.DescribeTrainingFrameworksResponse._repr_html_ = framework_html

models.DescribeBillingSpecsResponse.__repr__ = bill_specs_str
models.DescribeBillingSpecsResponse._repr_html_ = bill_specs_html

models.DescribeTrainingTasksResponse.__repr__ = training_task_str
models.DescribeTrainingTasksResponse._repr_html_ = training_task_html

models.DescribeTaiJiHYTasksResponse.__repr__ = taiji_hy_task_str
models.DescribeTaiJiHYTasksResponse._repr_html_ = taiji_hy_task_html

models.DescribeTaijiHYSpecsResponse.__repr__ = taiji_hy_specs_str
models.DescribeTaijiHYSpecsResponse._repr_html_ = taiji_hy_specs_html

models.DescribeLogsResponse.__repr__ = log_str
models.DescribeLogsResponse._repr_html_ = log_html


models.DescribeTAIJITemplateResponse.__repr__ = taiji_hy_template_str
models.DescribeTAIJITemplateResponse._repr_html_ = taiji_hy_template_html

models.DescribeTAIJITemplateListResponse.__repr__ = taiji_hy_template_list_str
models.DescribeTAIJITemplateListResponse._repr_html_ = taiji_hy_template_list_html


